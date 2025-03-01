import pytest

from aqi_hub.aqi_cn.aqi import cal_iaqi_cn


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        (35, 50),
        (75, 100),
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
        (150, 100),
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
        (1600, None),
        (2100, None),
        (2620, None),
        (3000, None),
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
        (1000, None),
        (1200, None),
        (1500, None),
    ],
)
@pytest.mark.parametrize("item", ["O3_8H"])
def test_o3_8h(value, expected, item):
    print(f"item: {item}, value: {value}, expected: {expected}")
    assert cal_iaqi_cn(item, value) == expected


if __name__ == "__main__":
    # test_so2_1h(3000, None, "SO2_1H")
    pytest.main(["-v", "tests/test_aqi.py"])