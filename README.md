# AQI Hub

![AQI Hub Cover](docs/cover.jpeg)

aqi 计算，以及分指数计算  

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

```python
from aqi_hub.aqi_cn import cal_iaqi, cal_aqi

# 计算单项污染物的 IAQI (Individual Air Quality Index)
pm25_iaqi = cal_iaqi('pm2.5', 35)    # PM2.5: 35 μg/m³
pm10_iaqi = cal_iaqi('pm10', 80)     # PM10: 80 μg/m³
o3_iaqi = cal_iaqi('o3', 120)        # O3: 120 μg/m³
co_iaqi = cal_iaqi('co', 1.5)        # CO: 1.5 mg/m³
no2_iaqi = cal_iaqi('no2', 40)       # NO2: 40 μg/m³
so2_iaqi = cal_iaqi('so2', 30)       # SO2: 30 μg/m³

print(f"PM2.5 IAQI: {pm25_iaqi}")  # 示例输出：PM2.5 IAQI: 50
print(f"PM10 IAQI: {pm10_iaqi}")   # 示例输出：PM10 IAQI: 57
print(f"O3 IAQI: {o3_iaqi}")       # 示例输出：O3 IAQI: 75

# 计算总体 AQI（取各项污染物 IAQI 的最大值）
pollutants = {
    'pm2.5': 35,    # μg/m³
    'pm10': 80,     # μg/m³
    'o3': 120,      # μg/m³
    'co': 1.5,      # mg/m³
    'no2': 40,      # μg/m³
    'so2': 30       # μg/m³
}
aqi_result = cal_aqi(pollutants)
print(f"AQI: {aqi_result['aqi']}")                 # AQI 值
print(f"主要污染物: {aqi_result['primary']}")      # 主要污染物
print(f"空气质量等级: {aqi_result['level']}")      # 空气质量等级
print(f"空气质量类别: {aqi_result['category']}")   # 空气质量类别
print(f"颜色: {aqi_result['color']}")             # 对应的颜色（RGB HEX）
```

### 美国 AQI 计算

```python
from aqi_hub.aqi_usa import cal_iaqi, cal_aqi

# 计算单项污染物的 AQI
pm25_aqi = cal_iaqi('pm2.5', 35)     # PM2.5: 35 μg/m³（与中国单位相同）
pm10_aqi = cal_iaqi('pm10', 80)      # PM10: 80 μg/m³（与中国单位相同）
o3_aqi = cal_iaqi('o3', 60)          # O3: 60 ppb（约等于 117.72 μg/m³）
co_aqi = cal_iaqi('co', 1.3)         # CO: 1.3 ppm（约等于 1.49 mg/m³）
no2_aqi = cal_iaqi('no2', 53)        # NO2: 53 ppb（约等于 99.64 μg/m³）
so2_aqi = cal_iaqi('so2', 30)        # SO2: 30 ppb（约等于 78.6 μg/m³）

print(f"PM2.5 AQI: {pm25_aqi}")  # 示例输出：PM2.5 AQI: 99
print(f"PM10 AQI: {pm10_aqi}")   # 示例输出：PM10 AQI: 60
print(f"O3 AQI: {o3_aqi}")       # 示例输出：O3 AQI: 84

# 计算总体 AQI（取各项污染物 AQI 的最大值）
pollutants = {
    'pm2.5': 35,     # μg/m³
    'pm10': 80,      # μg/m³
    'o3': 60,        # ppb
    'co': 1.3,       # ppm
    'no2': 53,       # ppb
    'so2': 30        # ppb
}
aqi_result = cal_aqi(pollutants)
print(f"AQI: {aqi_result['aqi']}")                    # AQI 值
print(f"主要污染物: {aqi_result['primary']}")         # 主要污染物
print(f"空气质量描述: {aqi_result['descriptor']}")    # 空气质量描述
print(f"颜色: {aqi_result['color']}")                # 对应的颜色（RGB HEX）
```

### 返回值说明

#### 中国标准 (cal_aqi_cn)

返回一个字典，包含以下字段：  
- `aqi`: AQI 值（整数）
- `primary`: 主要污染物
- `level`: 空气质量等级（一级~六级）
- `category`: 空气质量类别（优、良、轻度污染等）
- `color`: 对应的颜色代码（RGB HEX）

#### 美国标准 (cal_aqi_us)

返回一个字典，包含以下字段：  
- `aqi`: AQI 值（整数）
- `primary`: 主要污染物
- `descriptor`: 空气质量描述（Good、Moderate 等）
- `color`: 对应的颜色代码（RGB HEX）

### 支持的污染物

中国标准支持的污染物及单位：
- PM2.5 (μg/m³)
- PM10 (μg/m³)
- O3 (μg/m³)
- CO (mg/m³)
- NO2 (μg/m³)
- SO2 (μg/m³)

美国标准支持的污染物及单位：
- PM2.5 (μg/m³) - 与中国相同
- PM10 (μg/m³) - 与中国相同
- O3 (ppb) - 中国使用 μg/m³，需要转换
- CO (ppm) - 中国使用 mg/m³，需要转换
- NO2 (ppb) - 中国使用 μg/m³，需要转换
- SO2 (ppb) - 中国使用 μg/m³，需要转换

单位换算参考（25℃，1标准大气压）：
- O3: 1 ppb = 1.962 μg/m³
- CO: 1 ppm = 1.145 mg/m³
- NO2: 1 ppb = 1.88 μg/m³
- SO2: 1 ppb = 2.62 μg/m³

## 参考文献

1. [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)
2. [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
