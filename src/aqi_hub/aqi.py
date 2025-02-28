import math
from typing import Optional, Union

# 分段标准，格式为列表 [(BP_lo, BP_hi, IAQI_lo, IAQI_hi)
# 定义 PM2.5 的分段标准
pm25_breakpoints = [
    (0, 35, 0, 50),  # 优
    (35, 75, 50, 100),  # 良
    (75, 115, 100, 150),  # 轻度污染
    (115, 150, 150, 200),  # 中度污染
    (150, 250, 200, 300),  # 重度污染
    (250, 350, 300, 400),  # 严重污染
    (350, 500, 400, 500),  # 极度污染
]
# 定义 PM10 的分段标准
pm10_breakpoints = [
    (0, 50, 0, 50),  # 优
    (50, 150, 50, 100),  # 良
    (150, 250, 100, 150),  # 轻度污染
    (250, 350, 150, 200),  # 中度污染
    (350, 420, 200, 300),  # 重度污染
    (420, 500, 300, 400),  # 严重污染
    (500, 600, 400, 500),  # 极度污染
]
# 定义 SO2 的分段标准
so2_24h_breakpoints = [
    (0, 150, 0, 50),  # 优
    (150, 500, 50, 100),  # 良
    (500, 650, 100, 150),  # 轻度污染
    (650, 800, 150, 200),  # 中度污染
    (800, 1600, 200, 300),  # 重度污染
    (1600, 2100, 300, 400),  # 严重污染
    (2100, 2620, 400, 500),  # 极度污染
]
so2_1h_breakpoints = [
    (0, 150, 0, 50),  # 优
    (150, 500, 50, 100),  # 良
    (500, 650, 100, 150),  # 轻度污染
    (650, 800, 150, 200),  # 中度污染
]
# 定义 NO2 的分段标准
no2_24h_breakpoints = [
    (0, 40, 0, 50),  # 优
    (40, 80, 50, 100),  # 良
    (80, 180, 100, 150),  # 轻度污染
    (180, 280, 150, 200),  # 中度污染
    (280, 565, 200, 300),  # 重度污染
    (565, 750, 300, 400),  # 严重污染
    (750, 940, 400, 500),  # 极度污染
]
no2_1h_breakpoints = [
    (0, 100, 0, 50),
    (100, 200, 50, 100),
    (200, 700, 100, 150),
    (700, 1200, 150, 200),
    (1200, 2340, 200, 300),
    (2340, 3090, 300, 400),
    (3090, 3840, 400, 500),
]
# 定义 CO 的分段标准
co_1h_breakpoints = [
    (0, 5, 0, 50),  # 优
    (5, 10, 50, 100),  # 良
    (10, 35, 100, 150),  # 轻度污染
    (35, 60, 150, 200),  # 中度污染
    (60, 90, 200, 300),  # 重度污染
    (90, 120, 300, 400),  # 严重污染
    (120, 150, 400, 500),  # 极度污染
]
co_24h_breakpoints = [
    (0, 2, 0, 50),  # 优
    (2, 4, 50, 100),  # 良
    (4, 14, 100, 150),  # 轻度污染
    (14, 24, 150, 200),  # 中度污染
    (24, 36, 200, 300),  # 重度污染
    (36, 48, 300, 400),  # 严重污染
    (48, 60, 400, 500),  # 极度污染
]
# 定义 O3 的分段标准
# 臭氧 1小时 IAQI 分段标准
o3_1hr_breakpoints = [
    (0, 160, 0, 50),
    (160, 200, 50, 100),
    (200, 300, 100, 150),
    (300, 400, 150, 200),
    (400, 800, 200, 300),
    (800, 1000, 300, 400),
    (1000, 1200, 400, 500),
]

# 臭氧 8小时滑动平均 IAQI 分段标准
o3_8hr_breakpoints = [
    (0, 100, 0, 50),
    (100, 160, 50, 100),
    (160, 215, 100, 150),
    (215, 265, 150, 200),
    (265, 800, 200, 300),
]
breakpoints = {
    "PM25_24H": pm25_breakpoints,
    "PM25_1H": pm25_breakpoints,
    "PM10_24H": pm10_breakpoints,
    "PM10_1H": pm10_breakpoints,
    "SO2_24H": so2_24h_breakpoints,
    "SO2_1H": so2_1h_breakpoints,
    "NO2_24H": no2_24h_breakpoints,
    "NO2_1H": no2_1h_breakpoints,
    "CO_24H": co_24h_breakpoints,
    "CO_1H": co_1h_breakpoints,
    "O3_8H": o3_8hr_breakpoints,
    "O3_1H": o3_1hr_breakpoints,
}


def _calculate_iaqi(concentration, breakpoints) -> float:
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

    https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf
    http://sthjj.wuhai.gov.cn/sthjj/1115793/1115792/hbxw/1195969/index.html
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


if __name__ == "__main__":
    print(cal_iaqi_cn("PM25_24H", 35))
    print(cal_iaqi_cn("PM25_1H", 501))
    print(cal_iaqi_cn("O3_8H", 801))
