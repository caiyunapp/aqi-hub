//! China AQI (GB 3095-2026, HJ 633-2026)

/// (BP_lo, BP_hi, IAQI_lo, IAQI_hi)
type Breakpoint = (f64, f64, f64, f64);

fn iaqi_linear(concentration: f64, breakpoints: &[Breakpoint]) -> f64 {
    for &(bp_lo, bp_hi, iaqi_lo, iaqi_hi) in breakpoints {
        if concentration >= bp_lo && concentration <= bp_hi {
            return (iaqi_hi - iaqi_lo) / (bp_hi - bp_lo) * (concentration - bp_lo) + iaqi_lo;
        }
    }
    500.0
}

// PM2.5 良/轻度界限 60 (HJ 633-2026)
const PM25_BP: &[Breakpoint] = &[
    (0., 35., 0., 50.),
    (35., 60., 50., 100.),
    (60., 115., 100., 150.),
    (115., 150., 150., 200.),
    (150., 250., 200., 300.),
    (250., 350., 300., 400.),
    (350., 500., 400., 500.),
];
// PM10 良/轻度界限 120
const PM10_BP: &[Breakpoint] = &[
    (0., 50., 0., 50.),
    (50., 120., 50., 100.),
    (120., 250., 100., 150.),
    (250., 350., 150., 200.),
    (350., 420., 200., 300.),
    (420., 500., 300., 400.),
    (500., 600., 400., 500.),
];
const SO2_24H_BP: &[Breakpoint] = &[
    (0., 150., 0., 50.),
    (150., 500., 50., 100.),
    (500., 650., 100., 150.),
    (650., 800., 150., 200.),
    (800., 1600., 200., 300.),
    (1600., 2100., 300., 400.),
    (2100., 2620., 400., 500.),
];
const SO2_1H_BP: &[Breakpoint] = &[
    (0., 150., 0., 50.),
    (150., 500., 50., 100.),
    (500., 650., 100., 150.),
    (650., 800., 150., 200.),
];
const NO2_24H_BP: &[Breakpoint] = &[
    (0., 40., 0., 50.),
    (40., 80., 50., 100.),
    (80., 180., 100., 150.),
    (180., 280., 150., 200.),
    (280., 565., 200., 300.),
    (565., 750., 300., 400.),
    (750., 940., 400., 500.),
];
const NO2_1H_BP: &[Breakpoint] = &[
    (0., 100., 0., 50.),
    (100., 200., 50., 100.),
    (200., 700., 100., 150.),
    (700., 1200., 150., 200.),
    (1200., 2340., 200., 300.),
    (2340., 3090., 300., 400.),
    (3090., 3840., 400., 500.),
];
const CO_1H_BP: &[Breakpoint] = &[
    (0., 5., 0., 50.),
    (5., 10., 50., 100.),
    (10., 35., 100., 150.),
    (35., 60., 150., 200.),
    (60., 90., 200., 300.),
    (90., 120., 300., 400.),
    (120., 150., 400., 500.),
];
const CO_24H_BP: &[Breakpoint] = &[
    (0., 2., 0., 50.),
    (2., 4., 50., 100.),
    (4., 14., 100., 150.),
    (14., 24., 150., 200.),
    (24., 36., 200., 300.),
    (36., 48., 300., 400.),
    (48., 60., 400., 500.),
];
const O3_1H_BP: &[Breakpoint] = &[
    (0., 160., 0., 50.),
    (160., 200., 50., 100.),
    (200., 300., 100., 150.),
    (300., 400., 150., 200.),
    (400., 800., 200., 300.),
    (800., 1000., 300., 400.),
    (1000., 1200., 400., 500.),
];
const O3_8H_BP: &[Breakpoint] = &[
    (0., 100., 0., 50.),
    (100., 160., 50., 100.),
    (160., 215., 100., 150.),
    (215., 265., 150., 200.),
    (265., 800., 200., 300.),
];

#[derive(Clone, Copy)]
#[allow(non_camel_case_types)] // CO_1H, CO_24H 与标准/API 命名一致，不改为 Co1h/Co24h
pub enum CnItem {
    PM25_1H,
    PM25_24H,
    PM10_1H,
    PM10_24H,
    SO2_1H,
    SO2_24H,
    NO2_1H,
    NO2_24H,
    CO_1H,
    CO_24H,
    O3_1H,
    O3_8H,
}

fn breakpoints_cn(item: CnItem) -> &'static [Breakpoint] {
    match item {
        CnItem::PM25_1H | CnItem::PM25_24H => PM25_BP,
        CnItem::PM10_1H | CnItem::PM10_24H => PM10_BP,
        CnItem::SO2_1H => SO2_1H_BP,
        CnItem::SO2_24H => SO2_24H_BP,
        CnItem::NO2_1H => NO2_1H_BP,
        CnItem::NO2_24H => NO2_24H_BP,
        CnItem::CO_1H => CO_1H_BP,
        CnItem::CO_24H => CO_24H_BP,
        CnItem::O3_1H => O3_1H_BP,
        CnItem::O3_8H => O3_8H_BP,
    }
}

/// 计算单项 IAQI（中国）
/// - SO2_1H > 800 → 200；O3_8H > 800 → 300
///
/// # Examples
///
/// ```
/// use aqi_hub::{cal_iaqi_cn, CnItem};
///
/// let iaqi = cal_iaqi_cn(CnItem::PM25_24H, 35.0);
/// assert_eq!(iaqi, Some(50));
/// let iaqi_high = cal_iaqi_cn(CnItem::PM25_24H, 115.0);
/// assert_eq!(iaqi_high, Some(150));
/// ```
pub fn cal_iaqi_cn(item: CnItem, value: f64) -> Option<i32> {
    if value < 0. {
        return None;
    }
    if matches!(item, CnItem::SO2_1H) && value > 800. {
        return Some(200);
    }
    if matches!(item, CnItem::O3_8H) && value > 800. {
        return Some(300);
    }
    let bp = breakpoints_cn(item);
    let iaqi = iaqi_linear(value, bp);
    Some(iaqi.ceil() as i32)
}

#[derive(Clone, Copy)]
pub enum DataType {
    Hourly,
    Daily,
}

/// 计算 AQI（中国），返回 (AQI, IAQI 字典)
/// 任一浓度为 None 时，该污染物 IAQI 为 None
///
/// # Examples
///
/// 小时值（时均）：
///
/// ```
/// use aqi_hub::{cal_aqi_cn, DataType};
///
/// let (aqi, iaqi) = cal_aqi_cn(
///     Some(45.0), Some(80.0), Some(35.0), Some(85.0), Some(3.0), Some(140.0),
///     DataType::Hourly,
/// );
/// assert!(aqi.is_some());
/// assert!(iaqi.pm25.is_some());
/// ```
///
/// 日均值：
///
/// ```
/// use aqi_hub::{cal_aqi_cn, DataType};
///
/// let (aqi, iaqi) = cal_aqi_cn(
///     Some(60.0), Some(80.0), None, None, None, Some(100.0),
///     DataType::Daily,
/// );
/// assert_eq!(aqi, Some(100));
/// assert_eq!(iaqi.pm25, Some(100));
/// ```
pub fn cal_aqi_cn(
    pm25: Option<f64>,
    pm10: Option<f64>,
    so2: Option<f64>,
    no2: Option<f64>,
    co: Option<f64>,
    o3: Option<f64>,
    data_type: DataType,
) -> (Option<i32>, CnIaqiMap) {
    let (pm25_item, pm10_item, so2_item, no2_item, co_item, o3_item) = match data_type {
        DataType::Hourly => (
            CnItem::PM25_1H,
            CnItem::PM10_1H,
            CnItem::SO2_1H,
            CnItem::NO2_1H,
            CnItem::CO_1H,
            CnItem::O3_1H,
        ),
        DataType::Daily => (
            CnItem::PM25_24H,
            CnItem::PM10_24H,
            CnItem::SO2_24H,
            CnItem::NO2_24H,
            CnItem::CO_24H,
            CnItem::O3_8H,
        ),
    };
    let pm25_iaqi = pm25.and_then(|v| cal_iaqi_cn(pm25_item, v));
    let pm10_iaqi = pm10.and_then(|v| cal_iaqi_cn(pm10_item, v));
    let so2_iaqi = so2.and_then(|v| cal_iaqi_cn(so2_item, v));
    let no2_iaqi = no2.and_then(|v| cal_iaqi_cn(no2_item, v));
    let co_iaqi = co.and_then(|v| cal_iaqi_cn(co_item, v));
    let o3_iaqi = o3.and_then(|v| cal_iaqi_cn(o3_item, v));
    let iaqi = CnIaqiMap {
        pm25: pm25_iaqi,
        pm10: pm10_iaqi,
        so2: so2_iaqi,
        no2: no2_iaqi,
        co: co_iaqi,
        o3: o3_iaqi,
    };
    let values: Vec<i32> = [pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_iaqi]
        .into_iter()
        .flatten()
        .collect();
    let aqi = values.into_iter().max();
    (aqi, iaqi)
}

#[derive(Clone, Default)]
pub struct CnIaqiMap {
    pub pm25: Option<i32>,
    pub pm10: Option<i32>,
    pub so2: Option<i32>,
    pub no2: Option<i32>,
    pub co: Option<i32>,
    pub o3: Option<i32>,
}

impl CnIaqiMap {
    pub fn to_dict(&self) -> std::collections::HashMap<String, Option<i32>> {
        let mut m = std::collections::HashMap::new();
        m.insert("PM2.5".to_string(), self.pm25);
        m.insert("PM10".to_string(), self.pm10);
        m.insert("SO2".to_string(), self.so2);
        m.insert("NO2".to_string(), self.no2);
        m.insert("CO".to_string(), self.co);
        m.insert("O3".to_string(), self.o3);
        m
    }
    pub fn max_iaqi(&self) -> Option<i32> {
        [self.pm25, self.pm10, self.so2, self.no2, self.co, self.o3]
            .into_iter()
            .flatten()
            .max()
    }
}

/// 首要污染物：IAQI > 50 且等于最大值（中国）
///
/// # Examples
///
/// ```
/// use aqi_hub::{cal_aqi_cn, cal_primary_pollutant_cn, DataType};
///
/// let (_, iaqi) = cal_aqi_cn(
///     Some(80.0), Some(80.0), None, None, None, Some(100.0),
///     DataType::Daily,
/// );
/// let primary = cal_primary_pollutant_cn(&iaqi);
/// assert!(primary.contains(&"PM2.5".to_string()) || primary.contains(&"PM10".to_string()));
/// ```
pub fn cal_primary_pollutant_cn(iaqi: &CnIaqiMap) -> Vec<String> {
    let max_iaqi = match iaqi.max_iaqi() {
        Some(m) => m,
        None => return vec![],
    };
    if max_iaqi <= 50 {
        return vec![];
    }
    let mut out = Vec::new();
    if iaqi.pm25 == Some(max_iaqi) {
        out.push("PM2.5".to_string());
    }
    if iaqi.pm10 == Some(max_iaqi) {
        out.push("PM10".to_string());
    }
    if iaqi.so2 == Some(max_iaqi) {
        out.push("SO2".to_string());
    }
    if iaqi.no2 == Some(max_iaqi) {
        out.push("NO2".to_string());
    }
    if iaqi.co == Some(max_iaqi) {
        out.push("CO".to_string());
    }
    if iaqi.o3 == Some(max_iaqi) {
        out.push("O3".to_string());
    }
    out
}

/// AQI 等级 1–6（中国）
///
/// # Examples
///
/// ```
/// use aqi_hub::get_aqi_level_cn;
///
/// assert_eq!(get_aqi_level_cn(35), Some(1));
/// assert_eq!(get_aqi_level_cn(100), Some(2));
/// assert_eq!(get_aqi_level_cn(500), Some(6));
/// assert_eq!(get_aqi_level_cn(-1), None);
/// assert_eq!(get_aqi_level_cn(501), None);
/// ```
pub fn get_aqi_level_cn(aqi: i32) -> Option<i32> {
    if !(0..=500).contains(&aqi) {
        return None;
    }
    if aqi <= 50 {
        Some(1)
    } else if aqi <= 100 {
        Some(2)
    } else if aqi <= 150 {
        Some(3)
    } else if aqi <= 200 {
        Some(4)
    } else if aqi <= 300 {
        Some(5)
    } else {
        Some(6)
    }
}

/// 中国 AQI 等级颜色
///
/// # Examples
///
/// ```
/// use aqi_hub::get_aqi_level_color_cn;
///
/// let c = get_aqi_level_color_cn(1, "rgb").unwrap();
/// assert_eq!(c.rgb, (0, 228, 0));
/// assert_eq!(c.rgb_hex, "#00E400");
/// assert!(get_aqi_level_color_cn(0, "rgb").is_none());
/// ```
pub fn get_aqi_level_color_cn(level: i32, _color_type: &str) -> Option<ColorValue> {
    if !(1..=6).contains(&level) {
        return None;
    }
    let rgb = match level {
        1 => (0, 228, 0),
        2 => (255, 255, 0),
        3 => (255, 126, 0),
        4 => (255, 0, 0),
        5 => (153, 0, 76),
        6 => (126, 0, 35),
        _ => return None,
    };
    let cmyk = match level {
        1 => (40, 0, 100, 0),
        2 => (0, 0, 100, 0),
        3 => (0, 52, 100, 0),
        4 => (0, 100, 100, 0),
        5 => (10, 100, 40, 30),
        6 => (30, 100, 100, 30),
        _ => return None,
    };
    let rgb_hex = match level {
        1 => "#00E400",
        2 => "#FFFF00",
        3 => "#FF7E00",
        4 => "#FF0000",
        5 => "#99004C",
        6 => "#7E0023",
        _ => return None,
    };
    let cmyk_hex = match level {
        1 => "#99FF00",
        2 => "#FFFF00",
        3 => "#FF7A00",
        4 => "#FF0000",
        5 => "#A0006B",
        6 => "#7C0000",
        _ => return None,
    };
    Some(ColorValue {
        rgb,
        cmyk,
        rgb_hex: rgb_hex.to_string(),
        cmyk_hex: cmyk_hex.to_string(),
    })
}

#[derive(Clone, Debug, PartialEq)]
pub struct ColorValue {
    pub rgb: (i32, i32, i32),
    pub cmyk: (i32, i32, i32, i32),
    pub rgb_hex: String,
    pub cmyk_hex: String,
}

/// 从字符串解析中国污染物项（供 Python 等调用）
pub fn cn_item_from_str(s: &str) -> Option<CnItem> {
    match s {
        "PM25_1H" => Some(CnItem::PM25_1H),
        "PM25_24H" => Some(CnItem::PM25_24H),
        "PM10_1H" => Some(CnItem::PM10_1H),
        "PM10_24H" => Some(CnItem::PM10_24H),
        "SO2_1H" => Some(CnItem::SO2_1H),
        "SO2_24H" => Some(CnItem::SO2_24H),
        "NO2_1H" => Some(CnItem::NO2_1H),
        "NO2_24H" => Some(CnItem::NO2_24H),
        "CO_1H" => Some(CnItem::CO_1H),
        "CO_24H" => Some(CnItem::CO_24H),
        "O3_1H" => Some(CnItem::O3_1H),
        "O3_8H" => Some(CnItem::O3_8H),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pm25_iaqi() {
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 0.), Some(0));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 35.), Some(50));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 60.), Some(100));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 75.), Some(114));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_1H, 59.), Some(98));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_1H, 60.), Some(100));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 500.), Some(500));
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, 600.), Some(500));
    }

    #[test]
    fn test_pm10_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (50., 50),
            (120., 100),
            (150., 112),
            (250., 150),
            (350., 200),
            (420., 300),
            (500., 400),
            (600., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::PM10_24H, v),
                Some(exp),
                "PM10_24H {} -> {}",
                v,
                exp
            );
            assert_eq!(
                cal_iaqi_cn(CnItem::PM10_1H, v),
                Some(exp),
                "PM10_1H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_so2_24h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (150., 50),
            (500., 100),
            (650., 150),
            (800., 200),
            (1600., 300),
            (2100., 400),
            (2620., 500),
            (3000., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::SO2_24H, v),
                Some(exp),
                "SO2_24H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_so2_1h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (150., 50),
            (500., 100),
            (650., 150),
            (800., 200),
            (1600., 200),
            (2100., 200),
            (2620., 200),
            (3000., 200),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::SO2_1H, v),
                Some(exp),
                "SO2_1H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_no2_24h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (40., 50),
            (80., 100),
            (180., 150),
            (280., 200),
            (565., 300),
            (750., 400),
            (940., 500),
            (1000., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::NO2_24H, v),
                Some(exp),
                "NO2_24H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_no2_1h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (100., 50),
            (200., 100),
            (700., 150),
            (1200., 200),
            (2340., 300),
            (3090., 400),
            (3840., 500),
            (4000., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::NO2_1H, v),
                Some(exp),
                "NO2_1H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_co_24h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (2., 50),
            (4., 100),
            (14., 150),
            (24., 200),
            (36., 300),
            (48., 400),
            (60., 500),
            (100., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::CO_24H, v),
                Some(exp),
                "CO_24H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_co_1h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (5., 50),
            (10., 100),
            (35., 150),
            (60., 200),
            (90., 300),
            (120., 400),
            (150., 500),
            (200., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::CO_1H, v),
                Some(exp),
                "CO_1H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_o3_1h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (160., 50),
            (200., 100),
            (300., 150),
            (400., 200),
            (800., 300),
            (1000., 400),
            (1200., 500),
            (1500., 500),
            (2000., 500),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::O3_1H, v),
                Some(exp),
                "O3_1H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_o3_8h_iaqi() {
        for &(v, exp) in &[
            (0., 0),
            (100., 50),
            (160., 100),
            (215., 150),
            (265., 200),
            (800., 300),
            (1000., 300),
            (1200., 300),
            (1500., 300),
        ] {
            assert_eq!(
                cal_iaqi_cn(CnItem::O3_8H, v),
                Some(exp),
                "O3_8H {} -> {}",
                v,
                exp
            );
        }
    }

    #[test]
    fn test_so2_1h_over_800() {
        assert_eq!(cal_iaqi_cn(CnItem::SO2_1H, 801.), Some(200));
    }

    #[test]
    fn test_o3_8h_over_800() {
        assert_eq!(cal_iaqi_cn(CnItem::O3_8H, 1000.), Some(300));
    }

    #[test]
    fn test_iaqi_cn_negative_returns_none() {
        assert_eq!(cal_iaqi_cn(CnItem::PM25_24H, -1.), None);
    }

    #[test]
    fn test_cal_aqi_cn_hourly() {
        let (aqi, iaqi) = cal_aqi_cn(
            Some(35.),
            Some(50.),
            Some(150.),
            Some(100.),
            Some(5.),
            Some(160.),
            DataType::Hourly,
        );
        assert_eq!(aqi, Some(50));
        assert_eq!(iaqi.pm25, Some(50));
        assert_eq!(iaqi.o3, Some(50));
    }

    #[test]
    fn test_cal_aqi_cn_daily() {
        let (aqi, iaqi) = cal_aqi_cn(
            Some(35.),
            Some(50.),
            Some(150.),
            Some(40.),
            Some(2.),
            Some(100.),
            DataType::Daily,
        );
        assert_eq!(aqi, Some(50));
        assert_eq!(iaqi.o3, Some(50));
    }

    #[test]
    fn test_get_aqi_level_cn_valid() {
        let cases = [
            (0, 1),
            (25, 1),
            (50, 1),
            (51, 2),
            (75, 2),
            (100, 2),
            (101, 3),
            (125, 3),
            (150, 3),
            (151, 4),
            (175, 4),
            (200, 4),
            (201, 5),
            (250, 5),
            (300, 5),
            (301, 6),
            (400, 6),
            (500, 6),
        ];
        for (aqi, level) in cases {
            assert_eq!(
                get_aqi_level_cn(aqi),
                Some(level),
                "aqi {} -> level {}",
                aqi,
                level
            );
        }
    }

    #[test]
    fn test_get_aqi_level_cn_invalid_returns_none() {
        assert_eq!(get_aqi_level_cn(-1), None);
        assert_eq!(get_aqi_level_cn(501), None);
        assert_eq!(get_aqi_level_cn(600), None);
    }

    #[test]
    fn test_get_aqi_level_color_cn() {
        assert_eq!(
            get_aqi_level_color_cn(1, "RGB"),
            Some(ColorValue {
                rgb: (0, 228, 0),
                cmyk: (40, 0, 100, 0),
                rgb_hex: "#00E400".into(),
                cmyk_hex: "#99FF00".into()
            })
        );
        assert_eq!(
            get_aqi_level_color_cn(2, "RGB"),
            Some(ColorValue {
                rgb: (255, 255, 0),
                cmyk: (0, 0, 100, 0),
                rgb_hex: "#FFFF00".into(),
                cmyk_hex: "#FFFF00".into()
            })
        );
        assert_eq!(
            get_aqi_level_color_cn(6, "RGB_HEX").map(|c| c.rgb_hex),
            Some("#7E0023".into())
        );
        assert_eq!(
            get_aqi_level_color_cn(1, "CMYK_HEX").map(|c| c.cmyk_hex),
            Some("#99FF00".into())
        );
        assert_eq!(get_aqi_level_color_cn(0, "RGB"), None);
        assert_eq!(get_aqi_level_color_cn(7, "RGB"), None);
    }

    #[test]
    fn test_cal_primary_pollutant_cn() {
        let map = CnIaqiMap {
            pm25: Some(150),
            pm10: Some(75),
            so2: Some(50),
            no2: Some(100),
            co: Some(80),
            o3: Some(120),
        };
        assert_eq!(cal_primary_pollutant_cn(&map), vec!["PM2.5"]);

        let map2 = CnIaqiMap {
            pm25: Some(200),
            pm10: Some(200),
            so2: Some(150),
            no2: Some(180),
            co: Some(160),
            o3: Some(200),
        };
        let mut r = cal_primary_pollutant_cn(&map2);
        r.sort();
        assert_eq!(r, ["O3", "PM10", "PM2.5"]);

        let map3 = CnIaqiMap {
            pm25: Some(100),
            pm10: Some(100),
            so2: Some(100),
            no2: Some(100),
            co: Some(100),
            o3: Some(100),
        };
        let mut r3 = cal_primary_pollutant_cn(&map3);
        r3.sort();
        assert_eq!(r3, ["CO", "NO2", "O3", "PM10", "PM2.5", "SO2"]);

        let empty = CnIaqiMap::default();
        assert!(cal_primary_pollutant_cn(&empty).is_empty());

        let all_low = CnIaqiMap {
            pm25: Some(50),
            pm10: Some(40),
            so2: None,
            no2: None,
            co: None,
            o3: None,
        };
        assert!(cal_primary_pollutant_cn(&all_low).is_empty());
    }

    #[test]
    fn test_cn_item_from_str() {
        assert!(cn_item_from_str("PM25_24H").is_some());
        assert!(cn_item_from_str("INVALID").is_none());
    }
}
