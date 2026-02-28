#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
美国空气质量指数（AQI）计算示例

浓度单位: PM2.5/PM10 μg/m³, SO2/NO2 ppb, CO/O3 ppm

运行: 在项目根目录执行 `uv run python examples/us_example.py`
"""

from aqi_hub.aqi_usa.aqi import (
    AQI,
    cal_aqi_usa,
    cal_iaqi_usa,
    cal_primary_pollutant,
    get_aqi_level,
    get_aqi_level_color,
)


def main() -> None:
    print("=== 美国 AQI 示例 ===\n")

    # 1. AQI 计算
    print("1. AQI 计算")
    aqi, iaqi = cal_aqi_usa(
        pm25=120,
        pm10=180,
        so2_1h=65,
        no2=150,
        co=8,
        o3_8h=0.200,
        so2_24h=None,
        o3_1h=None,
    )
    print("  AQI:", aqi)
    print("  IAQI:", iaqi)

    # 2. 单项 IAQI
    print("\n2. 单项 IAQI")
    pm25_iaqi = cal_iaqi_usa(120, "PM25_24H")
    pm10_iaqi = cal_iaqi_usa(180, "PM10_24H")
    o3_8h_iaqi = cal_iaqi_usa(0.200, "O3_8H")
    so2_24h_iaqi = cal_iaqi_usa(307, "SO2_24H")
    print("  PM25_24H 120 μg/m³ → IAQI =", pm25_iaqi)
    print("  PM10_24H 180 μg/m³ → IAQI =", pm10_iaqi)
    print("  O3_8H 0.200 ppm → IAQI =", o3_8h_iaqi)
    print("  SO2_24H 307 ppb → IAQI =", so2_24h_iaqi)

    # 3. AQI 等级
    print("\n3. AQI 等级 (1–6)")
    aqi_level = get_aqi_level(aqi)
    print("  AQI", aqi, "→ 等级", aqi_level)

    # 4. 等级颜色
    print("\n4. 等级颜色")
    color = get_aqi_level_color(1, "RGB")
    print("  等级 1 RGB:", color)
    color = get_aqi_level_color(5, "RGB_HEX")
    print("  等级 5 (紫) RGB_HEX:", color)

    # 5. 首要污染物
    print("\n5. 首要污染物")
    iaqi_dict = {
        "PM2.5": 150,
        "PM10": 120,
        "SO2": 200,
        "NO2": 100,
        "CO": 50,
        "O3": 300,
    }
    primary = cal_primary_pollutant(iaqi_dict)
    print("  Primary pollutant(s):", primary)

    # 6. AQI 类（一站式）
    print("\n6. AQI 类")
    aqi_obj = AQI(
        pm25=120,
        pm10=180,
        so2_1h=65,
        no2=150,
        co=8,
        o3_8h=0.200,
        so2_24h=None,
        o3_1h=None,
    )
    print("  AQI:", aqi_obj.AQI)
    print("  IAQI:", aqi_obj.IAQI)
    print("  AQI 等级:", aqi_obj.aqi_level)
    print("  首要污染物:", aqi_obj.primary_pollutant)
    print("  等级颜色 RGB:", aqi_obj.aqi_color_rgb)
    print("  等级颜色 RGB_HEX:", aqi_obj.aqi_color_rgb_hex)

    print("\n=== 示例结束 ===")


if __name__ == "__main__":
    main()
