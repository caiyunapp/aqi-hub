# Breaking Points

## O3 (8-hour)
```python
O3_8H = {
    (0, 50): (0.000, 0.054),
    (51, 100): (0.055, 0.070),
    (101, 150): (0.071, 0.085),
    (151, 200): (0.086, 0.105),
    (201, 300): (0.106, 0.200),
    (301, 500): (0.201, None),  # 上限未定义
}
```

## O3 (1-hour)
```python
O3_1H = {
    (101, 150): (0.125, 0.164),
    (151, 200): (0.165, 0.204),
    (201, 300): (0.205, 0.404),
    (301, 500): (0.405, None),  # 上限未定义
}
```

## PM2.5 (24-hour, μg/m³)
```python
PM25_24H = {
    (0, 50): (0.0, 9.0),
    (51, 100): (9.1, 35.4),
    (101, 150): (35.5, 55.4),
    (151, 200): (55.5, 125.4),
    (201, 300): (125.5, 225.4),
    (301, 500): (225.5, None),  # 上限未定义
}
```

## PM10 (24-hour, μg/m³)
```python
PM10_24H = {
    (0, 50): (0, 54),
    (51, 100): (55, 154),
    (101, 150): (155, 254),
    (151, 200): (255, 354),
    (201, 300): (355, 424),
    (301, 500): (425, None),  # 上限未定义
}
```

## CO (8-hour, ppm)
```python
CO_8H = {
    (0, 50): (0.0, 4.4),
    (51, 100): (4.5, 9.4),
    (101, 150): (9.5, 12.4),
    (151, 200): (12.5, 15.4),
    (201, 300): (15.5, 30.4),
    (301, 500): (30.5, None),  # 上限未定义
}
```

## SO2 (1-hour, ppb)
```python
SO2_1H = {
    (0, 50): (0, 35),
    (51, 100): (36, 75),
    (101, 150): (76, 185),
    (151, 200): (186, 304),
    (201, 300): (305, 604),
    (301, 500): (605, None),  # 上限未定义
}
```

## NO2 (1-hour, ppb)
```python
NO2_1H = {
    (0, 50): (0, 53),
    (51, 100): (54, 100),
    (101, 150): (101, 360),
    (151, 200): (361, 649),
    (201, 300): (650, 1249),
    (301, 500): (1250, None),  # 上限未定义
}
```

## 说明
- 所有数据都按照 AQI 等级进行分组：Good (0-50), Moderate (51-100), Unhealthy for Sensitive Groups (101-150), Unhealthy (151-200), Very Unhealthy (201-300), Hazardous (301+)
- 数据格式为 Python 字典，键为 AQI 范围元组，值为污染物浓度范围元组
- None 表示该级别没有上限值
- 所有数值都保持原始精度 