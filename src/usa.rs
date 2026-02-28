//! USA AQI (EPA)

/// (BP_lo, BP_hi, IAQI_lo, IAQI_hi) - stored in original units; scale applied when comparing
type Breakpoint = (f64, f64, f64, f64);

#[derive(Clone, Copy)]
#[allow(non_camel_case_types)] // CO_8H 与标准/API 命名一致，不改为 Co8h
pub enum UsaItem {
    PM25_24H,
    PM10_24H,
    SO2_1H,
    SO2_24H,
    NO2_1H,
    CO_8H,
    O3_8H,
    O3_1H,
}

struct UsaItemConfig {
    breakpoints: &'static [Breakpoint],
    scale: f64,
    min_val: f64,
    max_val: f64,
    singularity: Option<f64>, // O3_1H min, O3_8H max, SO2_1H max, SO2_24H min
}

fn usa_config(item: UsaItem) -> UsaItemConfig {
    match item {
        UsaItem::PM25_24H => UsaItemConfig {
            breakpoints: &[
                (0., 9.0, 0., 50.),
                (9.1, 35.4, 51., 100.),
                (35.5, 55.4, 101., 150.),
                (55.5, 125.4, 151., 200.),
                (125.5, 225.4, 201., 300.),
                (225.5, 325.4, 301., 500.),
            ],
            scale: 10.,
            min_val: 0.,
            max_val: 325.4,
            singularity: None,
        },
        UsaItem::PM10_24H => UsaItemConfig {
            breakpoints: &[
                (0., 54., 0., 50.),
                (55., 154., 51., 100.),
                (155., 254., 101., 150.),
                (255., 354., 151., 200.),
                (355., 424., 201., 300.),
                (425., 604., 301., 500.),
            ],
            scale: 1.,
            min_val: 0.,
            max_val: 604.,
            singularity: None,
        },
        UsaItem::SO2_1H => UsaItemConfig {
            breakpoints: &[
                (0., 35., 0., 50.),
                (36., 75., 51., 100.),
                (76., 185., 101., 150.),
                (186., 304., 151., 200.),
            ],
            scale: 1.,
            min_val: 0.,
            max_val: 185.,
            singularity: Some(304.), // conc > 304 -> None
        },
        UsaItem::SO2_24H => UsaItemConfig {
            breakpoints: &[(305., 604., 201., 300.), (605., 1004., 301., 500.)],
            scale: 1.,
            min_val: 305.,
            max_val: 1004.,
            singularity: Some(305.), // conc < 305 -> None
        },
        UsaItem::NO2_1H => UsaItemConfig {
            breakpoints: &[
                (0., 53., 0., 50.),
                (54., 100., 51., 100.),
                (101., 360., 101., 150.),
                (361., 649., 151., 200.),
                (650., 1249., 201., 300.),
                (1250., 2049., 301., 500.),
            ],
            scale: 1.,
            min_val: 0.,
            max_val: 1249.,
            singularity: None,
        },
        UsaItem::CO_8H => UsaItemConfig {
            breakpoints: &[
                (0., 4.4, 0., 50.),
                (4.4, 9.4, 51., 100.),
                (9.5, 12.4, 101., 150.),
                (12.5, 15.4, 151., 200.),
                (15.5, 30.4, 201., 300.),
                (30.5, 50.4, 301., 500.),
            ],
            scale: 10.,
            min_val: 0.,
            max_val: 50.4,
            singularity: None,
        },
        UsaItem::O3_8H => UsaItemConfig {
            breakpoints: &[
                (0., 0.054, 0., 50.),
                (0.054, 0.070, 51., 100.),
                (0.071, 0.085, 101., 150.),
                (0.086, 0.105, 151., 200.),
                (0.106, 0.200, 201., 300.),
            ],
            scale: 1000.,
            min_val: 0.,
            max_val: 0.200,
            singularity: Some(0.201), // conc >= 0.201 -> None
        },
        UsaItem::O3_1H => UsaItemConfig {
            breakpoints: &[
                (0.125, 0.164, 101., 150.),
                (0.165, 0.204, 151., 200.),
                (0.205, 0.404, 201., 300.),
                (0.405, 0.604, 301., 500.),
            ],
            scale: 1000.,
            min_val: 0.125,
            max_val: 0.604,
            singularity: Some(0.125), // conc < 0.125 -> None
        },
    }
}

/// 计算单项 IAQI（美国）
///
/// # Examples
///
/// ```
/// use aqi_hub::{cal_iaqi_usa, UsaItem};
///
/// let iaqi = cal_iaqi_usa(UsaItem::PM25_24H, 9.0);
/// assert_eq!(iaqi, Some(50));
/// let iaqi_high = cal_iaqi_usa(UsaItem::PM25_24H, 35.5);
/// assert_eq!(iaqi_high, Some(101));
/// ```
pub fn cal_iaqi_usa(item: UsaItem, conc: f64) -> Option<i32> {
    let cfg = usa_config(item);
    let scale = cfg.scale;
    // Truncate (toward zero) to match Python int(conc*scale) and EPA decimal rules; round() can shift values across thresholds.
    let conc_scaled = (conc * scale).trunc();
    let min_scaled = (cfg.min_val * scale).trunc();
    let max_scaled = (cfg.max_val * scale).trunc();

    match item {
        UsaItem::O3_1H => {
            let sing = (cfg.singularity.unwrap() * scale).trunc();
            if conc_scaled < sing {
                return None;
            }
            if conc_scaled >= max_scaled {
                return Some(500);
            }
        }
        UsaItem::O3_8H => {
            if conc_scaled < min_scaled {
                return None;
            }
            if let Some(s) = cfg.singularity {
                let sing = (s * scale).trunc();
                if conc_scaled >= sing {
                    return None;
                }
            }
        }
        UsaItem::SO2_1H => {
            if let Some(s) = cfg.singularity {
                if conc_scaled > (s * scale).trunc() {
                    return None;
                }
            }
        }
        UsaItem::SO2_24H => {
            if let Some(s) = cfg.singularity {
                if conc_scaled < (s * scale).trunc() {
                    return None;
                }
            }
            if conc_scaled >= max_scaled {
                return Some(500);
            }
        }
        _ => {
            if conc_scaled >= max_scaled {
                return Some(500);
            }
        }
    }

    // Breakpoints are static and already in ascending order by bp_lo; no allocation/sort.
    for (bp_lo, bp_hi, iaqi_lo, iaqi_hi) in cfg.breakpoints.iter().copied() {
        let lo = (bp_lo * scale).trunc();
        let hi = (bp_hi * scale).trunc();
        if conc_scaled >= lo && conc_scaled <= hi {
            let iaqi = (iaqi_hi - iaqi_lo) * (conc_scaled - lo) / (hi - lo) + iaqi_lo;
            return Some(iaqi as i32); // truncate to match Python int()
        }
    }
    None
}

#[derive(Clone, Default)]
pub struct UsaIaqiMap {
    pub pm25: Option<i32>,
    pub pm10: Option<i32>,
    pub so2: Option<i32>,
    pub no2: Option<i32>,
    pub co: Option<i32>,
    pub o3: Option<i32>,
}

/// 计算美国 AQI；SO2 取 1h/24h 最大，O3 取 8h/1h 最大
#[allow(clippy::too_many_arguments)] // API 与 Python 一致，参数固定
///
/// # Examples
///
/// ```
/// use aqi_hub::cal_aqi_usa;
///
/// let (aqi, iaqi) = cal_aqi_usa(5.0, 40.0, None, 40.0, 2.0, 0.04, None, None);
/// assert_eq!(aqi, Some(37));
/// assert_eq!(iaqi.pm10, Some(37));
/// ```
pub fn cal_aqi_usa(
    pm25: f64,
    pm10: f64,
    so2_1h: Option<f64>,
    no2: f64,
    co: f64,
    o3_8h: f64,
    so2_24h: Option<f64>,
    o3_1h: Option<f64>,
) -> (Option<i32>, UsaIaqiMap) {
    let pm25_iaqi = cal_iaqi_usa(UsaItem::PM25_24H, pm25);
    let pm10_iaqi = cal_iaqi_usa(UsaItem::PM10_24H, pm10);
    let so2_1h_iaqi = so2_1h.and_then(|v| cal_iaqi_usa(UsaItem::SO2_1H, v));
    let so2_24h_iaqi = so2_24h.and_then(|v| cal_iaqi_usa(UsaItem::SO2_24H, v));
    let so2_iaqi = [so2_1h_iaqi, so2_24h_iaqi].into_iter().flatten().max();
    let no2_iaqi = cal_iaqi_usa(UsaItem::NO2_1H, no2);
    let co_iaqi = cal_iaqi_usa(UsaItem::CO_8H, co);
    let o3_8h_iaqi = cal_iaqi_usa(UsaItem::O3_8H, o3_8h);
    let o3_1h_iaqi = o3_1h.and_then(|v| cal_iaqi_usa(UsaItem::O3_1H, v));
    let o3_iaqi = [o3_8h_iaqi, o3_1h_iaqi].into_iter().flatten().max();

    let iaqi = UsaIaqiMap {
        pm25: pm25_iaqi,
        pm10: pm10_iaqi,
        so2: so2_iaqi,
        no2: no2_iaqi,
        co: co_iaqi,
        o3: o3_iaqi,
    };
    let aqi = [pm25_iaqi, pm10_iaqi, so2_iaqi, no2_iaqi, co_iaqi, o3_iaqi]
        .into_iter()
        .flatten()
        .max();
    (aqi, iaqi)
}

/// 首要污染物：等于最大 IAQI（美国，无 >50 限制）
///
/// # Examples
///
/// ```
/// use aqi_hub::{cal_aqi_usa, cal_primary_pollutant_usa};
///
/// let (_, iaqi) = cal_aqi_usa(150.0, 150.0, Some(30.0), 100.0, 4.0, 0.07, None, None);
/// let primary = cal_primary_pollutant_usa(&iaqi);
/// assert!(!primary.is_empty());
/// ```
pub fn cal_primary_pollutant_usa(iaqi: &UsaIaqiMap) -> Vec<String> {
    let max_iaqi = {
        let v = [iaqi.pm25, iaqi.pm10, iaqi.so2, iaqi.no2, iaqi.co, iaqi.o3];
        v.into_iter().flatten().max()
    };
    let Some(m) = max_iaqi else {
        return vec![];
    };
    let mut out = Vec::new();
    if iaqi.pm25 == Some(m) {
        out.push("PM2.5".to_string());
    }
    if iaqi.pm10 == Some(m) {
        out.push("PM10".to_string());
    }
    if iaqi.so2 == Some(m) {
        out.push("SO2".to_string());
    }
    if iaqi.no2 == Some(m) {
        out.push("NO2".to_string());
    }
    if iaqi.co == Some(m) {
        out.push("CO".to_string());
    }
    if iaqi.o3 == Some(m) {
        out.push("O3".to_string());
    }
    out
}

/// AQI 等级 1–6（美国）
///
/// # Examples
///
/// ```
/// use aqi_hub::get_aqi_level_usa;
///
/// assert_eq!(get_aqi_level_usa(35), 1);
/// assert_eq!(get_aqi_level_usa(100), 2);
/// assert_eq!(get_aqi_level_usa(500), 6);
/// ```
pub fn get_aqi_level_usa(aqi: i32) -> i32 {
    if aqi <= 50 {
        1
    } else if aqi <= 100 {
        2
    } else if aqi <= 150 {
        3
    } else if aqi <= 200 {
        4
    } else if aqi <= 300 {
        5
    } else {
        6
    }
}

/// 美国 AQI 等级颜色（紫色与中国的 RGB 不同）
///
/// # Examples
///
/// ```
/// use aqi_hub::get_aqi_level_color_usa;
///
/// let c = get_aqi_level_color_usa(5, "rgb").unwrap();
/// assert_eq!(c.rgb, (143, 63, 151));
/// assert_eq!(c.rgb_hex, "#8F3F97");
/// assert!(get_aqi_level_color_usa(0, "rgb").is_none());
/// ```
pub fn get_aqi_level_color_usa(level: i32, _color_type: &str) -> Option<UsaColorValue> {
    if !(1..=6).contains(&level) {
        return None;
    }
    let rgb = match level {
        1 => (0, 228, 0),
        2 => (255, 255, 0),
        3 => (255, 126, 0),
        4 => (255, 0, 0),
        5 => (143, 63, 151),
        6 => (126, 0, 35),
        _ => return None,
    };
    let cmyk = match level {
        1 => (40, 0, 100, 0),
        2 => (0, 0, 100, 0),
        3 => (0, 52, 100, 0),
        4 => (0, 100, 100, 0),
        5 => (5, 58, 0, 41),
        6 => (30, 100, 100, 30),
        _ => return None,
    };
    let rgb_hex = match level {
        1 => "#00E400",
        2 => "#FFFF00",
        3 => "#FF7E00",
        4 => "#FF0000",
        5 => "#8F3F97",
        6 => "#7E0023",
        _ => return None,
    };
    let cmyk_hex = match level {
        1 => "#99FF00",
        2 => "#FFFF00",
        3 => "#FF7A00",
        4 => "#FF0000",
        5 => "#8F3F96",
        6 => "#7D0000",
        _ => return None,
    };
    Some(UsaColorValue {
        rgb,
        cmyk,
        rgb_hex: rgb_hex.to_string(),
        cmyk_hex: cmyk_hex.to_string(),
    })
}

#[derive(Clone, Debug, PartialEq)]
pub struct UsaColorValue {
    pub rgb: (i32, i32, i32),
    pub cmyk: (i32, i32, i32, i32),
    pub rgb_hex: String,
    pub cmyk_hex: String,
}

pub fn usa_item_from_str(s: &str) -> Option<UsaItem> {
    match s {
        "PM25_24H" => Some(UsaItem::PM25_24H),
        "PM10_24H" => Some(UsaItem::PM10_24H),
        "SO2_1H" => Some(UsaItem::SO2_1H),
        "SO2_24H" => Some(UsaItem::SO2_24H),
        "NO2_1H" => Some(UsaItem::NO2_1H),
        "CO_8H" => Some(UsaItem::CO_8H),
        "O3_8H" => Some(UsaItem::O3_8H),
        "O3_1H" => Some(UsaItem::O3_1H),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cal_aqi_usa_1() {
        let (aqi, iaqi) = cal_aqi_usa(5.0, 40.0, Some(20.0), 40.0, 2.0, 0.040, None, None);
        assert_eq!(aqi, Some(37));
        assert_eq!(iaqi.pm10, Some(37));
    }

    #[test]
    fn test_cal_aqi_usa_2() {
        let (aqi, _) = cal_aqi_usa(150.5, 150.0, Some(30.0), 100.0, 4.0, 0.070, None, None);
        assert_eq!(aqi, Some(225));
    }

    #[test]
    fn test_cal_aqi_usa_extreme() {
        let (aqi, _) = cal_aqi_usa(
            600.0,
            900.0,
            Some(400.0),
            2500.0,
            60.0,
            0.25,
            None,
            Some(0.7),
        );
        assert_eq!(aqi, Some(500));
    }

    #[test]
    fn test_cal_iaqi_usa_pm25() {
        for &(conc, exp) in &[
            (0.0, 0),
            (9.0, 50),
            (9.1, 51),
            (35.4, 100),
            (125.4, 200),
            (325.4, 500),
            (425.4, 500),
        ] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::PM25_24H, conc),
                Some(exp),
                "PM25_24H {} -> {}",
                conc,
                exp
            );
        }
    }

    #[test]
    fn test_cal_iaqi_usa_pm10() {
        for &(conc, exp) in &[
            (0.0, 0),
            (54.0, 50),
            (154.0, 100),
            (424.0, 300),
            (504.0, 388),
            (604.0, 500),
        ] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::PM10_24H, conc),
                Some(exp),
                "PM10_24H {} -> {}",
                conc,
                exp
            );
        }
    }

    #[test]
    fn test_cal_iaqi_usa_co8h() {
        for &(conc, exp) in &[(0.0, 0), (4.4, 50), (9.4, 100), (15.4, 200), (50.4, 500)] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::CO_8H, conc),
                Some(exp),
                "CO_8H {} -> {}",
                conc,
                exp
            );
        }
    }

    #[test]
    fn test_cal_iaqi_usa_no2() {
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 0.0), Some(0));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 53.0), Some(50));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 100.0), Some(100));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 360.0), Some(150));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 649.0), Some(200));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 1249.0), Some(500));
        assert_eq!(cal_iaqi_usa(UsaItem::NO2_1H, 2049.0), Some(500));
    }

    #[test]
    fn test_cal_iaqi_usa_so2_1h() {
        for &(conc, exp) in &[
            (0.0, 0),
            (35.0, 50),
            (75.0, 100),
            (185.0, 150),
            (304.0, 200),
        ] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::SO2_1H, conc),
                Some(exp),
                "SO2_1H {} -> {}",
                conc,
                exp
            );
        }
        assert_eq!(cal_iaqi_usa(UsaItem::SO2_1H, 305.0), None);
    }

    #[test]
    fn test_cal_iaqi_usa_so2_24h() {
        assert_eq!(cal_iaqi_usa(UsaItem::SO2_24H, 304.0), None);
        for &(conc, exp) in &[(305.0, 201), (605.0, 301), (1005.0, 500), (1205.0, 500)] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::SO2_24H, conc),
                Some(exp),
                "SO2_24H {} -> {}",
                conc,
                exp
            );
        }
    }

    #[test]
    fn test_cal_iaqi_usa_o3_8h() {
        for &(conc, exp) in &[
            (0.0, 0),
            (0.054, 50),
            (0.070, 100),
            (0.085, 150),
            (0.105, 200),
        ] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::O3_8H, conc),
                Some(exp),
                "O3_8H {} -> {}",
                conc,
                exp
            );
        }
        assert_eq!(cal_iaqi_usa(UsaItem::O3_8H, 0.201), None);
    }

    #[test]
    fn test_cal_iaqi_usa_o3_1h() {
        assert_eq!(cal_iaqi_usa(UsaItem::O3_1H, 0.124), None);
        for &(conc, exp) in &[
            (0.125, 101),
            (0.164, 150),
            (0.204, 200),
            (0.404, 300),
            (0.604, 500),
        ] {
            assert_eq!(
                cal_iaqi_usa(UsaItem::O3_1H, conc),
                Some(exp),
                "O3_1H {} -> {}",
                conc,
                exp
            );
        }
        assert_eq!(cal_iaqi_usa(UsaItem::O3_1H, 0.605), Some(500));
    }

    #[test]
    fn test_get_aqi_level_usa_valid() {
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
                get_aqi_level_usa(aqi),
                level,
                "aqi {} -> level {}",
                aqi,
                level
            );
        }
    }

    #[test]
    fn test_get_aqi_level_color_usa() {
        let c1 = get_aqi_level_color_usa(1, "RGB").unwrap();
        assert_eq!(c1.rgb, (0, 228, 0));
        assert_eq!(c1.rgb_hex, "#00E400");
        let c5 = get_aqi_level_color_usa(5, "RGB").unwrap();
        assert_eq!(c5.rgb, (143, 63, 151));
        assert_eq!(c5.rgb_hex, "#8F3F97");
        assert_eq!(
            get_aqi_level_color_usa(6, "CMYK_HEX").unwrap().cmyk_hex,
            "#7D0000"
        );
        assert!(get_aqi_level_color_usa(0, "RGB").is_none());
        assert!(get_aqi_level_color_usa(7, "RGB").is_none());
    }

    #[test]
    fn test_cal_primary_pollutant_usa() {
        let map = UsaIaqiMap {
            pm25: Some(150),
            pm10: Some(75),
            so2: Some(50),
            no2: Some(100),
            co: Some(80),
            o3: Some(120),
        };
        assert_eq!(cal_primary_pollutant_usa(&map), vec!["PM2.5"]);

        let map2 = UsaIaqiMap {
            pm25: Some(200),
            pm10: Some(200),
            so2: Some(150),
            no2: Some(180),
            co: Some(160),
            o3: Some(200),
        };
        let mut r = cal_primary_pollutant_usa(&map2);
        r.sort();
        assert_eq!(r, ["O3", "PM10", "PM2.5"]);

        let map3 = UsaIaqiMap {
            pm25: Some(100),
            pm10: Some(100),
            so2: Some(100),
            no2: Some(100),
            co: Some(100),
            o3: Some(100),
        };
        let mut r3 = cal_primary_pollutant_usa(&map3);
        r3.sort();
        assert_eq!(r3, ["CO", "NO2", "O3", "PM10", "PM2.5", "SO2"]);

        assert_eq!(
            cal_primary_pollutant_usa(&UsaIaqiMap::default()),
            Vec::<String>::new()
        );

        let all_none = UsaIaqiMap {
            pm25: None,
            pm10: None,
            so2: None,
            no2: None,
            co: None,
            o3: None,
        };
        assert!(cal_primary_pollutant_usa(&all_none).is_empty());

        let single = UsaIaqiMap {
            pm25: Some(75),
            pm10: None,
            so2: None,
            no2: None,
            co: None,
            o3: None,
        };
        assert_eq!(cal_primary_pollutant_usa(&single), vec!["PM2.5"]);
    }

    #[test]
    fn test_usa_item_from_str() {
        assert!(usa_item_from_str("PM25_24H").is_some());
        assert!(usa_item_from_str("O3_1H").is_some());
        assert!(usa_item_from_str("INVALID").is_none());
    }
}
