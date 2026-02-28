//! 美国空气质量指数（AQI）计算示例
//!
//! 运行: `cargo run --example us_example`（在项目根目录）
//!
//! 浓度单位: PM2.5/PM10 μg/m³, SO2/NO2 ppb, CO/O3 ppm

use aqi_hub::{
    cal_aqi_usa, cal_iaqi_usa, cal_primary_pollutant_usa, get_aqi_level_color_usa,
    get_aqi_level_usa, usa_item_from_str,
};

fn main() {
    println!("=== 美国 AQI 示例 ===\n");

    // 1. AQI 计算
    println!("1. AQI 计算");
    let (aqi, iaqi) = cal_aqi_usa(
        120.0,      // pm25 μg/m³
        180.0,      // pm10
        Some(65.0), // so2_1h ppb
        150.0,      // no2 ppb
        8.0,        // co ppm
        0.200,      // o3_8h ppm
        None,       // so2_24h
        None,       // o3_1h
    );
    println!("  AQI = {:?}", aqi);
    println!(
        "  IAQI: pm25={:?}, pm10={:?}, so2={:?}, no2={:?}, co={:?}, o3={:?}",
        iaqi.pm25, iaqi.pm10, iaqi.so2, iaqi.no2, iaqi.co, iaqi.o3
    );

    // 2. 单项 IAQI
    println!("\n2. 单项 IAQI");
    let pm25_iaqi = cal_iaqi_usa(usa_item_from_str("PM25_24H").unwrap(), 120.0);
    let pm10_iaqi = cal_iaqi_usa(usa_item_from_str("PM10_24H").unwrap(), 180.0);
    let o3_8h_iaqi = cal_iaqi_usa(usa_item_from_str("O3_8H").unwrap(), 0.200);
    println!("  PM25_24H 120 μg/m³ → IAQI = {:?}", pm25_iaqi);
    println!("  PM10_24H 180 μg/m³ → IAQI = {:?}", pm10_iaqi);
    println!("  O3_8H 0.200 ppm → IAQI = {:?}", o3_8h_iaqi);

    // 3. AQI 等级
    println!("\n3. AQI 等级 (1–6)");
    let level = get_aqi_level_usa(aqi.unwrap_or(0));
    println!("  AQI {:?} → 等级 {}", aqi, level);

    // 4. 等级颜色
    println!("\n4. 等级颜色");
    if let Some(c) = get_aqi_level_color_usa(1, "rgb") {
        println!("  等级 1 RGB: {:?}, RGB_HEX: {}", c.rgb, c.rgb_hex);
    }
    if let Some(c) = get_aqi_level_color_usa(5, "rgb") {
        println!("  等级 5 (紫) RGB: {:?}, RGB_HEX: {}", c.rgb, c.rgb_hex);
    }

    // 5. 首要污染物
    println!("\n5. 首要污染物");
    let primary = cal_primary_pollutant_usa(&iaqi);
    println!("  Primary pollutant(s): {:?}", primary);

    println!("\n=== 示例结束 ===");
}
