//! AQI Hub: Air quality index calculation (China GB 3095-2026 / HJ 633-2026, USA EPA).
//!
//! # Examples
//!
//! ## 中国 AQI（时均 / 日均）
//!
//! 小时值（时均，用 `DataType::Hourly`）：
//!
//! ```rust
//! use aqi_hub_native::{cal_aqi_cn, cal_primary_pollutant_cn, get_aqi_level_cn, get_aqi_level_color_cn, DataType};
//!
//! let (aqi, iaqi) = cal_aqi_cn(
//!     Some(45.0), Some(80.0), Some(35.0), Some(85.0), Some(3.0), Some(140.0),
//!     DataType::Hourly,
//! );
//! assert!(aqi.is_some());
//! let _ = cal_primary_pollutant_cn(&iaqi);
//! let _ = get_aqi_level_cn(aqi.unwrap());
//! ```
//!
//! 日均值（用 `DataType::Daily`）：
//!
//! ```rust
//! use aqi_hub_native::{cal_aqi_cn, cal_primary_pollutant_cn, get_aqi_level_cn, get_aqi_level_color_cn, DataType};
//!
//! let (aqi, iaqi) = cal_aqi_cn(
//!     Some(60.0), Some(80.0), None, None, None, Some(100.0),
//!     DataType::Daily,
//! );
//! assert_eq!(aqi, Some(100));
//! let primary = cal_primary_pollutant_cn(&iaqi);
//! let level = get_aqi_level_cn(aqi.unwrap());
//! let color = get_aqi_level_color_cn(level.unwrap(), "rgb");
//! ```
//!
//! ## 美国 AQI
//!
//! ```rust
//! use aqi_hub_native::{cal_aqi_usa, cal_primary_pollutant_usa, get_aqi_level_usa, get_aqi_level_color_usa};
//!
//! // PM2.5=5 μg/m³, PM10=40, NO2=40 ppb, CO=2 ppm, O3_8h=0.04 ppm
//! let (aqi, iaqi) = cal_aqi_usa(5.0, 40.0, None, 40.0, 2.0, 0.04, None, None);
//! assert!(aqi.is_some());
//! let primary = cal_primary_pollutant_usa(&iaqi);
//! let level = get_aqi_level_usa(aqi.unwrap());
//! let color = get_aqi_level_color_usa(level, "rgb");
//! ```

pub mod cn;
pub mod usa;

pub use cn::{
    cal_aqi_cn, cal_iaqi_cn, cal_primary_pollutant_cn, cn_item_from_str, get_aqi_level_cn,
    get_aqi_level_color_cn, CnIaqiMap, CnItem, ColorValue, DataType,
};
pub use usa::{
    cal_aqi_usa, cal_iaqi_usa, cal_primary_pollutant_usa, get_aqi_level_color_usa,
    get_aqi_level_usa, usa_item_from_str, UsaColorValue, UsaIaqiMap, UsaItem,
};

#[cfg(feature = "python")]
mod python;
#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn _native(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()> {
    python::register(m)
}
