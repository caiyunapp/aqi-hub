#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中国空气质量指数（AQI）计算示例

运行: 在项目根目录执行 `uv run python examples/cn_example.py`
"""

from aqi_hub.aqi_cn.aqi import (
    AQI,
    cal_aqi_cn,
    cal_iaqi_cn,
    cal_primary_pollutant,
    get_aqi_level,
    get_aqi_level_color,
)


def main() -> None:
    print("=== 中国 AQI 示例 ===\n")

    # 1. AQI 计算
    print("1. AQI 计算")
    aqi, iaqi = cal_aqi_cn(
        pm25=45, pm10=80, so2=35, no2=85, co=3, o3=140, data_type="hourly"
    )
    print("  小时值: AQI =", aqi, ", IAQI =", iaqi)

    aqi2, iaqi2 = cal_aqi_cn(
        pm25=120, pm10=180, so2=65, no2=150, co=8, o3=200, data_type="daily"
    )
    print("  日均值: AQI =", aqi2, ", IAQI =", iaqi2)

    # 2. 单项 IAQI
    print("\n2. 单项 IAQI")
    pm25_iaqi = cal_iaqi_cn("PM25_24H", 120)
    pm10_iaqi = cal_iaqi_cn("PM10_24H", 180)
    print("  PM25_24H 120 μg/m³ → IAQI =", pm25_iaqi)
    print("  PM10_24H 180 μg/m³ → IAQI =", pm10_iaqi)

    # 3. AQI 等级
    print("\n3. AQI 等级 (1–6)")
    level = get_aqi_level(120)
    print("  AQI 120 → 等级", level)

    # 4. 等级颜色
    print("\n4. 等级颜色")
    color = get_aqi_level_color(1, "RGB")
    print("  等级 1 RGB:", color)
    color = get_aqi_level_color(3, "RGB_HEX")
    print("  等级 3 RGB_HEX:", color)
    color = get_aqi_level_color(4, "CMYK_HEX")
    print("  等级 4 CMYK_HEX:", color)

    # 5. 首要污染物
    print("\n5. 首要污染物")
    primary = cal_primary_pollutant(iaqi2)
    print("  IAQI 最大时首要污染物:", primary)

    # 6. AQI 类（一站式）
    print("\n6. AQI 类")
    aqi_obj = AQI(
        pm25=120,
        pm10=180,
        so2=65,
        no2=150,
        co=1.0,
        o3=200,
        data_type="daily",
    )
    print("  AQI:", aqi_obj.AQI)
    print("  IAQI:", aqi_obj.IAQI)
    print("  首要污染物:", aqi_obj.primary_pollutant)
    print("  AQI 等级:", aqi_obj.aqi_level)
    print("  等级颜色 RGB:", aqi_obj.aqi_color_rgb)
    print("  等级颜色 RGB_HEX:", aqi_obj.aqi_color_rgb_hex)

    print("\n=== 示例结束 ===")


if __name__ == "__main__":
    main()
