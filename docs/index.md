# AQI Hub

AQI 计算，以及分指数计算。支持**中国**（GB 3095-2026 / HJ 633-2026）与**美国**（EPA）两种标准。

## 特性

- **中国 AQI**：小时值 / 日均值，PM2.5、PM10、SO2、NO2、CO、O3 六项污染物
- **美国 AQI**：EPA 标准，支持 PM2.5、PM10、SO2、NO2、CO、O3
- **IAQI**：各污染物分指数
- **等级与颜色**：AQI 等级、RGB/CMYK 颜色、首要污染物与超标污染物

## 快速开始

```bash
pip install aqi-hub
```

```python
from aqi_hub.aqi_cn.aqi import cal_aqi_cn

aqi, iaqi = cal_aqi_cn(
    pm25=45, pm10=80, so2=35, no2=85, co=3, o3=140, data_type="hourly"
)
print(f"AQI: {aqi}, IAQI: {iaqi}")
```

详细用法请查看 [使用方法](usage.md)。

## 链接

- [PyPI](https://pypi.org/project/aqi-hub/)
- [GitHub](https://github.com/caiyunapp/aqi-hub)
