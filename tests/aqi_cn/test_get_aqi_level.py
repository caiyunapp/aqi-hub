import pytest

from aqi_hub.aqi_cn.aqi import get_aqi_level


@pytest.mark.parametrize(
    "aqi, expected_level",
    [
        (0, 1),  # Lower boundary
        (25, 1),  # Middle of level 1
        (50, 1),  # Upper boundary level 1
        (51, 2),  # Lower boundary level 2
        (75, 2),  # Middle of level 2
        (100, 2),  # Upper boundary level 2
        (101, 3),  # Lower boundary level 3
        (125, 3),  # Middle of level 3
        (150, 3),  # Upper boundary level 3
        (151, 4),  # Lower boundary level 4
        (175, 4),  # Middle of level 4
        (200, 4),  # Upper boundary level 4
        (201, 5),  # Lower boundary level 5
        (250, 5),  # Middle of level 5
        (300, 5),  # Upper boundary level 5
        (301, 6),  # Lower boundary level 6
        (400, 6),  # Middle of level 6
        (500, 6),  # Upper boundary level 6
    ],
)
def test_get_aqi_level(aqi, expected_level):
    assert get_aqi_level(aqi) == expected_level


@pytest.mark.parametrize(
    "invalid_aqi",
    [
        -1,  # Below minimum
        501,  # Above maximum
        600,  # Well above maximum
    ],
)
def test_get_aqi_level_invalid_input(invalid_aqi):
    with pytest.raises(ValueError, match="AQI must be between 0 and 500"):
        get_aqi_level(invalid_aqi)


if __name__ == "__main__":
    pytest.main([__file__])
# $ python tests/aqi_cn/test_get_aqi_level.py
# ============================= test session starts ==============================
