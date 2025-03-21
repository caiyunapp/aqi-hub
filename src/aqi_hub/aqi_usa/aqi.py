"""
AQI_USA 计算模块

该模块实现了美国空气质量指数(AQI)的计算方法。
"""

import warnings
from typing import Dict, List, Tuple, Union

from aqi_hub.aqi_usa.common import (
    AQI_COLOR,
    AQI_LEVEL,
    breakpoints,
    minmaxs,
    scales,
    singularities,
)


def cal_iaqi_usa(conc: Union[None, int, float], item: str) -> Union[None, int]:
    """
    计算单项空气质量指数 (IAQI)

    Args:
        concentration: 污染物浓度值
        item: 污染物类型，如 PM25_24H, PM10_24H 等

    Returns:
        对应的 IAQI 值
    """
    if item not in breakpoints:
        raise ValueError(f"item: {item} must be one of {breakpoints.keys()}")
    if conc is None:
        warnings.warn(f"conc is None for {item}")
        return None
    bk_points = breakpoints[item]
    _min, _max = minmaxs[item]
    # 浓度值缩放因子, 用于将浓度值转换为整数
    scale = scales[item]
    conc = int(conc * scale)
    _min = int(_min * scale)
    _max = int(_max * scale)
    singularity = singularities.get(item, 0)
    singularity = int(singularity * scale)
    match item:
        case "O3_1H":
            # 臭氧 1 小时 < 0.125 ppm, 无数据. 应该用 臭氧8小时 的浓度值
            if conc < singularity:
                warnings.warn(
                    f"O3_1H concentration {conc} is less than 0.125 ppm, return None"
                )
                return None
            elif conc >= _max:
                warnings.warn(
                    f"O3_1H concentration {conc} is greater than {_max}, return 500"
                )
                return 500
        case "O3_8H":
            if conc < _min:
                warnings.warn(
                    f"O3_8H concentration {conc} is less than {_min}, return None"
                )
                return None
            elif conc >= singularity:
                # 臭氧 8 小时 >= 0.201 ppm, 无数据. 应该用 臭氧1小时 的浓度值
                warnings.warn(
                    f"O3_8H concentration {conc} is greater than {singularity}, "
                    "Please use O3_1H concentration instead. return None"
                )
                return None
        case "SO2_1H":
            # 二氧化硫1小时浓度 > 304 ppb, 无数据. 应该用 二氧化硫24小时 的浓度值
            if conc > singularity:
                warnings.warn(
                    "1-hr SO2 concentrations do not define higher AQI values (≥200). "
                    "AQI values of 200 or greater are calculated with 24-hour SO2 concentration"
                )
                return None
        case "SO2_24H":
            # 二氧化硫24小时浓度 < 305 ppb, 无数据. 应该用 二氧化硫1小时 的浓度值
            if conc < singularity:
                warnings.warn(
                    "24-hr SO2 concentrations do not define higher AQI values (≥300). "
                    "AQI values of 300 or greater are calculated with 1-hour SO2 concentration"
                )
                return None
            elif conc >= _max:
                # 二氧化硫24小时浓度 >= 1004 ppb, 返回500
                warnings.warn(
                    f"SO2_24H concentration {conc} is greater than {_max}, return 500"
                )
                return 500
        case _:
            # 如果浓度值在最后一个区间内
            if conc >= _max:
                warnings.warn(
                    f"{item} concentration {conc} is greater than {_max}, return 500"
                )
                return 500

    # 按照浓度值从小到大排序
    sorted_bk_points = sorted(bk_points, key=lambda x: x[0])

    # 标准的线性插值计算
    for _, (bp_lo, bp_hi, iaqi_lo, iaqi_hi) in enumerate(sorted_bk_points):
        # 将浓度值和断点值转换为整数
        bp_lo = int(bp_lo * scale)
        bp_hi = int(bp_hi * scale)
        if bp_lo <= conc <= bp_hi:
            # 线性插值计算
            iaqi = ((iaqi_hi - iaqi_lo) * (conc - bp_lo)) / (bp_hi - bp_lo) + iaqi_lo
            return int(iaqi)

    # 如果没有找到合适的区间
    warnings.warn(
        f"No suitable interval found for {item} with concentration {conc}, return None"
    )
    return None


def cal_aqi_usa(
    pm25: float,
    pm10: float,
    so2_1h: float,
    no2: float,
    co: float,
    o3_8h: float,
    so2_24h: float = None,
    o3_1h: float = None,
) -> Tuple[Union[int, None], Dict[str, Union[int, None]]]:
    """计算美国AQI

    Args:
        pm25: PM2.5浓度, 单位: μg/m³ (24小时平均)
        pm10: PM10浓度, 单位: μg/m³ (24小时平均)
        so2_1h: SO2浓度, 单位: ppb (1小时平均)
        so2_24h: SO2浓度, 单位: ppb (24小时平均)
        no2: NO2浓度, 单位: ppb (1小时平均)
        co: CO浓度, 单位: ppm (8小时平均)
        o3_8h: O3浓度, 单位: ppm (8小时平均)
        o3_1h: O3浓度, 单位: ppm (1小时平均)，可选

    Returns:
        (AQI, IAQI) 元组:
            - AQI: AQI值
            - IAQI: 各污染物的IAQI值字典
    """
    # 使用cal_iaqi_usa计算各污染物的IAQI
    pm25_iaqi = cal_iaqi_usa(pm25, "PM25_24H")
    pm10_iaqi = cal_iaqi_usa(pm10, "PM10_24H")
    so2_1h_iaqi = cal_iaqi_usa(so2_1h, "SO2_1H")
    so2_24h_iaqi = cal_iaqi_usa(so2_24h, "SO2_24H")
    # 取 SO2 1小时和24小时 IAQI 的最大值
    so2_iaqi = (
        max(filter(None, [so2_1h_iaqi, so2_24h_iaqi]))
        if any([so2_1h_iaqi, so2_24h_iaqi])
        else None
    )
    no2_iaqi = cal_iaqi_usa(no2, "NO2_1H")
    co_iaqi = cal_iaqi_usa(co, "CO_8H")
    o3_8h_iaqi = cal_iaqi_usa(o3_8h, "O3_8H")
    o3_1h_iaqi = cal_iaqi_usa(o3_1h, "O3_1H")
    # 取 O3 8小时和1小时 IAQI 的最大值
    o3_iaqi = (
        max(filter(None, [o3_8h_iaqi, o3_1h_iaqi]))
        if any([o3_8h_iaqi, o3_1h_iaqi])
        else None
    )

    iaqi_values = [
        pm25_iaqi,
        pm10_iaqi,
        so2_iaqi,
        no2_iaqi,
        co_iaqi,
        o3_iaqi,
    ]

    iaqi = {
        "PM2.5": pm25_iaqi,
        "PM10": pm10_iaqi,
        "SO2": so2_iaqi,
        "NO2": no2_iaqi,
        "CO": co_iaqi,
        "O3": o3_iaqi,
    }
    aqi = max(filter(None, iaqi_values)) if any(iaqi_values) else None
    return aqi, iaqi


def get_aqi_level(aqi: int) -> int:
    """获取美国标准下的AQI等级

    Args:
        aqi: AQI值

    Returns:
        AQI等级 (1-6)
    """
    if aqi < 0 or aqi > 500:
        raise ValueError("AQI must be between 0 and 500")
    if aqi <= 50:
        return 1
    elif aqi <= 100:
        return 2
    elif aqi <= 150:
        return 3
    elif aqi <= 200:
        return 4
    elif aqi <= 300:
        return 5
    else:
        return 6


def cal_primary_pollutant(iaqi: Dict[str, int]) -> List[str]:
    """计算首要污染物

    Args:
        iaqi: IAQI字典

    Returns:
        首要污染物列表
    """
    if not iaqi:
        warnings.warn("IAQI字典为空")
        return []

    # 检查是否所有值都为None
    if all(value is None for value in iaqi.values()):
        warnings.warn("所有污染物IAQI值均为None")
        return []

    max_iaqi = max(filter(None, iaqi.values()))
    return [pollutant for pollutant, value in iaqi.items() if value == max_iaqi]


def get_aqi_level_color(
    aqi_level: int, color_type: str
) -> Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]:
    """获取AQI等级对应的颜色

    其中, 颜色类型包括 RGB, CMYK, RGB_HEX, CMYK_HEX.

    Args:
        aqi_level (int): AQI等级
        color_type (str): 颜色类型, 可选 RGB, CMYK, RGB_HEX, CMYK_HEX

    Returns:
        如果是 RGB 或 CMYK, 返回一个元组 (int, int, int) 或 (int, int, int, int)
        如果是 RGB_HEX 或 CMYK_HEX, 返回一个字符串
    """
    if aqi_level not in AQI_LEVEL:
        raise ValueError(f"aqi_level must be one of {AQI_LEVEL}")
    if color_type not in AQI_COLOR:
        raise ValueError(f"color_type must be one of {list(AQI_COLOR.keys())}")
    return AQI_COLOR[color_type][aqi_level]


class AQI:
    """美国空气质量指数 (AQI) 计算器

    Args:
        pm25: PM2.5浓度, 单位: μg/m³ (24小时平均)
        pm10: PM10浓度, 单位: μg/m³ (24小时平均)
        so2: SO2浓度, 单位: ppb (1小时平均)
        no2: NO2浓度, 单位: ppb (1小时平均)
        co: CO浓度, 单位: ppm (8小时平均)
        o3_8h: O3浓度, 单位: ppb (8小时平均)
        o3_1h: O3浓度, 单位: ppb (1小时平均)，可选
    """

    def __init__(
        self,
        pm25: float,
        pm10: float,
        so2_1h: float,
        no2: float,
        co: float,
        o3_8h: float,
        so2_24h: float = None,
        o3_1h: float = None,
    ):
        self.pm25 = pm25
        self.pm10 = pm10
        self.so2_1h = so2_1h
        self.so2_24h = so2_24h
        self.no2 = no2
        self.co = co
        self.o3_8h = o3_8h
        self.o3_1h = o3_1h
        self.AQI, self.IAQI = self.get_aqi()

    def get_aqi(self) -> Tuple[int, Dict[str, int]]:
        """计算AQI和IAQI

        Returns:
            (AQI, IAQI) 元组
        """
        return cal_aqi_usa(
            self.pm25,
            self.pm10,
            self.so2_1h,
            self.no2,
            self.co,
            self.o3_8h,
            self.so2_24h,
            self.o3_1h,
        )

    @property
    def aqi_level(self) -> int:
        """获取AQI等级

        Returns:
            AQI等级 (1-6)
        """
        return get_aqi_level(self.AQI)

    @property
    def primary_pollutant(self) -> List[str]:
        """获取首要污染物

        Returns:
            首要污染物列表
        """
        return cal_primary_pollutant(self.IAQI)

    @property
    def aqi_color_rgb(self) -> Tuple[int, int, int]:
        """获取AQI等级对应的RGB颜色值

        Returns:
            RGB颜色值元组 (R, G, B)
        """
        return get_aqi_level_color(self.aqi_level, "RGB")

    @property
    def aqi_color_cmyk(self) -> Tuple[int, int, int, int]:
        """获取AQI等级对应的CMYK颜色值

        Returns:
            CMYK颜色值元组 (C, M, Y, K)
        """
        return get_aqi_level_color(self.aqi_level, "CMYK")

    @property
    def aqi_color_rgb_hex(self) -> str:
        """获取AQI等级对应的RGB十六进制颜色值

        Returns:
            RGB十六进制颜色值字符串
        """
        return get_aqi_level_color(self.aqi_level, "RGB_HEX")

    @property
    def aqi_color_cmyk_hex(self) -> str:
        """获取AQI等级对应的CMYK十六进制颜色值

        Returns:
            CMYK十六进制颜色值字符串
        """
        return get_aqi_level_color(self.aqi_level, "CMYK_HEX")
