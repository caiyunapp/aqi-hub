"""测试 AQI 计算模块"""

import pytest

from aqi_hub.aqi_cn.aqi import cal_aqi_cn


def test_cal_aqi_cn_hourly_normal():
    """测试正常的小时值 AQI 计算"""
    aqi, iaqi = cal_aqi_cn(
        pm25=35,  # IAQI = 50
        pm10=50,  # IAQI = 50
        so2=150,  # IAQI = 50
        no2=100,  # IAQI = 50
        co=5,  # IAQI = 50
        o3=160,  # IAQI = 50
        data_type="hourly",
    )
    assert aqi == 50
    assert iaqi == {"PM2.5": 50, "PM10": 50, "SO2": 50, "NO2": 50, "CO": 50, "O3": 50}


def test_cal_aqi_cn_daily_normal():
    """测试正常的日均值 AQI 计算"""
    aqi, iaqi = cal_aqi_cn(
        pm25=35,  # IAQI = 50
        pm10=50,  # IAQI = 50
        so2=150,  # IAQI = 50
        no2=40,  # IAQI = 50
        co=2,  # IAQI = 50
        o3=100,  # IAQI = 50
        data_type="daily",
    )
    assert aqi == 50
    assert iaqi == {"PM2.5": 50, "PM10": 50, "SO2": 50, "NO2": 50, "CO": 50, "O3": 50}


def test_cal_aqi_cn_hourly_high():
    """测试高浓度的小时值 AQI 计算"""
    aqi, iaqi = cal_aqi_cn(
        pm25=250,  # IAQI = 300
        pm10=350,  # IAQI = 200
        so2=650,  # IAQI = 150
        no2=700,  # IAQI = 150
        co=35,  # IAQI = 150
        o3=300,  # IAQI = 150
        data_type="hourly",
    )
    assert aqi == 300
    assert iaqi == {
        "PM2.5": 300,
        "PM10": 200,
        "SO2": 150,
        "NO2": 150,
        "CO": 150,
        "O3": 150,
    }


def test_cal_aqi_cn_invalid_data_type():
    """测试无效的数据类型"""
    with pytest.raises(ValueError, match="data_type must be 'hourly' or 'daily'"):
        cal_aqi_cn(
            pm25=35, pm10=50, so2=150, no2=100, co=5, o3=160, data_type="invalid"
        )


def test_cal_aqi_cn_negative_values():
    """测试负值输入"""
    aqi, iaqi = cal_aqi_cn(
        pm25=-1,  # IAQI = None
        pm10=50,  # IAQI = 50
        so2=150,  # IAQI = 50
        no2=100,  # IAQI = 50
        co=5,  # IAQI = 50
        o3=160,  # IAQI = 50
        data_type="hourly",
    )
    assert aqi == 50
    assert iaqi == {"PM2.5": None, "PM10": 50, "SO2": 50, "NO2": 50, "CO": 50, "O3": 50}


def test_cal_aqi_cn_exceed_limits():
    """测试超出限值的情况（SO2>800 按 IAQI 200 计，O3_8H>800 按 300 计）"""
    aqi, iaqi = cal_aqi_cn(
        pm25=35,  # IAQI = 50
        pm10=50,  # IAQI = 50
        so2=801,  # IAQI = 200（超过 800 按 200 计）
        no2=100,  # IAQI = 50
        co=5,  # IAQI = 50
        o3=-1,  # IAQI = None（负值无效）
        data_type="hourly",
    )
    assert aqi == 200
    assert iaqi == {
        "PM2.5": 50,
        "PM10": 50,
        "SO2": 200,
        "NO2": 50,
        "CO": 50,
        "O3": None,
    }


def test_cal_aqi_cn_daily_o3_8h_exceed_800():
    """日均 AQI 下 O3_8H > 800 时 IAQI 按 300 计（HJ 633-2026）"""
    aqi, iaqi = cal_aqi_cn(
        pm25=35,  # IAQI = 50
        pm10=50,  # IAQI = 50
        so2=150,  # IAQI = 50
        no2=40,  # IAQI = 50
        co=2,  # IAQI = 50
        o3=1000,  # O3_8H > 800，IAQI = 300
        data_type="daily",
    )
    assert aqi == 300
    assert iaqi["O3"] == 300
    assert iaqi["PM2.5"] == 50


def test_cal_aqi_cn_all_invalid():
    """测试所有值都无效的情况"""
    aqi, iaqi = cal_aqi_cn(
        pm25=-1,  # IAQI = None
        pm10=-1,  # IAQI = None
        so2=-1,  # IAQI = None
        no2=-1,  # IAQI = None
        co=-1,  # IAQI = None
        o3=-1,  # IAQI = None
        data_type="hourly",
    )
    assert aqi is None
    assert iaqi == {
        "PM2.5": None,
        "PM10": None,
        "SO2": None,
        "NO2": None,
        "CO": None,
        "O3": None,
    }


if __name__ == "__main__":
    # test_cal_aqi_cn_hourly_normal()
    # test_cal_aqi_cn_daily_normal()
    # test_cal_aqi_cn_hourly_high()
    # test_cal_aqi_cn_invalid_data_type()
    # test_cal_aqi_cn_negative_values()
    # test_cal_aqi_cn_exceed_limits()
    test_cal_aqi_cn_all_invalid()
