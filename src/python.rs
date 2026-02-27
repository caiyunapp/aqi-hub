//! PyO3 bindings for aqi-hub (feature "python")

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::cn::{self, CnIaqiMap, DataType};
use crate::usa::{self, UsaIaqiMap};

#[pyfunction(signature = (pm25=None, pm10=None, so2=None, no2=None, co=None, o3=None, data_type="hourly"))]
fn cal_aqi_cn(
    py: Python<'_>,
    pm25: Option<f64>,
    pm10: Option<f64>,
    so2: Option<f64>,
    no2: Option<f64>,
    co: Option<f64>,
    o3: Option<f64>,
    data_type: &str,
) -> PyResult<(Option<i32>, PyObject)> {
    let dt = match data_type {
        "hourly" => DataType::Hourly,
        "daily" => DataType::Daily,
        _ => {
            return Err(PyValueError::new_err(
                "data_type must be 'hourly' or 'daily'",
            ))
        }
    };
    let (aqi, iaqi) = cn::cal_aqi_cn(pm25, pm10, so2, no2, co, o3, dt);
    let dict = PyDict::new_bound(py);
    dict.set_item("PM2.5", iaqi.pm25)?;
    dict.set_item("PM10", iaqi.pm10)?;
    dict.set_item("SO2", iaqi.so2)?;
    dict.set_item("NO2", iaqi.no2)?;
    dict.set_item("CO", iaqi.co)?;
    dict.set_item("O3", iaqi.o3)?;
    Ok((aqi, dict.into_py(py)))
}

#[pyfunction(signature = (item, value=None))]
fn cal_iaqi_cn(item: &str, value: Option<f64>) -> PyResult<Option<i32>> {
    let item_enum = cn::cn_item_from_str(item).ok_or_else(|| {
        PyValueError::new_err(format!(
            "item must be one of valid CN pollutant keys, got {}",
            item
        ))
    })?;
    let v = match value {
        Some(x) if x >= 0. => x,
        _ => return Ok(None),
    };
    Ok(cn::cal_iaqi_cn(item_enum, v))
}

#[pyfunction(signature = (aqi=None))]
fn get_aqi_level_cn(aqi: Option<i32>) -> PyResult<Option<i32>> {
    if let Some(x) = aqi {
        if x < 0 || x > 500 {
            return Err(PyValueError::new_err("AQI must be between 0 and 500"));
        }
    }
    Ok(aqi.and_then(cn::get_aqi_level_cn))
}

#[pyfunction]
fn get_aqi_level_color_cn(py: Python<'_>, level: i32, color_type: &str) -> PyResult<PyObject> {
    let color = cn::get_aqi_level_color_cn(level, color_type).ok_or_else(|| {
        PyValueError::new_err("aqi_level must be 1-6, color_type must be RGB/CMYK/RGB_HEX/CMYK_HEX")
    })?;
    let ret: PyObject = match color_type {
        "RGB" => (color.rgb.0, color.rgb.1, color.rgb.2).into_py(py),
        "CMYK" => (color.cmyk.0, color.cmyk.1, color.cmyk.2, color.cmyk.3).into_py(py),
        "RGB_HEX" => color.rgb_hex.into_py(py),
        "CMYK_HEX" => color.cmyk_hex.into_py(py),
        _ => {
            return Err(PyValueError::new_err(
                "color_type must be RGB, CMYK, RGB_HEX, or CMYK_HEX",
            ))
        }
    };
    Ok(ret)
}

fn iaqi_dict_to_cn_map(_py: Python<'_>, dict: &Bound<'_, PyDict>) -> PyResult<CnIaqiMap> {
    let get = |k: &str| -> Option<i32> {
        dict.get_item(k)
            .ok()
            .flatten()
            .and_then(|v| v.extract::<i32>().ok())
    };
    Ok(CnIaqiMap {
        pm25: get("PM2.5"),
        pm10: get("PM10"),
        so2: get("SO2"),
        no2: get("NO2"),
        co: get("CO"),
        o3: get("O3"),
    })
}

#[pyfunction]
fn cal_primary_pollutant_cn(iaqi_dict: &Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let py = iaqi_dict.py();
    let map = iaqi_dict_to_cn_map(py, iaqi_dict)?;
    Ok(cn::cal_primary_pollutant_cn(&map))
}

// --- USA ---

#[pyfunction(signature = (pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h=None, o3_1h=None))]
fn cal_aqi_usa(
    py: Python<'_>,
    pm25: f64,
    pm10: f64,
    so2_1h: Option<f64>,
    no2: f64,
    co: f64,
    o3_8h: f64,
    so2_24h: Option<f64>,
    o3_1h: Option<f64>,
) -> (Option<i32>, PyObject) {
    let (aqi, iaqi) = usa::cal_aqi_usa(pm25, pm10, so2_1h, no2, co, o3_8h, so2_24h, o3_1h);
    let dict = PyDict::new_bound(py);
    let _ = dict.set_item("PM2.5", iaqi.pm25);
    let _ = dict.set_item("PM10", iaqi.pm10);
    let _ = dict.set_item("SO2", iaqi.so2);
    let _ = dict.set_item("NO2", iaqi.no2);
    let _ = dict.set_item("CO", iaqi.co);
    let _ = dict.set_item("O3", iaqi.o3);
    (aqi, dict.into_py(py))
}

#[pyfunction(signature = (conc=None, *, item))]
fn cal_iaqi_usa(conc: Option<f64>, item: &str) -> PyResult<Option<i32>> {
    let item_enum = usa::usa_item_from_str(item)
        .ok_or_else(|| PyValueError::new_err(format!("item: {} must be one of dict_keys", item)))?;
    let c = match conc {
        Some(x) => x,
        None => return Ok(None),
    };
    Ok(usa::cal_iaqi_usa(item_enum, c))
}

#[pyfunction]
fn get_aqi_level_usa(aqi: i32) -> PyResult<i32> {
    if aqi < 0 || aqi > 500 {
        return Err(PyValueError::new_err("AQI must be between 0 and 500"));
    }
    Ok(usa::get_aqi_level_usa(aqi))
}

#[pyfunction]
fn get_aqi_level_color_usa(py: Python<'_>, level: i32, color_type: &str) -> PyResult<PyObject> {
    if level < 1 || level > 6 {
        return Err(PyValueError::new_err(
            "aqi_level must be one of [1, 2, 3, 4, 5, 6]",
        ));
    }
    let valid_color_types = ["RGB", "CMYK", "RGB_HEX", "CMYK_HEX"];
    if !valid_color_types.contains(&color_type) {
        return Err(PyValueError::new_err(
            "color_type must be one of ['RGB', 'CMYK', 'RGB_HEX', 'CMYK_HEX']",
        ));
    }
    let color =
        usa::get_aqi_level_color_usa(level, color_type).expect("level and color_type validated");
    let ret: PyObject = match color_type {
        "RGB" => (color.rgb.0, color.rgb.1, color.rgb.2).into_py(py),
        "CMYK" => (color.cmyk.0, color.cmyk.1, color.cmyk.2, color.cmyk.3).into_py(py),
        "RGB_HEX" => color.rgb_hex.into_py(py),
        "CMYK_HEX" => color.cmyk_hex.into_py(py),
        _ => unreachable!(),
    };
    Ok(ret)
}

fn iaqi_dict_to_usa_map(_py: Python<'_>, dict: &Bound<'_, PyDict>) -> PyResult<UsaIaqiMap> {
    let get = |k: &str| -> Option<i32> {
        dict.get_item(k)
            .ok()
            .flatten()
            .and_then(|v| v.extract::<i32>().ok())
    };
    Ok(UsaIaqiMap {
        pm25: get("PM2.5"),
        pm10: get("PM10"),
        so2: get("SO2"),
        no2: get("NO2"),
        co: get("CO"),
        o3: get("O3"),
    })
}

#[pyfunction]
fn cal_primary_pollutant_usa(iaqi_dict: &Bound<'_, PyDict>) -> PyResult<Vec<String>> {
    let py = iaqi_dict.py();
    let map = iaqi_dict_to_usa_map(py, iaqi_dict)?;
    Ok(usa::cal_primary_pollutant_usa(&map))
}

/// Register all Python bindings into the module
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_aqi_cn, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_iaqi_cn, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(get_aqi_level_cn, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(get_aqi_level_color_cn, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_primary_pollutant_cn, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_aqi_usa, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_iaqi_usa, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(get_aqi_level_usa, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(get_aqi_level_color_usa, m)?)?;
    m.add_function(pyo3::wrap_pyfunction_bound!(cal_primary_pollutant_usa, m)?)?;
    Ok(())
}
