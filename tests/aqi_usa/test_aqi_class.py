"""
测试 AQI_USA 计算模块中的 AQI 类
"""

import warnings

import pytest

from aqi_hub.aqi_usa.aqi import AQI


@pytest.fixture
def aqi_instance_normal():
    """创建一个正常情况下的AQI实例"""
    return AQI(
        pm25=10.0,  # PM2.5浓度较低
        pm10=50.0,  # PM10浓度较低
        so2_1h=35.0,  # SO2浓度较低
        no2=50.0,  # NO2浓度较低
        co=3.0,  # CO浓度较低
        o3_8h=0.071,  # O3浓度刚好进入101-150区间
    )


@pytest.fixture
def aqi_instance_high():
    """创建一个污染物浓度较高的AQI实例"""
    return AQI(
        pm25=200.5,  # PM2.5浓度非常高
        pm10=350.0,  # PM10浓度高
        so2_1h=200.0,  # SO2浓度高
        no2=200.0,  # NO2浓度高
        co=10.0,  # CO浓度高
        o3_8h=0.150,  # O3浓度高
        so2_24h=350.0,  # SO2 24小时浓度高
        o3_1h=0.200,  # O3 1小时浓度高
    )


def test_aqi_normal(aqi_instance_normal):
    """测试正常情况下的AQI计算"""
    assert aqi_instance_normal.AQI == 101  # 预期AQI值
    assert aqi_instance_normal.aqi_level == 3  # 预期AQI等级（101-150为等级3）
    assert set(aqi_instance_normal.primary_pollutant) == {"O3"}  # 预期首要污染物


def test_aqi_high(aqi_instance_high):
    """测试污染物浓度较高情况下的AQI计算"""
    assert aqi_instance_high.AQI == 275  # 预期AQI值
    assert aqi_instance_high.aqi_level == 5  # 预期AQI等级（201-300为等级5）
    assert set(aqi_instance_high.primary_pollutant) == {"PM2.5"}  # 预期首要污染物


def test_aqi_color_properties(aqi_instance_normal):
    """测试AQI颜色属性"""
    # 测试RGB颜色值
    rgb = aqi_instance_normal.aqi_color_rgb
    assert isinstance(rgb, tuple)
    assert len(rgb) == 3
    assert all(isinstance(x, int) for x in rgb)
    assert all(0 <= x <= 255 for x in rgb)

    # 测试CMYK颜色值
    cmyk = aqi_instance_normal.aqi_color_cmyk
    assert isinstance(cmyk, tuple)
    assert len(cmyk) == 4
    assert all(isinstance(x, int) for x in cmyk)
    assert all(0 <= x <= 100 for x in cmyk)

    # 测试RGB十六进制颜色值
    rgb_hex = aqi_instance_normal.aqi_color_rgb_hex
    assert isinstance(rgb_hex, str)
    assert len(rgb_hex) == 7  # 包括#号
    assert rgb_hex.startswith("#")
    assert all(c in "0123456789ABCDEFabcdef" for c in rgb_hex[1:])

    # 测试CMYK十六进制颜色值
    cmyk_hex = aqi_instance_normal.aqi_color_cmyk_hex
    assert isinstance(cmyk_hex, str)
    assert len(cmyk_hex) == 7  # 包括#号
    assert cmyk_hex.startswith("#")
    assert all(c in "0123456789ABCDEFabcdef" for c in cmyk_hex[1:])


def test_aqi_out_of_range():
    """测试超出范围的输入值"""
    # 捕获警告信息
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        aqi = AQI(
            pm25=1000.0,  # 超出最大范围
            pm10=75.0,
            so2_1h=40.0,
            no2=60.0,
            co=3.0,
            o3_8h=0.060,
        )
        # 验证返回最大AQI值500
        assert aqi.AQI == 500
        # 验证发出了警告
        assert len(w) >= 1
        assert issubclass(w[0].category, UserWarning)
        assert "PM25_24H concentration" in str(w[0].message)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
