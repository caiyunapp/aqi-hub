import math
from typing import Dict, List, Optional, Tuple, Union

from aqi_hub.aqi_cn.common import AQI_COLOR, AQI_LEVEL, POLLUTANT_MAP, breakpoints


def cal_iaqi_usa(concentration: float, breakpoints: dict[str:List]) -> float:
    """
    计算单项空气质量指数 (IAQI)

    :param concentration: 污染物浓度值 (float)
    :param breakpoints: 分段标准，格式为列表 [(BP_lo, BP_hi, IAQI_lo, IAQI_hi), ...]
    :return: 对应的 IAQI 值 (float)
    """
    for bp_lo, bp_hi, iaqi_lo, iaqi_hi in breakpoints:
        if bp_lo <= concentration <= bp_hi:
            return ((iaqi_hi - iaqi_lo) / (bp_hi - bp_lo)) * (
                concentration - bp_lo
            ) + iaqi_lo
    return 500.0  # 如果超出范围，可以返回500


def cal_iaqi_cn(item: str, value: Union[int, float]) -> Optional[int]:
    """计算单项污染物的IAQI

    PM2.5和PM10无逐小时的IAQI计算方法，直接采用24小时的浓度限值计算
    """
    if not isinstance(value, (int, float)):
        raise TypeError("value must be int or float")
    if value < 0:
        raise ValueError("value must be greater than or equal to 0")
    if item not in breakpoints:
        raise ValueError(f"item must be one of {breakpoints.keys()}")
    if item == "SO2_1H" and value > 800:
        return None
    elif item == "O3_8H" and value > 800:
        return None
    else:
        iaqi = cal_iaqi_usa(value, breakpoints[item])
    if iaqi is not None:
        iaqi = math.ceil(iaqi)
    return iaqi


def cal_aqi_cn_hourly(
    pm25: float,
    pm10: float,
    so2: float,
    no2: float,
    co: float,
    o3: float,
) -> Tuple[int, dict[str:int]]:
    """计算逐小时的AQI

    Args:
        pm25 (float): PM2.5浓度, 单位: μg/m³
        pm10 (float): PM10浓度, 单位: μg/m³
        so2 (float): SO2浓度 (1小时), 单位: μg/m³
        no2 (float): NO2浓度 (1小时), 单位: μg/m³
        co (float): CO浓度 (1小时), 单位: mg/m³
        o3 (float): O3浓度 (1小时), 单位: μg/m³

    Returns:
        AQI: AQI值, 整数
        IAQI: IAQI值, 字典, 键为污染物名称, 值为IAQI值
    """
    pm25_iaqi = cal_iaqi_cn("PM25_1H", pm25)
    pm10_iaqi = cal_iaqi_cn("PM10_1H", pm10)
    so2_iaqi = cal_iaqi_cn("SO2_1H", so2)
    no2_iaqi = cal_iaqi_cn("NO2_1H", no2)
    co_iaqi = cal_iaqi_cn("CO_1H", co)
    o3_iaqi = cal_iaqi_cn("O3_1H", o3)
    iaqi = {
        "PM2.5": pm25_iaqi,
        "PM10": pm10_iaqi,
        "SO2": so2_iaqi,
        "NO2": no2_iaqi,
        "CO": co_iaqi,
        "O3": o3_iaqi,
    }
    aqi = max(pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_iaqi)
    return aqi, iaqi


def cal_aqi_cn_daily(
    pm25: float, pm10: float, so2: float, no2: float, co: float, o3: float
) -> Tuple[int, Dict[str, int]]:
    """计算日均AQI

    Args:
        pm25 (float): PM2.5浓度, 单位: μg/m³
        pm10 (float): PM10浓度, 单位: μg/m³
        so2 (float): SO2浓度 (24小时), 单位: μg/m³
        no2 (float): NO2浓度 (24小时), 单位: μg/m³
        co (float): CO浓度 (24小时), 单位: mg/m³
        o3 (float): O3浓度 (8小时), 单位: μg/m³

    Returns:
        AQI: AQI值, 整数
        IAQI: IAQI值, 字典, 键为污染物名称, 值为IAQI值
    """
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
    aqi = max(pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_iaqi)
    return aqi, iaqi


def cal_primary_pollutant(iaqi: Dict[str, int]) -> List[str]:
    """计算首要污染物

    Args:
        iaqi (Dict[str, int]): IAQI

    Returns:
        首要污染物
    """
    primary_pollutant = []
    for item, value in iaqi.items():
        if value > 50:
            primary_pollutant.append(item)
    return primary_pollutant


def cal_exceed_pollutant(iaqi: Dict[str, int]) -> List[str]:
    """计算超标污染物

    Args:
        iaqi (Dict[str, int]): IAQI

    Returns:
        超标污染物
    """
    exceed_pollutant = []
    for item, value in iaqi.items():
        if value > 100:
            exceed_pollutant.append(item)
    return exceed_pollutant


def get_aqi_level(aqi: int) -> int:
    """获取中国标准下的AQI等级

    Args:
        aqi (int): AQI值

    Returns:
        AQI等级
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
        raise ValueError(f"color_type must be one of {AQI_COLOR.keys()}")
    return AQI_COLOR[color_type][aqi_level]


class AQI:
    """空气质量指数 (AQI) 计算器

    Args:
        pm25 (float): PM2.5浓度, 单位: μg/m³
        pm10 (float): PM10浓度, 单位: μg/m³
        so2 (float): SO2浓度, 单位: μg/m³
        no2 (float): NO2浓度, 单位: μg/m³
        co (float): CO浓度, 单位: mg/m³
        o3 (float): O3浓度, 单位: μg/m³
        data_type (str): 数据类型, 可选 'hourly', 'daily'
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
            return cal_aqi_cn_hourly(
                self.pm25, self.pm10, self.so2, self.no2, self.co, self.o3
            )
        elif self.data_type == "daily":
            return cal_aqi_cn_daily(
                self.pm25, self.pm10, self.so2, self.no2, self.co, self.o3
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
