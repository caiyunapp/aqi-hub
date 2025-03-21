# AQI Hub

![AQI Hub Cover](docs/cover.jpeg)

AQI 计算，以及分指数计算  

## 计算方法

### AQI (CN)

计算方法参照中华人民共和国生态环境部标准： [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)

#### AQI 等级说明

| AQI 范围   | 指数级别 | 类别     | 颜色   |
| ---------- | -------- | -------- | ------ |
| 0 至 50    | 一级     | 优       | 绿色   |
| 51 至 100  | 二级     | 良       | 黄色   |
| 101 至 150 | 三级     | 轻度污染 | 橙色   |
| 151 至 200 | 四级     | 中度污染 | 红色   |
| 201 至 300 | 五级     | 重度污染 | 紫色   |
| 301+       | 六级     | 严重污染 | 褐红色 |

#### AQI 颜色标准（中国）

| RGB 颜色                                                          | R   | G   | B   | RGB HEX | CMYK 颜色                                                                   | C   | M   | Y   | K   | CMYK HEX |
| ----------------------------------------------------------------- | --- | --- | --- | ------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | -------- |
| ![绿色](https://img.shields.io/badge/绿色-0_228_0-%2300E400)      | 0   | 228 | 0   | #00E400 | ![绿色 CMYK](https://img.shields.io/badge/绿色-40_0_100_0-%2399FF00)        | 40  | 0   | 100 | 0   | #99FF00  |
| ![黄色](https://img.shields.io/badge/黄色-255_255_0-%23FFFF00)    | 255 | 255 | 0   | #FFFF00 | ![黄色 CMYK](https://img.shields.io/badge/黄色-0_0_100_0-%23FFFF00)         | 0   | 0   | 100 | 0   | #FFFF00  |
| ![橙色](https://img.shields.io/badge/橙色-255_126_0-%23FF7E00)    | 255 | 126 | 0   | #FF7E00 | ![橙色 CMYK](https://img.shields.io/badge/橙色-0_52_100_0-%23FF7A00)        | 0   | 52  | 100 | 0   | #FF7A00  |
| ![红色](https://img.shields.io/badge/红色-255_0_0-%23FF0000)      | 255 | 0   | 0   | #FF0000 | ![红色 CMYK](https://img.shields.io/badge/红色-0_100_100_0-%23FF0000)       | 0   | 100 | 100 | 0   | #FF0000  |
| ![紫色](https://img.shields.io/badge/紫色-153_0_76-%2399004C)     | 153 | 0   | 76  | #99004C | ![紫色 CMYK](https://img.shields.io/badge/紫色-10_100_40_30-%23A0006B)      | 10  | 100 | 40  | 30  | #A0006B  |
| ![褐红色](https://img.shields.io/badge/褐红色-126_0_35-%237E0023) | 126 | 0   | 35  | #7E0023 | ![褐红色 CMYK](https://img.shields.io/badge/褐红色-30_100_100_30-%237C0000) | 30  | 100 | 100 | 30  | #7C0000  |

### AQI (USA)

计算方法参考 US EPA: [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)

#### AQI Range

| AQI Range  | Descriptor                     | Color  |
| ---------- | ------------------------------ | ------ |
| 0 to 50    | Good                           | Green  |
| 51 to 100  | Moderate                       | Yellow |
| 101 to 150 | Unhealthy for Sensitive Groups | Orange |
| 151 to 200 | Unhealthy                      | Red    |
| 201 to 300 | Very Unhealthy                 | Purple |
| 301+       | Hazardous                      | Maroon |

#### AQI Color

| RGB Color                                                           | R   | G   | B   | RGB HEX | CMYK Color                                                                  | C   | M   | Y   | K   | CMYK HEX |
| ------------------------------------------------------------------- | --- | --- | --- | ------- | --------------------------------------------------------------------------- | --- | --- | --- | --- | -------- |
| ![Green](https://img.shields.io/badge/Green-0_228_0-%2300E400)      | 0   | 228 | 0   | #00E400 | ![Green CMYK](https://img.shields.io/badge/Green-40_0_100_0-%2399FF00)      | 40  | 0   | 100 | 0   | #99FF00  |
| ![Yellow](https://img.shields.io/badge/Yellow-255_255_0-%23FFFF00)  | 255 | 255 | 0   | #FFFF00 | ![Yellow CMYK](https://img.shields.io/badge/Yellow-0_0_100_0-%23FFFF00)     | 0   | 0   | 100 | 0   | #FFFF00  |
| ![Orange](https://img.shields.io/badge/Orange-255_126_0-%23FF7E00)  | 255 | 126 | 0   | #FF7E00 | ![Orange CMYK](https://img.shields.io/badge/Orange-0_52_100_0-%23FF7A00)    | 0   | 52  | 100 | 0   | #FF7A00  |
| ![Red](https://img.shields.io/badge/Red-255_0_0-%23FF0000)          | 255 | 0   | 0   | #FF0000 | ![Red CMYK](https://img.shields.io/badge/Red-0_100_100_0-%23FF0000)         | 0   | 100 | 100 | 0   | #FF0000  |
| ![Purple](https://img.shields.io/badge/Purple-143_63_151-%238F3F97) | 143 | 63  | 151 | #8F3F97 | ![Purple CMYK](https://img.shields.io/badge/Purple-5_58_0_41-%238F3F96)     | 5   | 58  | 0   | 41  | #8F3F96  |
| ![Maroon](https://img.shields.io/badge/Maroon-126_0_35-%237E0023)   | 126 | 0   | 35  | #7E0023 | ![Maroon CMYK](https://img.shields.io/badge/Maroon-30_100_100_30-%237D0000) | 30  | 100 | 100 | 30  | #7D0000  |

## 使用方法

### 安装

```bash
pip install aqi-hub
```

### 中国 AQI 计算

#### 1 AQI 计算

```python
from aqi_hub.aqi_cn.aqi import cal_aqi_cn

# 1.1 计算小时值 AQI
aqi, iaqi = cal_aqi_cn(
    pm25=45, pm10=80, so2=35, no2=85, co=3, o3=140, data_type="hourly"
)
print("测试数据 1:")
print(f"AQI: {aqi}")
print(f"IAQI: {iaqi}")

# 1.2 计算日均值 AQI
aqi, iaqi = cal_aqi_cn(
    pm25=120, pm10=180, so2=65, no2=150, co=8, o3=200, data_type="daily"
)
print("\n测试数据 2:")
print(f"AQI: {aqi}")
print(f"IAQI: {iaqi}")

```

#### 2 IAQI 计算

```python
from aqi_hub.aqi_cn.aqi import cal_iaqi_cn

# 2.1 计算 PM2.5 的 IAQI
pm25_iaqi = cal_iaqi_cn("PM25_24H", 120)
print(f"PM25_24H IAQI: {pm25_iaqi}")

# 2.2 计算 PM10 的 IAQI
pm10_iaqi = cal_iaqi_cn("PM10_24H", 180)
print(f"PM10_24H IAQI: {pm10_iaqi}")

```

#### 3 空气质量等级

```python
from aqi_hub.aqi_cn.aqi import get_aqi_level

# 3.1 计算 AQI
level = get_aqi_level(120)
print(f"AQI 等级: {level}")

```

#### 4 空气质量等级颜色

```python
from aqi_hub.aqi_cn.aqi import get_aqi_level_color

# 4.1 计算 AQI 等级颜色
color = get_aqi_level_color(1, "RGB")
print(f"AQI 等级颜色: {color}")

# 4.2 计算 AQI 等级颜色
color = get_aqi_level_color(2, "CMYK")
print(f"AQI 等级颜色: {color}")

# 4.3 计算 AQI 等级颜色
color = get_aqi_level_color(3, "RGB_HEX")
print(f"AQI 等级颜色: {color}")

# 4.4 计算 AQI 等级颜色
color = get_aqi_level_color(4, "CMYK_HEX")
print(f"AQI 等级颜色: {color}")

```

#### 5 污染物计算

```python
from aqi_hub.aqi_cn.aqi import cal_primary_pollutant, cal_exceed_pollutant

# 5.1 计算主要污染物
iaqi = {
    "PM25": 120,
    "PM10": 180,
    "SO2": 65,
    "NO2": 150,
    "CO": 8,
    "O3": 200,
}
primary_pollutant = cal_primary_pollutant(iaqi)
print(f"主要污染物: {primary_pollutant}")

# 5.2 计算超标污染物
exceed_pollutant = cal_exceed_pollutant(iaqi)
print(f"超标污染物: {exceed_pollutant}")

```

### 美国 AQI 计算

```python

```

### 返回值说明

### 支持的污染物

| 污染物 | 中国标准单位 | 美国标准单位 | 单位换算（25℃，1标准大气压） |
|--------|--------------|--------------|------------------------------|
| PM2.5  | μg/m³       | μg/m³       | 相同                         |
| PM10   | μg/m³       | μg/m³       | 相同                         |
| O3     | μg/m³       | ppb         | 1 ppb = 1.962 μg/m³         |
| CO     | mg/m³       | ppm         | 1 ppm = 1.145 mg/m³         |
| NO2    | μg/m³       | ppb         | 1 ppb = 1.88 μg/m³          |
| SO2    | μg/m³       | ppb         | 1 ppb = 2.62 μg/m³          |

## 参考文献

1. [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)
2. [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
