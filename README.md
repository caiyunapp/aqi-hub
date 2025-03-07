# AQI Hub

![AQI Hub Cover](docs/cover.png)

aqi 计算，以及分指数计算  
目前仅支持中国 aqi 计算。

## 计算方法

### AQI (CN)

计算方法参照中华人民共和国生态环境部标准： [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)

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

| Color   | R   | G   | B   | HEX     | C   | M   | Y   | K   |
|---------|-----|-----|-----|---------|-----|-----|-----|-----|
| ![Green](https://img.shields.io/badge/Green-0_228_0-%2300E400)   | 0   | 228 | 0   | #00E400 | 40  | 0   | 100 | 0   |
| ![Yellow](https://img.shields.io/badge/Yellow-255_255_0-%23FFFF00)  | 255 | 255 | 0   | #FFFF00 | 0   | 0   | 100 | 0   |
| ![Orange](https://img.shields.io/badge/Orange-255_126_0-%23FF7E00)  | 255 | 126 | 0   | #FF7E00 | 0   | 52  | 100 | 0   |
| ![Red](https://img.shields.io/badge/Red-255_0_0-%23FF0000)     | 255 | 0   | 0   | #FF0000 | 0   | 100 | 100 | 0   |
| ![Purple](https://img.shields.io/badge/Purple-143_63_151-%238F3F97) | 143 | 63  | 151 | #8F3F97 | 5   | 58  | 0   | 41  |
| ![Maroon](https://img.shields.io/badge/Maroon-126_0_35-%237E0023)  | 126 | 0   | 35  | #7E0023 | 30  | 100 | 100 | 30  |

## 使用方法

```python
from aqi_hub.aqi import cal_iaqi_cn

print("hello")
```

## 参考文献

1. [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)
2. [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
