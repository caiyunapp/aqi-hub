# AQI Hub

![AQI Hub Cover](docs/cover.png)

aqi 计算，以及分指数计算  
目前仅支持中国 aqi 计算。


## 计算方法

### AQI (CN)

计算方法参照中华人民共和国生态环境部标准： [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)

### AQI (USA)

计算方法参考 US EPA: [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)

| AQI Range  | Descriptor                     | Color  |
| ---------- | ------------------------------ | ------ |
| 0 to 50    | Good                           | Green  |
| 51 to 100  | Moderate                       | Yellow |
| 101 to 150 | Unhealthy for Sensitive Groups | Orange |
| 151 to 200 | Unhealthy                      | Red    |
| 201 to 300 | Very Unhealthy                 | Purple |
| 301+       | Hazardous                      | Maroon |

## 使用方法

```python
from aqi_hub.aqi import cal_iaqi_cn

print("hello")
```


## 参考文献

1. [HJ 633--2012 环境空气质量指数 （AQI） 技术规定 （试行）.pdf](https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/jcffbz/201203/W020120410332725219541.pdf)
2. [Technical Assistance Document for the Reporting of Daily Air Quality – the Air Quality Index (AQI)](https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)
