import re

import pytest

from aqi_hub.aqi_usa.aqi import get_aqi_level_color


@pytest.mark.parametrize(
    "aqi_level,color_type,expected_color",
    [
        # RGB 颜色测试
        (1, "RGB", (0, 228, 0)),  # 绿色
        (2, "RGB", (255, 255, 0)),  # 黄色
        (3, "RGB", (255, 126, 0)),  # 橙色
        (4, "RGB", (255, 0, 0)),  # 红色
        (5, "RGB", (143, 63, 151)),  # 紫色
        (6, "RGB", (126, 0, 35)),  # 褐红色
        # CMYK 颜色测试
        (1, "CMYK", (40, 0, 100, 0)),  # 绿色
        (2, "CMYK", (0, 0, 100, 0)),  # 黄色
        (3, "CMYK", (0, 52, 100, 0)),  # 橙色
        (4, "CMYK", (0, 100, 100, 0)),  # 红色
        (5, "CMYK", (5, 58, 0, 41)),  # 紫色
        (6, "CMYK", (30, 100, 100, 30)),  # 褐红色
        # RGB 十六进制颜色测试
        (1, "RGB_HEX", "#00E400"),  # 绿色
        (2, "RGB_HEX", "#FFFF00"),  # 黄色
        (3, "RGB_HEX", "#FF7E00"),  # 橙色
        (4, "RGB_HEX", "#FF0000"),  # 红色
        (5, "RGB_HEX", "#8F3F97"),  # 紫色
        (6, "RGB_HEX", "#7E0023"),  # 褐红色
        # CMYK 十六进制颜色测试
        (1, "CMYK_HEX", "#99FF00"),  # 绿色
        (2, "CMYK_HEX", "#FFFF00"),  # 黄色
        (3, "CMYK_HEX", "#FF7A00"),  # 橙色
        (4, "CMYK_HEX", "#FF0000"),  # 红色
        (5, "CMYK_HEX", "#8F3F96"),  # 紫色
        (6, "CMYK_HEX", "#7D0000"),  # 褐红色
    ],
    ids=lambda x: str(x),
)
def test_get_aqi_level_color_valid(aqi_level, color_type, expected_color):
    """测试不同AQI等级对应的颜色值"""
    result = get_aqi_level_color(aqi_level, color_type)
    assert result == expected_color


@pytest.mark.parametrize(
    "invalid_level,color_type,error_message",
    [
        (0, "RGB", re.escape("aqi_level must be one of [1, 2, 3, 4, 5, 6]")),
        (7, "RGB", re.escape("aqi_level must be one of [1, 2, 3, 4, 5, 6]")),
        (
            1,
            "INVALID",
            re.escape(
                "color_type must be one of ['RGB', 'CMYK', 'RGB_HEX', 'CMYK_HEX']"
            ),
        ),
    ],
    ids=["level_too_low", "level_too_high", "invalid_color_type"],
)
def test_get_aqi_level_color_invalid(invalid_level, color_type, error_message):
    """测试无效的AQI等级和颜色类型"""
    with pytest.raises(ValueError, match=error_message):
        get_aqi_level_color(invalid_level, color_type)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
