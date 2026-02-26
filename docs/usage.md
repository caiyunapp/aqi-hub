# 使用方法

## 安装

```bash
pip install aqi-hub
```

## 中国 AQI 计算

依据 **GB 3095-2026** 与 **HJ 633-2026**，支持小时值与日均值。

### 1. AQI 计算

```python
from aqi_hub.aqi_cn.aqi import cal_aqi_cn

# 计算小时值 AQI
aqi, iaqi = cal_aqi_cn(
    pm25=45, pm10=80, so2=35, no2=85, co=3, o3=140, data_type="hourly"
)
print(f"AQI: {aqi}")
print(f"IAQI: {iaqi}")

# 计算日均值 AQI（O3 使用 8 小时滑动平均）
aqi, iaqi = cal_aqi_cn(
    pm25=120, pm10=180, so2=65, no2=150, co=8, o3=200, data_type="daily"
)
print(f"AQI: {aqi}, IAQI: {iaqi}")
```

### 2. IAQI 计算

```python
from aqi_hub.aqi_cn.aqi import cal_iaqi_cn

pm25_iaqi = cal_iaqi_cn("PM25_24H", 120)
pm10_iaqi = cal_iaqi_cn("PM10_24H", 180)
print(f"PM25_24H IAQI: {pm25_iaqi}, PM10_24H IAQI: {pm10_iaqi}")
```

### 3. 空气质量等级

```python
from aqi_hub.aqi_cn.aqi import get_aqi_level

level = get_aqi_level(120)  # 1~6 级
print(f"AQI 等级: {level}")
```

### 4. 空气质量等级颜色

```python
from aqi_hub.aqi_cn.aqi import get_aqi_level_color

color = get_aqi_level_color(1, "RGB")       # (0, 228, 0)
color = get_aqi_level_color(2, "CMYK")
color = get_aqi_level_color(3, "RGB_HEX")  # "#FF7E00"
color = get_aqi_level_color(4, "CMYK_HEX")
```

### 5. 首要污染物

```python
from aqi_hub.aqi_cn.aqi import cal_primary_pollutant

iaqi = {
    "PM2.5": 120,
    "PM10": 180,
    "SO2": 65,
    "NO2": 150,
    "CO": 8,
    "O3": 200,
}
primary = cal_primary_pollutant(iaqi)   # IAQI > 50 且最大的污染物
print(f"首要污染物: {primary}")
```

### 6. AQI 类（一站式）

```python
from aqi_hub.aqi_cn.aqi import AQI

aqi_obj = AQI(
    pm25=120,
    pm10=180,
    so2=65,
    no2=150,
    co=1.0,
    o3=200,
    data_type="hourly",  # 或 "daily"
)
print(f"AQI: {aqi_obj.AQI}")
print(f"IAQI: {aqi_obj.IAQI}")
print(f"首要污染物: {aqi_obj.primary_pollutant}")
print(f"AQI 等级: {aqi_obj.aqi_level}")
print(f"颜色 RGB: {aqi_obj.aqi_color_rgb}")
print(f"颜色 HEX: {aqi_obj.aqi_color_rgb_hex}")
print(f"中文首要污染物: {aqi_obj.primary_pollutant_cn}")
```

---

## 美国 AQI 计算

依据 US EPA 标准，单位与中国不同（如 O3、CO 用 ppb/ppm）。

### 1. AQI 计算

```python
from aqi_hub.aqi_usa.aqi import cal_aqi_usa

aqi, iaqi = cal_aqi_usa(
    pm25=120,
    pm10=180,
    so2_1h=65,
    no2=150,
    co=8,
    o3_8h=0.200,
    so2_24h=None,
    o3_1h=None,
)
print("aqi:", aqi)
print("iaqi:", iaqi)
```

### 2. IAQI 计算

```python
from aqi_hub.aqi_usa.aqi import cal_iaqi_usa

pm25_iaqi = cal_iaqi_usa(120, "PM25_24H")
pm10_iaqi = cal_iaqi_usa(180, "PM10_24H")
so2_1h_iaqi = cal_iaqi_usa(65, "SO2_1H")
no2_iaqi = cal_iaqi_usa(150, "NO2_1H")
co_iaqi = cal_iaqi_usa(8, "CO_8H")
o3_8h_iaqi = cal_iaqi_usa(0.200, "O3_8H")
o3_1h_iaqi = cal_iaqi_usa(0.200, "O3_1H")
```

### 3. AQI 等级与颜色

```python
from aqi_hub.aqi_usa.aqi import get_aqi_level, get_aqi_level_color

level = get_aqi_level(200)
color = get_aqi_level_color(1, "RGB")
```

### 4. AQI 类

```python
from aqi_hub.aqi_usa.aqi import AQI

aqi = AQI(
    pm25=120,
    pm10=180,
    so2_1h=65,
    no2=150,
    co=8,
    o3_8h=0.200,
    so2_24h=None,
    o3_1h=None,
)
print("aqi:", aqi.AQI)
print("iaqi:", aqi.IAQI)
print("aqi_level:", aqi.aqi_level)
print("primary_pollutant:", aqi.primary_pollutant)
print("aqi_color_rgb:", aqi.aqi_color_rgb)
```

---

## 支持的污染物与单位

| 污染物 | 中国标准单位 | 美国标准单位 | 单位换算（25℃，1 标准大气压） |
|--------|--------------|--------------|-------------------------------|
| PM2.5  | μg/m³        | μg/m³        | 相同                          |
| PM10   | μg/m³        | μg/m³        | 相同                          |
| O3     | μg/m³        | ppb          | 1 ppb = 1.962 μg/m³           |
| CO     | mg/m³        | ppm          | 1 ppm = 1.145 mg/m³           |
| NO2    | μg/m³        | ppb          | 1 ppb = 1.88 μg/m³            |
| SO2    | μg/m³        | ppb          | 1 ppb = 2.62 μg/m³            |

中国标准下 SO2、NO2、O3、CO 均使用 **μg/m³** 或 **mg/m³**（CO）；美国标准下气态污染物使用 **ppb/ppm**，需按上表换算后再传入。
