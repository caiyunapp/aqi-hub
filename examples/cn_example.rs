//! 中国空气质量指数（AQI）计算示例
//!
//! 运行: `cargo run --example cn_example`（在项目根目录）

use aqi_hub::{
    cal_aqi_cn, cal_iaqi_cn, cal_primary_pollutant_cn, cn_item_from_str, get_aqi_level_cn,
    get_aqi_level_color_cn, DataType,
};

fn main() {
    println!("=== 中国 AQI 示例 ===\n");

    // 1. AQI 计算
    println!("1. AQI 计算");
    let (aqi, iaqi) = cal_aqi_cn(
        Some(45.0),
        Some(80.0),
        Some(35.0),
        Some(85.0),
        Some(3.0),
        Some(140.0),
        DataType::Hourly,
    );
    println!(
        "  小时值: AQI = {:?}, IAQI = pm25:{:?} pm10:{:?} ...",
        aqi, iaqi.pm25, iaqi.pm10
    );

    let (aqi2, iaqi2) = cal_aqi_cn(
        Some(120.0),
        Some(180.0),
        Some(65.0),
        Some(150.0),
        Some(8.0),
        Some(200.0),
        DataType::Daily,
    );
    println!(
        "  日均值: AQI = {:?}, IAQI = pm25:{:?} pm10:{:?}",
        aqi2, iaqi2.pm25, iaqi2.pm10
    );

    // 2. 单项 IAQI
    println!("\n2. 单项 IAQI");
    let pm25_iaqi = cal_iaqi_cn(cn_item_from_str("PM25_24H").unwrap(), 120.0);
    let pm10_iaqi = cal_iaqi_cn(cn_item_from_str("PM10_24H").unwrap(), 180.0);
    println!("  PM25_24H 120 μg/m³ → IAQI = {:?}", pm25_iaqi);
    println!("  PM10_24H 180 μg/m³ → IAQI = {:?}", pm10_iaqi);

    // 3. AQI 等级
    println!("\n3. AQI 等级 (1–6)");
    let level = get_aqi_level_cn(120);
    println!("  AQI 120 → 等级 {:?}", level);

    // 4. 等级颜色
    println!("\n4. 等级颜色");
    if let Some(c) = get_aqi_level_color_cn(1, "rgb") {
        println!("  等级 1 RGB: {:?}, RGB_HEX: {}", c.rgb, c.rgb_hex);
    }
    if let Some(c) = get_aqi_level_color_cn(4, "rgb") {
        println!("  等级 4 RGB: {:?}, RGB_HEX: {}", c.rgb, c.rgb_hex);
    }

    // 5. 首要污染物
    println!("\n5. 首要污染物");
    let primary = cal_primary_pollutant_cn(&iaqi2);
    println!("  IAQI 最大时首要污染物: {:?}", primary);

    println!("\n=== 示例结束 ===");
}
