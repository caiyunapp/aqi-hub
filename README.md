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

| Color                                                                          | R   | G   | B   | --- | C   | M   | Y   | K   |
| ------------------------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| <span style="background-color: rgb(0, 228, 0); color: white;">Green</span>     | 0   | 228 | 0   | --- | 40  | 0   | 100 | 0   |
| <span style="background-color: rgb(255, 255, 0); color: black;">Yellow</span>  | 255 | 255 | 0   | --- | 0   | 0   | 100 | 0   |
| <span style="background-color: rgb(255, 126, 0); color: white;">Orange</span>  | 255 | 126 | 0   | --- | 0   | 52  | 100 | 0   |
| <span style="background-color: rgb(255, 0, 0); color: white;">Red</span>       | 255 | 0   | 0   | --- | 0   | 100 | 100 | 0   |
| <span style="background-color: rgb(143, 63, 151); color: white;">Purple</span> | 143 | 63  | 151 | --- | 5   | 58  | 0   | 41  |
| <span style="background-color: rgb(126, 0, 35); color: white;">Maroon</span>   | 126 | 0   | 35  | --- | 30  | 100 | 100 | 30  |

## 使用方法

```python
from aqi_hub.aqi import cal_iaqi_cn

print("hello")
```

## 参考文献

1. [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)
2. [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
