#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中国空气质量指数（AQI）计算示例
"""

from aqi_hub.aqi_cn.aqi import cal_aqi_cn_daily, cal_aqi_cn_hourly, cal_iaqi_cn


def main():
    # 计算单项污染物的 IAQI (Individual Air Quality Index)
    # 1小时值
    pm25_1h_iaqi = cal_iaqi_cn("PM25_1H", 35)  # PM2.5: 35 μg/m³
    pm10_1h_iaqi = cal_iaqi_cn("PM10_1H", 80)  # PM10: 80 μg/m³
    o3_1h_iaqi = cal_iaqi_cn("O3_1H", 120)  # O3: 120 μg/m³
    co_1h_iaqi = cal_iaqi_cn("CO_1H", 1.5)  # CO: 1.5 mg/m³
    no2_1h_iaqi = cal_iaqi_cn("NO2_1H", 40)  # NO2: 40 μg/m³
    so2_1h_iaqi = cal_iaqi_cn("SO2_1H", 30)  # SO2: 30 μg/m³

    # 24小时值
    pm25_24h_iaqi = cal_iaqi_cn("PM25_24H", 35)  # PM2.5: 35 μg/m³
    pm10_24h_iaqi = cal_iaqi_cn("PM10_24H", 80)  # PM10: 80 μg/m³
    o3_8h_iaqi = cal_iaqi_cn("O3_8H", 120)  # O3: 120 μg/m³（8小时滑动平均）
    co_24h_iaqi = cal_iaqi_cn("CO_24H", 1.5)  # CO: 1.5 mg/m³
    no2_24h_iaqi = cal_iaqi_cn("NO2_24H", 40)  # NO2: 40 μg/m³
    so2_24h_iaqi = cal_iaqi_cn("SO2_24H", 30)  # SO2: 30 μg/m³

    print("\n单项污染物 IAQI 计算结果（1小时值）：")
    print(f"PM2.5 IAQI: {pm25_1h_iaqi}")
    print(f"PM10 IAQI: {pm10_1h_iaqi}")
    print(f"O3 IAQI: {o3_1h_iaqi}")
    print(f"CO IAQI: {co_1h_iaqi}")
    print(f"NO2 IAQI: {no2_1h_iaqi}")
    print(f"SO2 IAQI: {so2_1h_iaqi}")

    print("\n单项污染物 IAQI 计算结果（24小时值）：")
    print(f"PM2.5 IAQI: {pm25_24h_iaqi}")
    print(f"PM10 IAQI: {pm10_24h_iaqi}")
    print(f"O3(8h) IAQI: {o3_8h_iaqi}")
    print(f"CO IAQI: {co_24h_iaqi}")
    print(f"NO2 IAQI: {no2_24h_iaqi}")
    print(f"SO2 IAQI: {so2_24h_iaqi}")

    # 准备污染物数据（1小时值）
    pm25_1h = 35  # μg/m³
    pm10_1h = 80  # μg/m³
    o3_1h = 120  # μg/m³
    co_1h = 1.5  # mg/m³
    no2_1h = 40  # μg/m³
    so2_1h = 30  # μg/m³

    # 准备污染物数据（24小时值）
    pm25_24h = 35  # μg/m³
    pm10_24h = 80  # μg/m³
    o3_8h = 120  # μg/m³
    co_24h = 1.5  # mg/m³
    no2_24h = 40  # μg/m³
    so2_24h = 30  # μg/m³

    # 计算小时 AQI
    hourly_aqi, hourly_primary = cal_aqi_cn_hourly(
        pm25=pm25_1h, pm10=pm10_1h, so2=so2_1h, no2=no2_1h, co=co_1h, o3=o3_1h
    )

    print("\n小时 AQI 计算结果：")
    print(f"AQI: {hourly_aqi}")
    print(f"主要污染物: {hourly_primary}")

    # 计算日均值 AQI
    daily_aqi, daily_primary = cal_aqi_cn_daily(
        pm25=pm25_24h, pm10=pm10_24h, so2=so2_24h, no2=no2_24h, co=co_24h, o3=o3_8h
    )

    print("\n日均值 AQI 计算结果：")
    print(f"AQI: {daily_aqi}")
    print(f"主要污染物: {daily_primary}")


if __name__ == "__main__":
    main()
