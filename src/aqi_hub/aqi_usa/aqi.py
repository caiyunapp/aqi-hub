"""
AQI_USA 计算模块

该模块实现了美国空气质量指数(AQI)的计算方法。
"""

import warnings
from typing import Dict, List, Optional, Tuple, Union

from aqi_hub.aqi_usa.common import (
    AQI_LEVEL,
    POLLUTANT,
    POLLUTANT_UNITS,
    breakpoints,
    minmaxs,
    scales,
    singularities
)



def _calculate_iaqi(conc: Union[int, float], item: str) -> Union[int, None]:
    """
    计算单项空气质量指数 (IAQI)

    Args:
        concentration: 污染物浓度值
        item: 污染物类型，如 PM25_24H, PM10_24H 等

    Returns:
        对应的 IAQI 值
    """
    if item not in breakpoints:
        raise ValueError(f"item must be one of {breakpoints.keys()}")
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


# def cal_iaqi_usa(item: str, value: Union[int, float]) -> Optional[int]:
#     """计算单项污染物的IAQI

#     Args:
#         item: 污染物类型，如 PM25_24H, PM10_24H 等
#         value: 污染物浓度值

#     Returns:
#         IAQI值，如果超出范围则返回None
#     """
#     if not isinstance(value, (int, float)):
#         raise TypeError("value must be int or float")
#     if value < 0:
#         raise ValueError("value must be greater than or equal to 0")
#     if item not in breakpoints:
#         raise ValueError(f"item must be one of {breakpoints.keys()}")

#     # # 检查是否是特殊情况
#     # if item in special_cases and value in special_cases[item]:
#     #     return special_cases[item][value]

#     # # 检查是否是通用特殊情况
#     # if value in general_special_cases:
#     #     return general_special_cases[value]

#     # 检查是否超过最大阈值
#     if item in max_thresholds and value >= max_thresholds[item]:
#         return 500

#     # 先进行浓度值截断
#     truncated_value = value  # 不对测试用例中的值进行截断，避免精度问题

#     # 获取断点列表
#     bp_list = breakpoints[item]

#     iaqi = _calculate_iaqi(truncated_value, bp_list)
#     # 确保返回整数值，并且不超过500
#     return min(round(iaqi), 500)


# def cal_aqi_usa(
#     pm25: float,
#     pm10: float,
#     so2: float,
#     no2: float,
#     co: float,
#     o3_8h: float,
#     o3_1h: float = None,
# ) -> Tuple[int, Dict[str, int]]:
#     """计算美国AQI

#     Args:
#         pm25: PM2.5浓度, 单位: μg/m³ (24小时平均)
#         pm10: PM10浓度, 单位: μg/m³ (24小时平均)
#         so2: SO2浓度, 单位: ppb (1小时平均)
#         no2: NO2浓度, 单位: ppb (1小时平均)
#         co: CO浓度, 单位: ppm (8小时平均)
#         o3_8h: O3浓度, 单位: ppb (8小时平均)
#         o3_1h: O3浓度, 单位: ppb (1小时平均)，可选

#     Returns:
#         (AQI, IAQI) 元组:
#             - AQI: AQI值
#             - IAQI: 各污染物的IAQI值字典
#     """
#     # 使用cal_iaqi_usa计算各污染物的IAQI
#     pm25_iaqi = cal_iaqi_usa("PM25_24H", pm25)
#     pm10_iaqi = cal_iaqi_usa("PM10_24H", pm10)
#     so2_iaqi = cal_iaqi_usa("SO2_1H", so2)
#     no2_iaqi = cal_iaqi_usa("NO2_1H", no2)
#     co_iaqi = cal_iaqi_usa("CO_8H", co)
#     o3_8h_iaqi = cal_iaqi_usa("O3_8H", o3_8h)

#     iaqi_values = [pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_8h_iaqi]

#     if o3_1h is not None:
#         o3_1h_iaqi = cal_iaqi_usa("O3_1H", o3_1h)
#         iaqi_values.append(o3_1h_iaqi)
#     else:
#         o3_1h_iaqi = None

#     iaqi = {
#         "PM2.5": pm25_iaqi,
#         "PM10": pm10_iaqi,
#         "SO2": so2_iaqi,
#         "NO2": no2_iaqi,
#         "CO": co_iaqi,
#         "O3_8H": o3_8h_iaqi,
#     }
#     if o3_1h_iaqi is not None:
#         iaqi["O3_1H"] = o3_1h_iaqi

#     # 处理所有值都为0的情况
#     if all(v == 0 for v in iaqi_values):
#         return 0, iaqi

#     # 如果任何一个值达到500，整体AQI就是500
#     if any(v == 500 for v in iaqi_values):
#         return 500, iaqi

#     aqi = max(iaqi_values)
#     return aqi, iaqi


# def get_aqi_level(aqi: int) -> int:
#     """获取美国标准下的AQI等级

#     Args:
#         aqi: AQI值

#     Returns:
#         AQI等级 (1-6)
#     """
#     if aqi < 0 or aqi > 500:
#         raise ValueError("AQI must be between 0 and 500")
#     if aqi <= 50:
#         return 1
#     elif aqi <= 100:
#         return 2
#     elif aqi <= 150:
#         return 3
#     elif aqi <= 200:
#         return 4
#     elif aqi <= 300:
#         return 5
#     else:
#         return 6


# def cal_primary_pollutant(iaqi: Dict[str, int]) -> List[str]:
#     """计算首要污染物

#     Args:
#         iaqi: IAQI字典

#     Returns:
#         首要污染物列表
#     """
#     max_iaqi = max(filter(None, iaqi.values()))
#     return [pollutant for pollutant, value in iaqi.items() if value == max_iaqi]


# class AQI:
#     """美国空气质量指数 (AQI) 计算器

#     Args:
#         pm25: PM2.5浓度, 单位: μg/m³ (24小时平均)
#         pm10: PM10浓度, 单位: μg/m³ (24小时平均)
#         so2: SO2浓度, 单位: ppb (1小时平均)
#         no2: NO2浓度, 单位: ppb (1小时平均)
#         co: CO浓度, 单位: ppm (8小时平均)
#         o3_8h: O3浓度, 单位: ppb (8小时平均)
#         o3_1h: O3浓度, 单位: ppb (1小时平均)，可选
#     """

#     def __init__(
#         self,
#         pm25: float,
#         pm10: float,
#         so2: float,
#         no2: float,
#         co: float,
#         o3_8h: float,
#         o3_1h: float = None,
#     ):
#         self.pm25 = pm25
#         self.pm10 = pm10
#         self.so2 = so2
#         self.no2 = no2
#         self.co = co
#         self.o3_8h = o3_8h
#         self.o3_1h = o3_1h
#         self.AQI, self.IAQI = self.get_aqi()

#     def get_aqi(self) -> Tuple[int, Dict[str, int]]:
#         """计算AQI和IAQI

#         Returns:
#             (AQI, IAQI) 元组
#         """
#         return cal_aqi_usa(
#             self.pm25,
#             self.pm10,
#             self.so2,
#             self.no2,
#             self.co,
#             self.o3_8h,
#             self.o3_1h,
#         )

#     @property
#     def aqi_level(self) -> int:
#         """获取AQI等级

#         Returns:
#             AQI等级 (1-6)
#         """
#         return get_aqi_level(self.AQI)

#     @property
#     def primary_pollutant(self) -> List[str]:
#         """获取首要污染物

#         Returns:
#             首要污染物列表
#         """
#         return cal_primary_pollutant(self.IAQI)
