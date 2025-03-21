import pytest

from aqi_hub.aqi_usa.aqi import get_aqi_level


@pytest.mark.parametrize(
    "aqi_value,expected_level",
    [
        # 第一级 (0-50)
        (0, 1),
        (25, 1),
        (50, 1),
        # 第二级 (51-100)
        (51, 2),
        (75, 2),
        (100, 2),
        # 第三级 (101-150)
        (101, 3),
        (125, 3),
        (150, 3),
        # 第四级 (151-200)
        (151, 4),
        (175, 4),
        (200, 4),
        # 第五级 (201-300)
        (201, 5),
        (250, 5),
        (300, 5),
        # 第六级 (301-500)
        (301, 6),
        (400, 6),
        (500, 6),
    ],
    ids=lambda x: f"AQI_{x}" if isinstance(x, int) else "Level",
)
def test_get_aqi_level_valid_ranges(aqi_value, expected_level):
    """测试不同AQI值范围的等级判断"""
    assert get_aqi_level(aqi_value) == expected_level


@pytest.mark.parametrize(
    "invalid_aqi,error_message",
    [
        (-1, "AQI must be between 0 and 500"),
        (501, "AQI must be between 0 and 500"),
    ],
    ids=["negative_value", "exceed_maximum"],
)
def test_get_aqi_level_invalid_values(invalid_aqi, error_message):
    """测试无效的AQI值"""
    with pytest.raises(ValueError, match=error_message):
        get_aqi_level(invalid_aqi)


if __name__ == "__main__":
    # 使用 pytest 运行当前文件中的所有测试
    pytest.main([__file__, "-v"])
