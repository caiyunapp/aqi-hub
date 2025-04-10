"""
美国空气质量指数（AQI）计算示例
"""

# # 1 AQI 计算
# from aqi_hub.aqi_usa.aqi import cal_aqi_usa

# aqi, iaqi = cal_aqi_usa(
#     pm25=120, pm10=180, so2_1h=65, no2=150, co=8, o3_8h=0.200, so2_24h=None, o3_1h=None
# )
# print("aqi:", aqi)
# print("iaqi:", iaqi)

# # 2 IAQI 计算
# from aqi_hub.aqi_usa.aqi import cal_iaqi_usa

# # 2.1 计算 PM2.5 的 IAQI
# pm25_iaqi = cal_iaqi_usa(120, "PM25_24H")
# print(f"PM25_24H IAQI: {pm25_iaqi}")

# # 2.2 计算 PM10 的 IAQI
# pm10_iaqi = cal_iaqi_usa(180, "PM10_24H")
# print(f"PM10_24H IAQI: {pm10_iaqi}")

# # 2.3 计算 SO2 的 IAQI
# so2_1h_iaqi = cal_iaqi_usa(65, "SO2_1H")
# print(f"SO2_1H IAQI: {so2_1h_iaqi}")
# so2_24h_iaqi = cal_iaqi_usa(307, "SO2_24H")
# print(f"SO2_24H IAQI: {so2_24h_iaqi}")

# # 2.4 计算 NO2 的 IAQI
# no2_iaqi = cal_iaqi_usa(150, "NO2_1H")
# print(f"NO2_1H IAQI: {no2_iaqi}")

# # 2.5 计算 CO 的 IAQI
# co_iaqi = cal_iaqi_usa(8, "CO_8H")
# print(f"CO_8H IAQI: {co_iaqi}")

# # 2.6 计算 O3 的 IAQI
# o3_8h_iaqi = cal_iaqi_usa(0.200, "O3_8H")
# print(f"O3_8H IAQI: {o3_8h_iaqi}")
# o3_1h_iaqi = cal_iaqi_usa(0.200, "O3_1H")
# print(f"O3_1H IAQI: {o3_1h_iaqi}")

# # 3 AQI 等级
# from aqi_hub.aqi_usa.aqi import get_aqi_level

# aqi_level = get_aqi_level(200)
# print(f"AQI: {aqi_level}")

# # 4 空气质量等级颜色
# from aqi_hub.aqi_usa.aqi import get_aqi_level_color

# color = get_aqi_level_color(1, "RGB")
# print(f"Color: {color}")

# color = get_aqi_level_color(2, "CMYK")
# print(f"Color: {color}")

# color = get_aqi_level_color(3, "RGB_HEX")
# print(f"Color: {color}")

# color = get_aqi_level_color(4, "CMYK_HEX")
# print(f"Color: {color}")

# # 5 污染物计算
# from aqi_hub.aqi_usa.aqi import cal_primary_pollutant

# iaqi = {
#     "PM2.5": 150,
#     "PM10": 120,
#     "SO2": 200,
#     "NO2": 100,
#     "CO": 50,
#     "O3": 300,
# }
# primary_pollutant = cal_primary_pollutant(iaqi)
# print(f"Primary Pollutant: {primary_pollutant}")

# # 6 AQI 类

# from aqi_hub.aqi_usa.aqi import AQI

# aqi = AQI(
#     pm25=120,
#     pm10=180,
#     so2_1h=65,
#     no2=150,
#     co=8,
#     o3_8h=0.200,
#     so2_24h=None,
#     o3_1h=None,
# )
# print("aqi:", aqi.AQI)
# print("iaqi:", aqi.IAQI)
# print("aqi_level:", aqi.aqi_level)
# print("primary_pollutant", aqi.primary_pollutant)
# print("aqi_color_rgb:", aqi.aqi_color_rgb)
# print("aqi_color_cmyk:", aqi.aqi_color_cmyk)
# print("aqi_color_rgb_hex:", aqi.aqi_color_rgb_hex)
# print("aqi_color_cmyk_hex:", aqi.aqi_color_cmyk_hex)
