"""
测试 AQI_USA 计算模块中的 _calculate_iaqi 函数
"""

import pytest
from aqi_hub.aqi_usa.aqi import _calculate_iaqi


@pytest.mark.parametrize(
    "conc,item,expected",
    [
        # PM2.5 浓度测试 (μg/m³)
        (0.0, "PM25_24H", 0),  # 最小值
        (9.0, "PM25_24H", 50),  # 第一个断点
        (9.1, "PM25_24H", 51),  # 略高于第一个断点
        (35.4, "PM25_24H", 100),  # AQI 100
        (35.5, "PM25_24H", 101),  # AQI 101
        (55.4, "PM25_24H", 150),  # AQI 150
        (125.4, "PM25_24H", 200),  # AQI 200
        (225.4, "PM25_24H", 300),  # AQI 300
        (325.4, "PM25_24H", 500),  # AQI 500
        (425.4, "PM25_24H", 500),  # AQI 500
        # PM10 浓度测试 (μg/m³)
        (0, "PM10_24H", 0),  # 最小值
        (54, "PM10_24H", 50),  # 第一个断点
        (154, "PM10_24H", 100),  # AQI 100
        (155, "PM10_24H", 101),  # AQI 101
        (254, "PM10_24H", 150),  # AQI 150
        (354, "PM10_24H", 200),  # AQI 200
        (424, "PM10_24H", 300),  # AQI 300
        (504, "PM10_24H", 388),  # AQI 388
        (604, "PM10_24H", 500),  # AQI 500
        # CO 浓度测试 (ppm)
        (0.0, "CO_8H", 0),  # 最小值
        (4.4, "CO_8H", 50),  # AQI 50
        (4.5, "CO_8H", 51),  # AQI 51
        (9.4, "CO_8H", 100),  # AQI 100
        (12.4, "CO_8H", 150),  # AQI 150
        (15.4, "CO_8H", 200),  # AQI 200
        (30.4, "CO_8H", 300),  # AQI 300
        (40.4, "CO_8H", 400),  # AQI 400
        (50.4, "CO_8H", 500),  # AQI 500
        # NO2 浓度测试 (ppb)
        (0, "NO2_1H", 0),  # 最小值
        (53, "NO2_1H", 50),  # AQI 50
        (100, "NO2_1H", 100),  # AQI 100
        (360, "NO2_1H", 150),  # AQI 150
        (649, "NO2_1H", 200),  # AQI 200
        (1249, "NO2_1H", 500),  # AQI 500 (超过最大值)
        (1649, "NO2_1H", 500),  # AQI 500 (超过最大值)
        (2049, "NO2_1H", 500),  # AQI 500 (超过最大值)
        # SO2 1小时浓度测试 (ppb)
        (0, "SO2_1H", 0),  # 最小值
        (35, "SO2_1H", 50),  # AQI 50
        (75, "SO2_1H", 100),  # AQI 100
        (185, "SO2_1H", 150),  # AQI 150
        (304, "SO2_1H", 200),  # AQI 200
        # SO2 24小时浓度测试 (ppb)
        (305, "SO2_24H", 201),  # AQI 201
        (605, "SO2_24H", 301),  # AQI 301
        (805, "SO2_24H", 400),  # AQI 400
        (1005, "SO2_24H", 500),  # AQI 500
        (1205, "SO2_24H", 500),  # AQI 500
        # O3 8小时浓度测试 (ppm)
        (0.000, "O3_8H", 0),  # 最小值
        (0.054, "O3_8H", 50),  # AQI 50
        (0.070, "O3_8H", 100),  # AQI 100
        (0.085, "O3_8H", 150),  # AQI 150
        (0.105, "O3_8H", 200),  # AQI 200
        # O3 1小时浓度测试 (ppm)
        (0.125, "O3_1H", 101),  # 最小有效值
        (0.164, "O3_1H", 150),  # AQI 150
        (0.204, "O3_1H", 200),  # AQI 200
        (0.404, "O3_1H", 300),  # AQI 300
        (0.504, "O3_1H", 400),  # AQI 400
        (0.604, "O3_1H", 500),  # AQI 500
    ],
)
def test_calculate_iaqi_normal(conc, item, expected):
    """测试正常情况下的线性插值计算"""
    assert _calculate_iaqi(conc, item) == expected


@pytest.mark.parametrize(
    "conc,item,warning_msg,expected",
    [
        # O3 1小时特殊情况
        (0.124, "O3_1H", "O3_1H concentration .* is less than 0.125 ppm", None),
        (0.605, "O3_1H", "O3_1H concentration .* is greater than .*", 500),
        # O3 8小时特殊情况
        (-0.01, "O3_8H", "O3_8H concentration .* is less than .*", None),
        (0.201, "O3_8H", "O3_8H concentration .* is greater than .*", None),
        # SO2 1小时特殊情况
        (
            305,
            "SO2_1H",
            "1-hr SO2 concentrations do not define higher AQI values",
            None,
        ),
        # SO2 24小时特殊情况
        (
            304,
            "SO2_24H",
            "24-hr SO2 concentrations do not define higher AQI values",
            None,
        ),
        # 超出范围的值
        (1000, "PM25_24H", ".* is greater than .*", 500),
        (-1, "PM10_24H", "No suitable interval found", None),
    ],
)
def test_calculate_iaqi_warnings(conc, item, warning_msg, expected):
    """测试会触发警告的特殊情况"""
    with pytest.warns(UserWarning, match=warning_msg):
        assert _calculate_iaqi(conc, item) == expected


@pytest.mark.parametrize(
    "conc,item,error_msg",
    [
        (100, "INVALID_POLLUTANT", "item must be one of"),
    ],
)
def test_calculate_iaqi_errors(conc, item, error_msg):
    """测试会触发错误的情况"""
    with pytest.raises(ValueError, match=error_msg):
        _calculate_iaqi(conc, item)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
