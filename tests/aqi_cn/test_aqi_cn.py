import pytest

from aqi_hub.aqi_cn.aqi import AQI, cal_iaqi_cn


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (35, 50),
        (60, 100),
        (75, 114),
        (115, 150),
        (150, 200),
        (250, 300),
        (350, 400),
        (500, 500),
        (600, 500),
    ],
)
@pytest.mark.parametrize("item", ["PM25_24H", "PM25_1H"])
def test_pm25(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (50, 50),
        (120, 100),
        (150, 112),
        (250, 150),
        (350, 200),
        (420, 300),
        (500, 400),
        (600, 500),
    ],
)
@pytest.mark.parametrize("item", ["PM10_24H", "PM10_1H"])
def test_pm10(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (150, 50),
        (500, 100),
        (650, 150),
        (800, 200),
        (1600, 300),
        (2100, 400),
        (2620, 500),
        (3000, 500),
    ],
)
@pytest.mark.parametrize("item", ["SO2_24H"])
def test_so2_24h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (150, 50),
        (500, 100),
        (650, 150),
        (800, 200),
        (1600, 200),
        (2100, 200),
        (2620, 200),
        (3000, 200),
    ],
)
@pytest.mark.parametrize("item", ["SO2_1H"])
def test_so2_1h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (40, 50),
        (80, 100),
        (180, 150),
        (280, 200),
        (565, 300),
        (750, 400),
        (940, 500),
        (1000, 500),
    ],
)
@pytest.mark.parametrize("item", ["NO2_24H"])
def test_no2_24h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (100, 50),
        (200, 100),
        (700, 150),
        (1200, 200),
        (2340, 300),
        (3090, 400),
        (3840, 500),
        (4000, 500),
    ],
)
@pytest.mark.parametrize("item", ["NO2_1H"])
def test_no2_1h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (2, 50),
        (4, 100),
        (14, 150),
        (24, 200),
        (36, 300),
        (48, 400),
        (60, 500),
        (100, 500),
    ],
)
@pytest.mark.parametrize("item", ["CO_24H"])
def test_co_24h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (5, 50),
        (10, 100),
        (35, 150),
        (60, 200),
        (90, 300),
        (120, 400),
        (150, 500),
        (200, 500),
    ],
)
@pytest.mark.parametrize("item", ["CO_1H"])
def test_co_1h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (160, 50),
        (200, 100),
        (300, 150),
        (400, 200),
        (800, 300),
        (1000, 400),
        (1200, 500),
        (1500, 500),
        (2000, 500),  # 超出范围时仍返回500
    ],
)
@pytest.mark.parametrize("item", ["O3_1H"])
def test_o3_1h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (100, 50),
        (160, 100),
        (215, 150),
        (265, 200),
        (800, 300),
        (1000, 300),
        (1200, 300),
        (1500, 300),
    ],
)
@pytest.mark.parametrize("item", ["O3_8H"])
def test_o3_8h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


def test_invalid_inputs():
    """测试无效输入的处理"""
    with pytest.raises(TypeError):
        cal_iaqi_cn("PM25_24H", "invalid")

    with pytest.raises(ValueError):
        cal_iaqi_cn("INVALID", 100)

    assert cal_iaqi_cn("PM25_24H", -1) is None
    assert cal_iaqi_cn("PM25_24H", None) is None


def test_aqi_class_hourly():
    """测试AQI类的小时值计算"""
    aqi = AQI(pm25=75, pm10=150, so2=500, no2=200, co=10, o3=200, data_type="hourly")

    # 新标准下 PM2.5=75 → IAQI 114（轻度），PM10=150 → 112，其余 100
    assert aqi.AQI == 114
    assert "PM2.5" in aqi.primary_pollutant
    assert aqi.aqi_level == 3  # 101-150 轻度污染
    assert isinstance(aqi.aqi_color_rgb, tuple)
    assert len(aqi.aqi_color_rgb) == 3
    assert isinstance(aqi.aqi_color_rgb_hex, str)


def test_aqi_class_daily():
    """测试AQI类的日均值计算"""
    aqi = AQI(pm25=115, pm10=250, so2=650, no2=180, co=14, o3=215, data_type="daily")

    assert aqi.AQI == 150  # 应该返回最大的IAQI值
    assert len(aqi.exceed_pollutant) > 0  # 应该有超标污染物
    assert all(
        pollutant in aqi.primary_pollutant_cn
        for pollutant in ["细颗粒物", "可吸入颗粒物"]
    )

    # 测试颜色值
    assert isinstance(aqi.aqi_color_cmyk, tuple)
    assert len(aqi.aqi_color_cmyk) == 4
    assert isinstance(aqi.aqi_color_cmyk_hex, str)


def test_aqi_invalid_data_type():
    """测试AQI类的无效数据类型处理"""
    with pytest.raises(ValueError):
        AQI(pm25=75, pm10=150, so2=500, no2=200, co=10, o3=200, data_type="invalid")


def test_hj633_2026_pm_boundaries():
    """HJ 633-2026：PM2.5 良/轻度界限 60，PM10 良/轻度界限 120"""
    # PM2.5=59 为良 (IAQI<100)，60 为轻度起算 (IAQI=100)
    assert cal_iaqi_cn("PM25_1H", 59) == 98  # 良
    assert cal_iaqi_cn("PM25_1H", 60) == 100  # 轻度下界
    # PM10=118 为良，120 为轻度起算
    assert cal_iaqi_cn("PM10_1H", 118) == 99  # 良
    assert cal_iaqi_cn("PM10_1H", 120) == 100  # 轻度下界
    # 集成：PM2.5=60 主导时 AQI=100、等级 2（100 仍属良）
    aqi_60 = AQI(pm25=60, pm10=50, so2=150, no2=100, co=5, o3=160, data_type="hourly")
    assert aqi_60.AQI == 100
    assert aqi_60.aqi_level == 2


def test_extreme_values():
    """测试极端值情况"""
    # 测试所有污染物浓度都很低的情况
    aqi_low = AQI(pm25=1, pm10=1, so2=1, no2=1, co=0.1, o3=1, data_type="hourly")
    assert aqi_low.AQI < 50
    assert len(aqi_low.primary_pollutant) == 0
    assert len(aqi_low.exceed_pollutant) == 0

    # 测试所有污染物浓度都很高的情况
    aqi_high = AQI(
        pm25=500, pm10=600, so2=2620, no2=3840, co=150, o3=1200, data_type="hourly"
    )
    assert aqi_high.AQI == 500
    assert len(aqi_high.primary_pollutant) > 0
    assert len(aqi_high.exceed_pollutant) > 0


def test_aqi_with_none_values():
    """测试AQI计算中包含None值的情况"""
    # 测试 SO2>800 时按 IAQI 200 计
    aqi = AQI(
        pm25=75,  # 114
        pm10=150,  # 112
        so2=800,  # 200
        no2=200,  # 100
        co=None,
        o3=200,  # 100
        data_type="hourly",
    )
    assert aqi.AQI == 200  # SO2 的 IAQI 为 200
    assert "SO2" in aqi.primary_pollutant
    assert len(aqi.primary_pollutant) > 0

    # 测试关键污染物为None的情况
    aqi = AQI(
        pm25=75,  # 114
        pm10=150,  # 112
        so2=None,  # None
        no2=200,  # 100
        co=10,  # 100
        o3=200,  # 100
        data_type="hourly",
    )
    assert aqi.AQI == 114  # 非 None 的 IAQI 最大值
    assert len(aqi.primary_pollutant) > 0

    # 测试全部污染物为None的情况
    aqi = AQI(
        pm25=None, pm10=None, so2=None, no2=None, co=None, o3=None, data_type="hourly"
    )
    assert aqi.AQI is None  # 当所有IAQI都为None时，AQI也应该为None
    assert len(aqi.primary_pollutant) == 0
    assert len(aqi.exceed_pollutant) == 0

    # 测试部分污染物超出范围：SO2>800 现按 IAQI 200 计，O3_1H 超范围仍为 500
    aqi = AQI(
        pm25=75,  # 114
        pm10=150,  # 112
        so2=3000,  # 200（超过 800 按 200 计）
        no2=200,  # 100
        co=10,  # 100
        o3=2000,  # 500 (O3_1H 超出范围时返回 500)
        data_type="hourly",
    )
    assert aqi.AQI == 500  # O3_1H 主导
    assert "O3" in aqi.primary_pollutant
    assert len(aqi.primary_pollutant) > 0


if __name__ == "__main__":
    # test_so2_1h(3000, None, "SO2_1H")
    pytest.main(["-v", "tests/test_aqi.py"])
