#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中国空气质量指数（AQI）计算示例
"""

# # 1 AQI 计算
# from aqi_hub.aqi_cn.aqi import cal_aqi_cn

# # 1.1 计算小时值 AQI
# aqi, iaqi = cal_aqi_cn(
#     pm25=45, pm10=80, so2=35, no2=85, co=3, o3=140, data_type="hourly"
# )
# print("测试数据 1:")
# print(f"AQI: {aqi}")
# print(f"IAQI: {iaqi}")

# # 1.2 计算日均值 AQI
# aqi, iaqi = cal_aqi_cn(
#     pm25=120, pm10=180, so2=65, no2=150, co=8, o3=200, data_type="daily"
# )
# print("\n测试数据 2:")
# print(f"AQI: {aqi}")
# print(f"IAQI: {iaqi}")

# # 2 IAQI 计算

# from aqi_hub.aqi_cn.aqi import cal_iaqi_cn

# # 2.1 计算 PM2.5 的 IAQI
# pm25_iaqi = cal_iaqi_cn("PM25_24H", 120)
# print(f"PM25_24H IAQI: {pm25_iaqi}")

# # 2.2 计算 PM10 的 IAQI
# pm10_iaqi = cal_iaqi_cn("PM10_24H", 180)
# print(f"PM10_24H IAQI: {pm10_iaqi}")


# # 3 空气质量等级
# from aqi_hub.aqi_cn.aqi import get_aqi_level

# # 3.1 计算 AQI
# level = get_aqi_level(120)
# print(f"AQI 等级: {level}")


# # 4 空气质量等级颜色
# from aqi_hub.aqi_cn.aqi import get_aqi_level_color

# # 4.1 计算 AQI 等级颜色
# color = get_aqi_level_color(1, "RGB")
# print(f"AQI 等级颜色: {color}")

# # 4.2 计算 AQI 等级颜色
# color = get_aqi_level_color(2, "CMYK")
# print(f"AQI 等级颜色: {color}")

# # 4.3 计算 AQI 等级颜色
# color = get_aqi_level_color(3, "RGB_HEX")
# print(f"AQI 等级颜色: {color}")

# # 4.4 计算 AQI 等级颜色
# color = get_aqi_level_color(4, "CMYK_HEX")
# print(f"AQI 等级颜色: {color}")

# # 5 主要污染物
# from aqi_hub.aqi_cn.aqi import cal_primary_pollutant

# # 5.1 计算首要污染物
# iaqi = {
#     "PM2.5": 120,
#     "PM10": 180,
#     "SO2": 65,
#     "NO2": 150,
#     "CO": 8,
#     "O3": 200,
# }
# primary_pollutant = cal_primary_pollutant(iaqi)
# print(f"首要污染物: {primary_pollutant}")

# # 6 AQI 类

# from aqi_hub.aqi_cn.aqi import AQI

# data_type = "hourly"
# # or
# data_type = "daily"

# aqi_obj = AQI(
#     pm25=120,
#     pm10=180,
#     so2=65,
#     no2=150,
#     co=1.0,
#     o3=200,
#     data_type=data_type,
# )
# print(f"AQI: {aqi_obj.AQI}")
# print(f"IAQI: {aqi_obj.IAQI}")
# print(f"主要污染物: {aqi_obj.primary_pollutant}")
# print(f"AQI 等级: {aqi_obj.aqi_level}")
# print(f"AQI 等级颜色 (RGB): {aqi_obj.aqi_color_rgb}")
# print(f"AQI 等级颜色 (CMYK): {aqi_obj.aqi_color_cmyk}")
# print(f"AQI 等级颜色 (RGB_HEX): {aqi_obj.aqi_color_rgb_hex}")
# print(f"AQI 等级颜色 (CMYK_HEX): {aqi_obj.aqi_color_cmyk_hex}")

# """
# AQI: 158
# IAQI: {'PM2.5': 158, 'PM10': 115, 'SO2': 22, 'NO2': 135, 'CO': 25, 'O3': 137}
# 首要污染物: ['PM2.5']
# AQI 等级: 4
# AQI 等级颜色 (RGB): (255, 0, 0)
# AQI 等级颜色 (CMYK): (0, 100, 100, 0)
# AQI 等级颜色 (RGB_HEX): #FF0000
# AQI 等级颜色 (CMYK_HEX): #FF0000
# """
