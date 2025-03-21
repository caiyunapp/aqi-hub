import pytest

from aqi_hub.aqi_usa.aqi import cal_primary_pollutant


@pytest.mark.parametrize(
    "iaqi_dict,expected_pollutants",
    [
        # 单个首要污染物的情况
        (
            {"PM2.5": 150, "PM10": 75, "SO2": 50, "NO2": 100, "CO": 80, "O3": 120},
            ["PM2.5"],
        ),
        # 多个首要污染物的情况（相同的最大值）
        (
            {"PM2.5": 200, "PM10": 200, "SO2": 150, "NO2": 180, "CO": 160, "O3": 200},
            ["PM2.5", "PM10", "O3"],
        ),
        # 包含None值的情况
        (
            {"PM2.5": 80, "PM10": None, "SO2": 60, "NO2": None, "CO": 50, "O3": 40},
            ["PM2.5"],
        ),
        # 所有值都相同的情况
        (
            {"PM2.5": 100, "PM10": 100, "SO2": 100, "NO2": 100, "CO": 100, "O3": 100},
            ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
        ),
        # 只有一个污染物的情况
        ({"PM2.5": 75}, ["PM2.5"]),
        # 部分污染物为None，但仍有有效值的情况
        (
            {"PM2.5": None, "PM10": 120, "SO2": None, "NO2": 80, "CO": None, "O3": 90},
            ["PM10"],
        ),
        # 所有值都为None的情况
        ({"PM2.5": None, "PM10": None, "SO2": None}, []),
    ],
    ids=[
        "single_primary",
        "multiple_primary",
        "with_none_values",
        "all_equal",
        "single_pollutant",
        "partial_none",
        "all_none_values",
    ],
)
def test_cal_primary_pollutant_valid(iaqi_dict, expected_pollutants):
    """测试计算首要污染物的各种有效情况"""
    result = cal_primary_pollutant(iaqi_dict)
    assert sorted(result) == sorted(expected_pollutants)


def test_cal_primary_pollutant_empty_dict():
    """测试空字典情况下的警告"""
    with pytest.warns(UserWarning, match="IAQI字典为空"):
        result = cal_primary_pollutant({})
        assert result == []


def test_cal_primary_pollutant_all_none():
    """测试所有值为None的情况下的警告"""
    with pytest.warns(UserWarning, match="所有污染物IAQI值均为None"):
        result = cal_primary_pollutant({"PM2.5": None, "PM10": None, "SO2": None})
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
