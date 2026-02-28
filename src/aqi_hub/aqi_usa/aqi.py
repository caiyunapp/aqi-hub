"""
AQI_USA 计算模块（Rust 实现）

美国 EPA 空气质量指数计算，由 Rust 通过 aqi_hub._native 提供。
"""

from typing import Dict, List, Optional, Tuple, Union

from aqi_hub._native import (
    cal_aqi_usa as _cal_aqi_usa,
    cal_iaqi_usa as _cal_iaqi_usa,
    cal_primary_pollutant_usa as _cal_primary_pollutant_usa,
    get_aqi_level_color_usa as _get_aqi_level_color_usa,
    get_aqi_level_usa as _get_aqi_level_usa,
)


def cal_iaqi_usa(conc: Union[None, int, float], item: str) -> Union[None, int]:
    """计算单项 IAQI（美国标准）。"""
    c = float(conc) if conc is not None else None
    return _cal_iaqi_usa(c, item=item)


def cal_aqi_usa(
    pm25: float,
    pm10: float,
    so2_1h: float,
    no2: float,
    co: float,
    o3_8h: float,
    so2_24h: Optional[float] = None,
    o3_1h: Optional[float] = None,
) -> Tuple[Optional[int], Dict[str, Optional[int]]]:
    """计算美国 AQI，返回 (AQI, IAQI 字典)。"""
    aqi, iaqi_dict = _cal_aqi_usa(pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h)
    return aqi, dict(iaqi_dict)


def get_aqi_level(aqi: Optional[int]) -> int:
    """获取美国标准 AQI 等级 (1–6)。"""
    if aqi is None:
        raise ValueError("AQI is None")
    return _get_aqi_level_usa(aqi)


def cal_primary_pollutant(iaqi: Dict[str, Optional[int]]) -> List[str]:
    """计算首要污染物（美国：IAQI 最大者）。"""
    return _cal_primary_pollutant_usa(iaqi)


def get_aqi_level_color(
    aqi_level: int, color_type: str
) -> Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]:
    """获取 AQI 等级颜色。color_type: RGB, CMYK, RGB_HEX, CMYK_HEX。"""
    return _get_aqi_level_color_usa(aqi_level, color_type)


class AQI:
    """美国 AQI 计算器（Rust 实现）。"""

    def __init__(
        self,
        pm25: float,
        pm10: float,
        so2_1h: float,
        no2: float,
        co: float,
        o3_8h: float,
        so2_24h: Optional[float] = None,
        o3_1h: Optional[float] = None,
    ):
        self.pm25 = pm25
        self.pm10 = pm10
        self.so2_1h = so2_1h
        self.so2_24h = so2_24h
        self.no2 = no2
        self.co = co
        self.o3_8h = o3_8h
        self.o3_1h = o3_1h
        self.AQI, self.IAQI = cal_aqi_usa(
            pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h
        )

    @property
    def aqi_level(self) -> int:
        return get_aqi_level(self.AQI)

    @property
    def primary_pollutant(self) -> List[str]:
        return cal_primary_pollutant(self.IAQI)

    @property
    def aqi_color_rgb(self) -> Tuple[int, int, int]:
        return get_aqi_level_color(self.aqi_level, "RGB")  # type: ignore[return-value]

    @property
    def aqi_color_cmyk(self) -> Tuple[int, int, int, int]:
        return get_aqi_level_color(self.aqi_level, "CMYK")  # type: ignore[return-value]

    @property
    def aqi_color_rgb_hex(self) -> str:
        return get_aqi_level_color(self.aqi_level, "RGB_HEX")  # type: ignore[return-value]

    @property
    def aqi_color_cmyk_hex(self) -> str:
        return get_aqi_level_color(self.aqi_level, "CMYK_HEX")  # type: ignore[return-value]
