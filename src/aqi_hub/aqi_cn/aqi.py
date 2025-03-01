import math
from typing import List, Optional, Union

from aqi_hub.aqi_cn.common import breakpoints


def _calculate_iaqi(concentration: float, breakpoints: dict[str:List]) -> float:
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
        iaqi = _calculate_iaqi(value, breakpoints[item])
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
    cal_primary: bool = True,
) -> int:
    """计算逐小时的AQI

    :param pm25: PM2.5浓度
    :param pm10: PM10浓度
    :param so2: SO2浓度 (1小时)
    :param no2: NO2浓度 (1小时)
    :param co: CO浓度 (1小时)
    :param o3: O3浓度 (1小时)
    :return: AQI
    """
    pm25_iaqi = cal_iaqi_cn("PM25_1H", pm25)
    pm10_iaqi = cal_iaqi_cn("PM10_1H", pm10)
    so2_iaqi = cal_iaqi_cn("SO2_1H", so2)
    no2_iaqi = cal_iaqi_cn("NO2_1H", no2)
    co_iaqi = cal_iaqi_cn("CO_1H", co)
    o3_iaqi = cal_iaqi_cn("O3_1H", o3)
    aqi = max(pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_iaqi)
    if cal_primary:
        pass
    return aqi


def get_aqi_level(aqi: int) -> int:
    """获取中国标准下的AQI等级

    :param aqi: AQI值
    :return: AQI等级
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


if __name__ == "__main__":
    print(cal_iaqi_cn("PM25_24H", 35))
    print(cal_iaqi_cn("PM25_1H", 501))
    print(cal_iaqi_cn("O3_8H", 801))
    print(cal_aqi_cn_hourly(35, 50, 150, 100, 5, 160))
    print(cal_aqi_cn_hourly(35, 50, 150, 100, 5, 160))
