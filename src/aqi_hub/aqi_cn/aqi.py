"""
空气质量指数 (AQI) 计算模块（Rust 实现）

本模块基于中国环境空气质量标准 (GB 3095-2026, HJ 633-2026) 计算 AQI。
实现由 Rust 提供，通过 aqi_hub._native 调用。
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from aqi_hub._native import (
    cal_aqi_cn as _cal_aqi_cn,
    cal_iaqi_cn as _cal_iaqi_cn,
    cal_primary_pollutant_cn as _cal_primary_pollutant_cn,
    get_aqi_level_cn as _get_aqi_level_cn,
    get_aqi_level_color_cn as _get_aqi_level_color_cn,
)

from .common import POLLUTANT_MAP


def _opt_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    raise TypeError("value must be int, float or None")


def cal_iaqi_cn(item: str, value: Union[int, float, None]) -> Optional[int]:
    """计算单项污染物的 IAQI（中国标准）。"""
    if value is None:
        return _cal_iaqi_cn(item, None)
    return _cal_iaqi_cn(item, _opt_float(value))


def cal_aqi_cn(
    pm25: Union[float, int, None],
    pm10: Union[float, int, None],
    so2: Union[float, int, None],
    no2: Union[float, int, None],
    co: Union[float, int, None],
    o3: Union[float, int, None],
    data_type: str = "hourly",
) -> Tuple[Optional[int], Dict[str, Optional[int]]]:
    """计算 AQI（中国），返回 (AQI, IAQI 字典)。"""
    if data_type not in ("hourly", "daily"):
        raise ValueError("data_type must be 'hourly' or 'daily'")
    aqi, iaqi_dict = _cal_aqi_cn(
        _opt_float(pm25) if pm25 is not None else None,
        _opt_float(pm10) if pm10 is not None else None,
        _opt_float(so2) if so2 is not None else None,
        _opt_float(no2) if no2 is not None else None,
        _opt_float(co) if co is not None else None,
        _opt_float(o3) if o3 is not None else None,
        data_type,
    )
    return aqi, dict(iaqi_dict)


def cal_primary_pollutant(iaqi: Dict[str, Optional[int]]) -> List[str]:
    """计算首要污染物（中国：IAQI > 50 且等于最大值）。"""
    return _cal_primary_pollutant_cn(iaqi)


def get_aqi_level(aqi: Union[int, None]) -> Union[int, None]:
    """获取中国标准 AQI 等级 (1–6)。"""
    return _get_aqi_level_cn(aqi)


def get_aqi_level_color(
    aqi_level: int, color_type: str
) -> Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]:
    """获取 AQI 等级对应颜色。color_type: RGB, CMYK, RGB_HEX, CMYK_HEX。"""
    return _get_aqi_level_color_cn(aqi_level, color_type)


class AQI:
    """中国 AQI 计算器（Rust 实现）。"""

    def __init__(
        self,
        pm25: Union[float, int, None],
        pm10: Union[float, int, None],
        so2: Union[float, int, None],
        no2: Union[float, int, None],
        co: Union[float, int, None],
        o3: Union[float, int, None],
        data_type: str,
    ):
        if data_type not in ("hourly", "daily"):
            raise ValueError("data_type must be 'hourly' or 'daily'")
        self.pm25 = pm25
        self.pm10 = pm10
        self.so2 = so2
        self.no2 = no2
        self.co = co
        self.o3 = o3
        self.data_type = data_type
        self.AQI, self.IAQI = cal_aqi_cn(pm25, pm10, so2, no2, co, o3, data_type)

    @property
    def aqi_level(self) -> Optional[int]:
        return get_aqi_level(self.AQI)

    def _color(self, color_type: str) -> Any:
        if self.aqi_level is None:
            raise ValueError("AQI is None, cannot get color")
        return get_aqi_level_color(self.aqi_level, color_type)

    @property
    def aqi_color_rgb(self) -> Tuple[int, int, int]:
        return self._color("RGB")  # type: ignore[return-value]

    @property
    def aqi_color_cmyk(self) -> Tuple[int, int, int, int]:
        return self._color("CMYK")  # type: ignore[return-value]

    @property
    def aqi_color_rgb_hex(self) -> str:
        return self._color("RGB_HEX")  # type: ignore[return-value]

    @property
    def aqi_color_cmyk_hex(self) -> str:
        return self._color("CMYK_HEX")  # type: ignore[return-value]

    @property
    def primary_pollutant(self) -> List[str]:
        return cal_primary_pollutant(self.IAQI)

    @property
    def primary_pollutant_cn(self) -> List[str]:
        return [POLLUTANT_MAP[item] for item in self.primary_pollutant]
