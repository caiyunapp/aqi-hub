"""
测试 AQI_USA 计算模块中的 cal_aqi_usa 函数
"""

import pytest

from aqi_hub.aqi_usa.aqi import cal_aqi_usa


@pytest.mark.parametrize(
    "pm25,pm10,so2_1h,no2,co,o3_8h,so2_24h,o3_1h,expected_aqi,expected_iaqi",
    [
        # 测试用例 1: 所有污染物浓度较低
        (
            5.0,  # PM2.5
            40.0,  # PM10
            20.0,  # SO2_1H
            40.0,  # NO2
            2.0,  # CO
            0.040,  # O3_8H
            None,  # SO2_24H
            None,  # O3_1H
            37,  # 预期 AQI
            {
                "PM2.5": 27,
                "PM10": 37,
                "SO2": 28,
                "NO2": 37,
                "CO": 22,
                "O3": 37,
            },
        ),
        # 测试用例 2: PM2.5 为主要污染物
        (
            150.5,  # PM2.5
            150.0,  # PM10
            30.0,  # SO2_1H
            100.0,  # NO2
            4.0,  # CO
            0.070,  # O3_8H
            None,  # SO2_24H
            None,  # O3_1H
            225,  # 预期 AQI
            {
                "PM2.5": 225,
                "PM10": 98,
                "SO2": 42,
                "NO2": 100,
                "CO": 45,
                "O3": 100,
            },
        ),
        # 测试用例 3: SO2 24小时和1小时值都存在
        (
            10.0,  # PM2.5
            50.0,  # PM10
            200.0,  # SO2_1H
            50.0,  # NO2
            3.0,  # CO
            0.050,  # O3_8H
            400.0,  # SO2_24H
            None,  # O3_1H
            232,  # 预期 AQI (保持原值)
            {"PM2.5": 52, "PM10": 46, "SO2": 232, "NO2": 47, "CO": 34, "O3": 46},
        ),
        # 测试用例 4: O3 8小时和1小时值都存在
        (
            20.0,  # PM2.5
            80.0,  # PM10
            50.0,  # SO2_1H
            80.0,  # NO2
            5.0,  # CO
            0.090,  # O3_8H
            None,  # SO2_24H
            0.150,  # O3_1H
            161,  # 预期 AQI (保持原值)
            {
                "PM2.5": 71,
                "PM10": 63,
                "SO2": 68,
                "NO2": 78,
                "CO": 56,
                "O3": 161,
            },
        ),
        # 测试用例 5: 多个污染物超标
        (
            250.5,  # PM2.5
            420.0,  # PM10
            304.0,  # SO2_1H
            600.0,  # NO2
            15.0,  # CO
            0.200,  # O3_8H
            None,  # SO2_24H
            0.350,  # O3_1H
            350,  # 预期 AQI (保持原值)
            {
                "PM2.5": 350,
                "PM10": 294,
                "SO2": 200,
                "NO2": 191,
                "CO": 193,
                "O3": 300,
            },
        ),
    ],
)
def test_cal_aqi_usa_normal(
    pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h, expected_aqi, expected_iaqi
):
    """测试正常情况下的 AQI 计算"""
    aqi, iaqi = cal_aqi_usa(pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h)
    assert aqi == expected_aqi
    assert iaqi == expected_iaqi


@pytest.mark.parametrize(
    "pm25,pm10,so2_1h,no2,co,o3_8h,so2_24h,o3_1h,expected_aqi",
    [
        # 测试用例 1: 超出范围的值
        (
            600.0,  # PM2.5 超出范围
            900.0,  # PM10 超出范围
            400.0,  # SO2_1H
            2500.0,  # NO2 超出范围
            60.0,  # CO 超出范围
            0.250,  # O3_8H 超出范围
            None,  # SO2_24H
            0.700,  # O3_1H 超出范围
            500,  # 预期 AQI
        ),
    ],
)
def test_cal_aqi_usa_extreme(
    pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h, expected_aqi
):
    """测试极端情况下的 AQI 计算"""
    aqi, _ = cal_aqi_usa(pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h)
    assert aqi == expected_aqi


if __name__ == "__main__":
    pytest.main(["-v", __file__])
