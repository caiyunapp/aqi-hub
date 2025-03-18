"""
测试 AQI_USA 计算模块中的 _calculate_iaqi 函数
"""

import pytest
from aqi_hub.aqi_usa.aqi import _calculate_iaqi


def test_calculate_iaqi_normal():
    """测试正常情况下的线性插值计算"""
    # PM2.5 浓度为 35.5 μg/m³，应该返回 IAQI 为 101
    assert _calculate_iaqi(35.5, "PM25_24H") == 101

    # PM10 浓度为 155 μg/m³，应该返回 IAQI 为 101 
    assert _calculate_iaqi(155, "PM10_24H") == 101

    # CO 浓度为 4.5 ppm，应该返回 IAQI 为 51
    assert _calculate_iaqi(4.5, "CO_8H") == 51

    # SO2_24H 浓度为 304 ppb，应该返回 IAQI 为 200
    assert _calculate_iaqi(304, "SO2_1H") == 200

    # NO2_1H 浓度为 360 ppb，应该返回 IAQI 为 150
    assert _calculate_iaqi(360, "NO2_1H") == 150

    # O3_8H 浓度为 0.085 ppm，应该返回 IAQI 为 150
    assert _calculate_iaqi(0.085, "O3_8H") == 150

    # O3_1H 浓度为 0.165 ppm，应该返回 IAQI 为 151
    assert _calculate_iaqi(0.165, "O3_1H") == 151

    # PM2.5 浓度为 9.1 μg/m³，应该返回 IAQI 为 51
    assert _calculate_iaqi(9.1, "PM25_24H") == 51

    # PM10 浓度为 54 μg/m³，应该返回 IAQI 为 50
    assert _calculate_iaqi(54, "PM10_24H") == 50


def test_calculate_iaqi_o3_1h_special():
    """测试臭氧1小时特殊情况"""
    # 浓度小于 0.125 ppm
    with pytest.warns(UserWarning):
        assert _calculate_iaqi(0.124, "O3_1H") is None

    # 浓度等于 0.125 ppm
    assert _calculate_iaqi(0.125, "O3_1H") == 101

    # 浓度大于最大值
    with pytest.warns(UserWarning):
        assert _calculate_iaqi(0.605, "O3_1H") == 500


def test_calculate_iaqi_o3_8h_special():
    """测试臭氧8小时特殊情况"""
    # 浓度小于最小值
    with pytest.warns(UserWarning):
        assert _calculate_iaqi(-0.001, "O3_8H") is None

    # 正常范围内的值
    assert _calculate_iaqi(0.085, "O3_8H") == 150

    # 浓度大于等于 0.201 ppm
    with pytest.warns(UserWarning):
        assert _calculate_iaqi(0.201, "O3_8H") is None


def test_calculate_iaqi_so2_special():
    """测试二氧化硫特殊情况"""
    # 正常范围内的值
    assert _calculate_iaqi(75, "SO2_1H") == 100

    # 浓度大于等于 305 ppb
    with pytest.warns(UserWarning):
        assert _calculate_iaqi(305, "SO2_1H") is None


def test_calculate_iaqi_invalid_input():
    """测试无效输入"""
    # 测试无效的污染物类型
    with pytest.raises(ValueError, match="item must be one of"):
        _calculate_iaqi(100, "INVALID_POLLUTANT")


def test_calculate_iaqi_boundary_values():
    """测试边界值"""
    # PM2.5 最小值
    assert _calculate_iaqi(0.0, "PM25_24H") == 0

    # PM2.5 临界值
    assert _calculate_iaqi(9.1, "PM25_24H") == 51
    assert _calculate_iaqi(35.5, "PM25_24H") == 101

    # PM10 临界值
    assert _calculate_iaqi(154, "PM10_24H") == 100
    assert _calculate_iaqi(155, "PM10_24H") == 101


if __name__ == "__main__":
    test_calculate_iaqi_normal()
    test_calculate_iaqi_o3_1h_special()
    test_calculate_iaqi_o3_8h_special()
    test_calculate_iaqi_so2_special()
    test_calculate_iaqi_invalid_input()
    test_calculate_iaqi_boundary_values()