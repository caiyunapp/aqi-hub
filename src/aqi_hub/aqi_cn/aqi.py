"""
空气质量指数 (AQI) 计算模块

本模块实现了基于中国环境空气质量标准 (GB 3095-2012) 的空气质量指数 (AQI) 计算方法。
支持计算小时和日均 AQI，以及相关的空气质量评价指标。

主要功能:
1. 计算单项空气质量指数 (IAQI)
2. 计算小时和日均 AQI
3. 识别首要污染物和超标污染物
4. 获取 AQI 等级和对应的颜色标识

支持的污染物:
- PM2.5 (细颗粒物)
- PM10 (可吸入颗粒物)
- SO2 (二氧化硫)
- NO2 (二氧化氮)
- CO (一氧化碳)
- O3 (臭氧)

使用示例:
    >>> from aqi_hub.aqi_cn.aqi import AQI
    >>> # 创建 AQI 计算器实例 (小时值)
    >>> aqi = AQI(pm25=35, pm10=50, so2=150, no2=100, co=5, o3=160, data_type="hourly")
    >>> print(f"AQI: {aqi.AQI}")
    >>> print(f"首要污染物: {aqi.primary_pollutant_cn}")
    >>> print(f"AQI 等级: {aqi.aqi_level}")
    >>> print(f"颜色 (RGB): {aqi.aqi_color_rgb}")

参考标准:
    GB 3095-2012 环境空气质量标准
    HJ 633-2012 环境空气质量指数 (AQI) 技术规定
"""

import math
import warnings
from typing import Dict, List, Optional, Tuple, Union

from aqi_hub.aqi_cn.common import AQI_COLOR, AQI_LEVEL, POLLUTANT_MAP, breakpoints


def _cal_iaqi_cn(concentration: float, breakpoints: dict[str:List]) -> float:
    """
    计算单项空气质量指数 (IAQI)

    根据污染物浓度值和对应的分段标准计算 IAQI 值。计算公式为：
    IAQI = [(IAQI_hi - IAQI_lo)/(BP_hi - BP_lo)] × (C - BP_lo) + IAQI_lo

    Args:
        concentration: 污染物浓度值 (float)
        breakpoints: 分段标准, 格式为列表 [(BP_lo, BP_hi, IAQI_lo, IAQI_hi), ...]
            - BP_lo: 该区间的浓度下限值
            - BP_hi: 该区间的浓度上限值
            - IAQI_lo: 该区间的 IAQI 下限值
            - IAQI_hi: 该区间的 IAQI 上限值

    Returns:
        float: 对应的 IAQI 值。如果超出最高分段范围，返回 500.0
    """
    for bp_lo, bp_hi, iaqi_lo, iaqi_hi in breakpoints:
        if bp_lo <= concentration <= bp_hi:
            return ((iaqi_hi - iaqi_lo) / (bp_hi - bp_lo)) * (
                concentration - bp_lo
            ) + iaqi_lo
    return 500.0  # 如果超出范围, 可以返回500


def cal_iaqi_cn(item: str, value: Union[int, float, None]) -> Optional[int]:
    """计算单项污染物的 IAQI (Individual Air Quality Index)

    根据污染物类型和浓度值计算对应的 IAQI。
    PM2.5 和 PM10 无逐小时的 IAQI 计算方法, 直接采用 24 小时的浓度限值计算。
    SO2_1H 和 O3_8H 的浓度限值为 800 μg/m³, 超出 800 μg/m³ 时, IAQI 取 500。

    Args:
        item: 污染物名称, 可选值为:
            - "PM25_1H": PM2.5 1 小时浓度
            - "PM10_1H": PM10 1 小时浓度
            - "SO2_1H": SO2 1 小时浓度
            - "O3_8H": O3 8 小时浓度
            - "NO2_1H": NO2 1 小时浓度
            - "CO_1H": CO 1 小时浓度
            - "O3_1H": O3 1 小时浓度
            - "PM25_24H": PM2.5 24 小时浓度
            - "PM10_24H": PM10 24 小时浓度
            - "SO2_24H": SO2 24 小时浓度
            - "NO2_24H": NO2 24 小时浓度
            - "CO_24H": CO 24 小时浓度
            - "O3_8H": O3 8 小时浓度
        value: 污染物浓度值。对于气态污染物 SO2, NO2, O3 单位为 μg/m³,
              CO 单位为 mg/m³, 颗粒物 PM2.5, PM10 单位为 μg/m³

    Returns:
        Optional[int]: IAQI 值。当输入值无效时返回 None
            - 当 value 为 None 时返回 None
            - 当 value 小于 0 时返回 None
            - 当 SO2_1H 或 O3_8H 浓度超过 800 μg/m³ 时返回 None
    """
    if value is None:
        warnings.warn(f"value is None for {item}")
        return None
    if not isinstance(value, (int, float)):
        raise TypeError("value must be int or float")
    if value < 0:
        warnings.warn(f"value is less than 0 for {item}")
        return None
    if item not in breakpoints:
        raise ValueError(f"item must be one of {breakpoints.keys()}")
    if item == "SO2_1H" and value > 800:
        warnings.warn(f"value is greater than 800 for {item}")
        return None
    elif item == "O3_8H" and value > 800:
        warnings.warn(f"value is greater than 800 for {item}")
        return None
    else:
        iaqi = _cal_iaqi_cn(value, breakpoints[item])
    if iaqi is not None:
        iaqi = math.ceil(iaqi)
    return iaqi


def cal_aqi_cn(
    pm25: float,
    pm10: float,
    so2: float,
    no2: float,
    co: float,
    o3: float,
    data_type: str = "hourly",
) -> Tuple[Optional[int], Dict[str, Optional[int]]]:
    """计算空气质量指数 (AQI)

    基于六项污染物的浓度值计算 AQI。AQI 值取六项污染物 IAQI 的最大值。
    支持计算小时值和日均值 AQI。

    Args:
        pm25: PM2.5 浓度, 单位: μg/m³
        pm10: PM10 浓度, 单位: μg/m³
        so2: SO2 浓度, 单位: μg/m³
        no2: NO2 浓度, 单位: μg/m³
        co: CO 浓度, 单位: mg/m³
        o3: O3 浓度, 单位: μg/m³
        data_type: 数据类型，可选值:
            - "hourly": 使用小时值计算
            - "daily": 使用日均值计算 (O3 使用 8 小时滑动平均)

    Returns:
        Tuple[Optional[int], Dict[str, Optional[int]]]:
            - 第一个元素为 AQI 值 (整数或 None)
                - 当所有 IAQI 值都为 None 时返回 None
                - 当有有效的 IAQI 值时返回最大值
            - 第二个元素为各污染物的 IAQI 值字典，键为污染物名称，值为 IAQI 值或 None
                - 当污染物浓度值无效时返回 None
                - 当污染物浓度值有效时返回对应的 IAQI 值
    """
    if data_type not in ["hourly", "daily"]:
        raise ValueError("data_type must be 'hourly' or 'daily'")

    if data_type == "hourly":
        pm25_iaqi = cal_iaqi_cn("PM25_1H", pm25)
        pm10_iaqi = cal_iaqi_cn("PM10_1H", pm10)
        so2_iaqi = cal_iaqi_cn("SO2_1H", so2)
        no2_iaqi = cal_iaqi_cn("NO2_1H", no2)
        co_iaqi = cal_iaqi_cn("CO_1H", co)
        o3_iaqi = cal_iaqi_cn("O3_1H", o3)
    else:
        pm25_iaqi = cal_iaqi_cn("PM25_24H", pm25)
        pm10_iaqi = cal_iaqi_cn("PM10_24H", pm10)
        so2_iaqi = cal_iaqi_cn("SO2_24H", so2)
        no2_iaqi = cal_iaqi_cn("NO2_24H", no2)
        co_iaqi = cal_iaqi_cn("CO_24H", co)
        o3_iaqi = cal_iaqi_cn("O3_8H", o3)

    iaqi = {
        "PM2.5": pm25_iaqi,
        "PM10": pm10_iaqi,
        "SO2": so2_iaqi,
        "NO2": no2_iaqi,
        "CO": co_iaqi,
        "O3": o3_iaqi,
    }
    iaqi_values = [v for v in iaqi.values() if v is not None]
    aqi = max(iaqi_values) if iaqi_values else None
    return aqi, iaqi


def cal_primary_pollutant(iaqi: Dict[str, int]) -> List[str]:
    """计算首要污染物

    首要污染物是指 IAQI 值大于 50 且最大的污染物。如果有多个污染物的 IAQI 值相同且最大，
    则这些污染物都是首要污染物。

    Args:
        iaqi: IAQI 值字典，键为污染物名称，值为 IAQI 值

    Returns:
        List[str]: 首要污染物列表。如果没有首要污染物，返回空列表
    """
    if not isinstance(iaqi, dict):
        raise TypeError("iaqi must be a dictionary")
    primary_pollutant = []
    valid_values = {k: v for k, v in iaqi.items() if v is not None}
    if not valid_values:
        return primary_pollutant
    max_iaqi = max(valid_values.values())
    for item, value in valid_values.items():
        if value > 50 and value == max_iaqi:
            primary_pollutant.append(item)
    return primary_pollutant


def cal_exceed_pollutant(iaqi: Dict[str, int]) -> List[str]:
    """计算超标污染物

    超标污染物是指 IAQI 值大于 100 的污染物。IAQI 大于 100 表示该污染物浓度超过
    国家空气质量二级标准（适用于居住区、商业交通居民混合区、文化区、一般工业区和农村地区）。

    Args:
        iaqi: IAQI 值字典，键为污染物名称，值为 IAQI 值

    Returns:
        List[str]: 超标污染物列表。如果没有超标污染物，返回空列表
    """
    if not isinstance(iaqi, dict):
        raise TypeError("iaqi must be a dictionary")
    exceed_pollutant = []
    for item, value in iaqi.items():
        if value is not None and value > 100:
            exceed_pollutant.append(item)
    return exceed_pollutant


def get_aqi_level(aqi: Union[int, None]) -> Union[int, None]:
    """获取中国标准下的 AQI 等级

    AQI 分为六个等级:
    1 级 (0-50): 优
    2 级 (51-100): 良
    3 级 (101-150): 轻度污染
    4 级 (151-200): 中度污染
    5 级 (201-300): 重度污染
    6 级 (>300): 严重污染

    Args:
        aqi: AQI 值，范围 0-500

    Returns:
        Union[int, None]: AQI 等级 (1-6)。当输入无效时返回 None
            - 当 aqi 为 None 时返回 None
            - 当 aqi 不是数值类型时抛出 ValueError
            - 当 aqi 小于 0 或大于 500 时抛出 ValueError
    """
    if aqi is None:
        warnings.warn("AQI is None")
        return None
    if not isinstance(aqi, (int, float)):
        raise ValueError("AQI must be a number")
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


def get_aqi_level_color(
    aqi_level: int, color_type: str
) -> Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]:
    """获取 AQI 等级对应的颜色

    不同 AQI 等级使用不同的颜色标识:
    1 级: 绿色
    2 级: 黄色
    3 级: 橙色
    4 级: 红色
    5 级: 紫色
    6 级: 褐红色

    Args:
        aqi_level: AQI 等级 (1-6)
        color_type: 颜色类型，可选值:
            - "RGB": 返回 RGB 颜色元组 (R,G,B)
            - "CMYK": 返回 CMYK 颜色元组 (C,M,Y,K)
            - "RGB_HEX": 返回 RGB 十六进制颜色代码 (如 "#FF0000")
            - "CMYK_HEX": 返回 CMYK 十六进制颜色代码

    Returns:
        Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]:
            根据 color_type 返回对应格式的颜色值

    Raises:
        ValueError: 当 aqi_level 不在 1-6 范围内，或 color_type 不是有效值时
    """
    if aqi_level not in AQI_LEVEL:
        raise ValueError(f"aqi_level must be one of {AQI_LEVEL}")
    if color_type not in AQI_COLOR:
        raise ValueError(f"color_type must be one of {AQI_COLOR.keys()}")
    return AQI_COLOR[color_type][aqi_level]


class AQI:
    """空气质量指数 (AQI) 计算器

    用于计算和评估空气质量指数的类。支持计算小时值和日均值 AQI，
    并提供 AQI 等级、颜色标识、首要污染物等信息。

    Attributes:
        AQI (int): 空气质量指数值
        IAQI (Dict[str, int]): 各污染物的 IAQI 值
        aqi_level (int): AQI 等级 (1-6)
        aqi_color_rgb (Tuple[int, int, int]): RGB 颜色元组
        aqi_color_cmyk (Tuple[int, int, int, int]): CMYK 颜色元组
        aqi_color_rgb_hex (str): RGB 十六进制颜色代码
        aqi_color_cmyk_hex (str): CMYK 十六进制颜色代码
        primary_pollutant (List[str]): 首要污染物列表 (英文)
        exceed_pollutant (List[str]): 超标污染物列表 (英文)
        primary_pollutant_cn (List[str]): 首要污染物列表 (中文)
        exceed_pollutant_cn (List[str]): 超标污染物列表 (中文)

    Args:
        pm25: PM2.5 浓度, 单位: μg/m³
        pm10: PM10 浓度, 单位: μg/m³
        so2: SO2 浓度, 单位: μg/m³
        no2: NO2 浓度, 单位: μg/m³
        co: CO 浓度, 单位: mg/m³
        o3: O3 浓度, 单位: μg/m³
        data_type: 数据类型，可选值:
            - "hourly": 使用小时值计算
            - "daily": 使用日均值计算 (O3 使用 8 小时滑动平均)
    """

    def __init__(
        self,
        pm25: float,
        pm10: float,
        so2: float,
        no2: float,
        co: float,
        o3: float,
        data_type: str,
    ):
        self.pm25 = pm25
        self.pm10 = pm10
        self.so2 = so2
        self.no2 = no2
        self.co = co
        self.o3 = o3
        self.data_type = data_type
        if data_type not in ["hourly", "daily"]:
            raise ValueError("data_type must be 'hourly' or 'daily'")
        self.AQI, self.IAQI = self.get_aqi()

    def get_aqi(self) -> int:
        if self.data_type == "hourly":
            return cal_aqi_cn(
                self.pm25,
                self.pm10,
                self.so2,
                self.no2,
                self.co,
                self.o3,
                self.data_type,
            )
        elif self.data_type == "daily":
            return cal_aqi_cn(
                self.pm25,
                self.pm10,
                self.so2,
                self.no2,
                self.co,
                self.o3,
                self.data_type,
            )
        else:
            raise ValueError("data_type must be 'hourly' or 'daily'")

    @property
    def aqi_level(self) -> int:
        return get_aqi_level(self.AQI)

    @property
    def aqi_color_rgb(self) -> Tuple[int, int, int]:
        return get_aqi_level_color(self.aqi_level, "RGB")

    @property
    def aqi_color_cmyk(self) -> Tuple[int, int, int, int]:
        return get_aqi_level_color(self.aqi_level, "CMYK")

    @property
    def aqi_color_rgb_hex(self) -> str:
        return get_aqi_level_color(self.aqi_level, "RGB_HEX")

    @property
    def aqi_color_cmyk_hex(self) -> str:
        return get_aqi_level_color(self.aqi_level, "CMYK_HEX")

    @property
    def primary_pollutant(self) -> List[str]:
        return cal_primary_pollutant(self.IAQI)

    @property
    def exceed_pollutant(self) -> List[str]:
        return cal_exceed_pollutant(self.IAQI)

    @property
    def primary_pollutant_cn(self) -> List[str]:
        return [POLLUTANT_MAP[item] for item in self.primary_pollutant]

    @property
    def exceed_pollutant_cn(self) -> List[str]:
        return [POLLUTANT_MAP[item] for item in self.exceed_pollutant]


if __name__ == "__main__":
    # print(cal_iaqi_cn("PM25_24H", 35))
    # print(cal_iaqi_cn("PM25_1H", 501))
    # print(cal_iaqi_cn("O3_8H", 801))
    # print(cal_aqi_cn_hourly(35, 50, 150, 100, 5, 160))
    # print(cal_aqi_cn_hourly(35, 50, 150, 100, 5, 160))
    aqi = AQI(101, 70, 150, 100, 5, 160, "hourly")
    print(f"aqi: {aqi.AQI}")
    print(aqi.aqi_level)
    aqi = AQI(35, 50, 150, 100, 5, 160, "daily")
    print(aqi.AQI)  # 150
