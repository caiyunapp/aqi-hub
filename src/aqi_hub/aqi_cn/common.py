"""
AQI_CN 公共常量（仅保留对外导出）
"""

AQI_LEVEL = [1, 2, 3, 4, 5, 6]
POLLUTANT = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
POLLUTANT_CN = ["细颗粒物", "可吸入颗粒物", "二氧化硫", "二氧化氮", "一氧化碳", "臭氧"]
POLLUTANT_MAP = dict(zip(POLLUTANT, POLLUTANT_CN))
