import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# Данные за 2023 и 2013
data_2023 = [
    {"Sector": "Processing of Farm and Sideline Food", "Enterprises": 1338, "Output Value": 4328.56, "Business Revenue": 4770.2, "Total Profits": 107.5, "Employed Persons": 15.05},
    {"Sector": "Manufacture of Food", "Enterprises": 1007, "Output Value": 2180.43, "Business Revenue": 2398.02, "Total Profits": 232.25, "Employed Persons": 19.46},
    {"Sector": "Textile Industry", "Enterprises": 1756, "Output Value": 2257.43, "Business Revenue": 2136.08, "Total Profits": 113.79, "Employed Persons": 22.21},
    {"Sector": "Manufacture of Textile Garments, Footwear and Headgear", "Enterprises": 2484, "Output Value": 2409.95, "Business Revenue": 2209.83, "Total Profits": 97.41, "Employed Persons": 41.59},
    {"Sector": "Manufacture of Cultural, Educational, Sports and Entertainment Articles", "Enterprises": 2094, "Output Value": 4020.44, "Business Revenue": 4056.29, "Total Profits": 105.2, "Employed Persons": 47.22},
    {"Sector": "Petroleum, Coal and other Fuel Processing", "Enterprises": 123, "Output Value": 5493.51, "Business Revenue": 5599.09, "Total Profits": 98.21, "Employed Persons": 2.45},
    {"Sector": "Manufacture of Raw Chemical Materials and Chemical Products", "Enterprises": 3496, "Output Value": 7384.32, "Business Revenue": 7597.59, "Total Profits": 384.88, "Employed Persons": 34.71},
    {"Sector": "Manufacture of Medicines", "Enterprises": 642, "Output Value": 2017.4, "Business Revenue": 1937.89, "Total Profits": 249.9, "Employed Persons": 16.7},
    {"Sector": "Rubber and Plastic Products", "Enterprises": 6461, "Output Value": 6118.03, "Business Revenue": 5987.08, "Total Profits": 314.83, "Employed Persons": 77.72},
    {"Sector": "Nonmetal Mineral Products", "Enterprises": 3904, "Output Value": 6351.17, "Business Revenue": 6052.55, "Total Profits": 266.22, "Employed Persons": 49.24},
    {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 592, "Output Value": 4591.48, "Business Revenue": 4621.68, "Total Profits": 90.44, "Employed Persons": 7.87},
    {"Sector": "Smelting and Pressing of Nonferrous Metals", "Enterprises": 1273, "Output Value": 3973.63, "Business Revenue": 4277.11, "Total Profits": 60.07, "Employed Persons": 14.55},
    {"Sector": "Metal Products", "Enterprises": 7166, "Output Value": 8794.14, "Business Revenue": 8610.65, "Total Profits": 379.24, "Employed Persons": 92.17},
    {"Sector": "Manufacture of General-purpose Machinery", "Enterprises": 4218, "Output Value": 6157.39, "Business Revenue": 6076.04, "Total Profits": 402.45, "Employed Persons": 59.94},
    {"Sector": "Manufacture of Special-purpose Machinery", "Enterprises": 4230, "Output Value": 5936.59, "Business Revenue": 5615.13, "Total Profits": 609.56, "Employed Persons": 65.35},
    {"Sector": "Manufacture of Automobile", "Enterprises": 1202, "Output Value": 12846.58, "Business Revenue": 13315.83, "Total Profits": 529.21, "Employed Persons": 49.11},
    {"Sector": "Manufacture of Electrical Machinery and Equipment", "Enterprises": 8463, "Output Value": 22192.47, "Business Revenue": 21702.98, "Total Profits": 1584.71, "Employed Persons": 174.15},
    {"Sector": "Manufacture of Communication Equipment, Computers and Other Electronic Equipment", "Enterprises": 9966, "Output Value": 47168.02, "Business Revenue": 47689.96, "Total Profits": 3628.09, "Employed Persons": 317.53},
    {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 604, "Output Value": 10511.89, "Business Revenue": 10617.81, "Total Profits": 726.43, "Employed Persons": 17.11},
    {"Sector": "Production and Supply of Gas", "Enterprises": 324, "Output Value": 3075.62, "Business Revenue": 3166.36, "Total Profits": 145.8, "Employed Persons": 2.47},
]
# 12-16  规模以上工业企业主要经济指标 (2013年)
# Main Economic Indicators of Industrial Enterprises above Designated Siz
# data_2013 = [
#     {"Sector": "Processing of Food from Agricultural Products", "Enterprises": 95, "Output Value": 4683387/10000, "Business Revenue": 4448189/10000, "Total Profits": 177896/10000, "Employed Persons": 13578/1000},
#     {"Sector": "Manufacturing of Foods", "Enterprises": 125, "Output Value": 4596574/10000, "Business Revenue": 5173074/10000, "Total Profits": 699174/10000, "Employed Persons": 62935/1000},
#     {"Sector": "Textile Industry", "Enterprises": 234, "Output Value": 2989537/10000, "Business Revenue": 2861612/10000, "Total Profits": 85092/10000, "Employed Persons": 50852/1000},
#     {"Sector": "Manufacture of Textile Wearing Apparel, Clothing", "Enterprises": 587, "Output Value": 5406914/10000, "Business Revenue": 5273886/10000, "Total Profits": 155282/10000, "Employed Persons": 151216/1000},
#     {"Sector": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", "Enterprises": 176, "Output Value": 2595319/10000, "Business Revenue": 2599521/10000, "Total Profits": 112425/10000, "Employed Persons": 84753/1000},
#     {"Sector": "Processing of Petroleum, Coking, Processing of Nuclear", "Enterprises": 12, "Output Value": 7484898/10000, "Business Revenue": 7506031/10000, "Total Profits": 77309/10000, "Employed Persons": 7320/1000},
#     {"Sector": "Manufacturing of Raw Chemical Material and Chemical Products", "Enterprises": 408, "Output Value": 18409815/10000, "Business Revenue": 17578532/10000, "Total Profits": 1787534/10000, "Employed Persons": 91450/1000},
#     {"Sector": "Manufacturing of Medical and Pharmaceutical Products", "Enterprises": 80, "Output Value": 2396958/10000, "Business Revenue": 2275736/10000, "Total Profits": 267298/10000, "Employed Persons": 33999/1000},
#     {"Sector": "Manufacture of Rubber and Plastic", "Enterprises": 317, "Output Value": 3741153/10000, "Business Revenue": 3661100/10000, "Total Profits": 110762/10000, "Employed Persons": 63779/1000},
#     {"Sector": "Manufacturing of Non-metallic Mineral Products", "Enterprises": 173, "Output Value": 1761999/10000, "Business Revenue": 1696726/10000, "Total Profits": 73436/10000, "Employed Persons": 24570/1000},
#     {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 47, "Output Value": 5408306/10000, "Business Revenue": 4869072/10000, "Total Profits": 20240/10000, "Employed Persons": 14492/1000},
#     {"Sector": "Smelting and Pressing of Non-ferrous Metals", "Enterprises": 60, "Output Value": 4694842/10000, "Business Revenue": 4163879/10000, "Total Profits": 51372/10000, "Employed Persons": 11194/1000},
#     {"Sector": "Manufacturing of Metal Products", "Enterprises": 255, "Output Value": 3762104/10000, "Business Revenue": 3428900/10000, "Total Profits": 95465/10000, "Employed Persons": 56831/1000},
#     {"Sector": "Manufacturing of General Purpose Equipment", "Enterprises": 221, "Output Value": 6454568/10000, "Business Revenue": 6144731/10000, "Total Profits": 488966/10000, "Employed Persons": 62214/1000},
#     {"Sector": "Manufacturing of Special Purpose Equipment", "Enterprises": 146, "Output Value": 1838345/10000, "Business Revenue": 1796123/10000, "Total Profits": 99969/10000, "Employed Persons": 25787/1000},
#     {"Sector": "Manufacture of Automobile", "Enterprises": 244, "Output Value": 33182791/10000, "Business Revenue": 33443560/10000, "Total Profits": 3558996/10000, "Employed Persons": 125983/1000},
#     {"Sector": "Manufacturing of Electric Machinery and Equipment", "Enterprises": 318, "Output Value": 9116579/10000, "Business Revenue": 8579104/10000, "Total Profits": 347738/10000, "Employed Persons": 105678/1000},
#     {"Sector": "Manufacture of Computers, Communications and Other Electronic Equipment", "Enterprises": 368, "Output Value": 19501481/10000, "Business Revenue": 17551506/10000, "Total Profits": 830931/10000, "Employed Persons": 216050/1000},
#     {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 21, "Output Value": 11827284/10000, "Business Revenue": 11008205/10000, "Total Profits": 1151133/10000, "Employed Persons": 23734/1000},
#     {"Sector": "Production and Supply of Gas", "Enterprises": 13, "Output Value": 2101628/10000, "Business Revenue": 1955762/10000, "Total Profits": 74015/10000, "Employed Persons": 4022/1000},
# ]
data_2013 = [
    {"Sector": "Processing of Food from Agricultural Products", "Enterprises": 906, "Output Value": 2835.51, "Business Revenue": 2747.35, "Total Profits": 134.12, "Employed Persons": 17.21},
    {"Sector": "Manufacturing of Foods", "Enterprises": 646, "Output Value": 1644.03, "Business Revenue": 1664.78, "Total Profits": 238.75, "Employed Persons": 19.91},
    {"Sector": "Textile Industry", "Enterprises": 1643, "Output Value": 2456.08, "Business Revenue": 2375.58, "Total Profits": 140.31, "Employed Persons": 43.76},
    {"Sector": "Manufacture of Textile Wearing Apparel, Clothing", "Enterprises": 3077, "Output Value": 3478.72, "Business Revenue": 3352.80, "Total Profits": 186.84, "Employed Persons": 100.92},
    {"Sector": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", "Enterprises": 1601, "Output Value": 3752.54, "Business Revenue": 3708.34, "Total Profits": 112.83, "Employed Persons": 82.45},
    {"Sector": "Processing of Petroleum, Coking, Processing of Nuclear", "Enterprises": 92, "Output Value": 3652.02, "Business Revenue": 3626.49, "Total Profits": 83.75, "Employed Persons": 2.61},
    {"Sector": "Manufacturing of Raw Chemical Material and Chemical Products", "Enterprises": 2163, "Output Value": 5461.28, "Business Revenue": 5292.94, "Total Profits": 401.07, "Employed Persons": 34.33},
    {"Sector": "Manufacturing of Medical and Pharmaceutical Products", "Enterprises": 382, "Output Value": 1222.46, "Business Revenue": 1144.59, "Total Profits": 150.13, "Employed Persons": 11.81},
    {"Sector": "Manufacture of Rubber and Plastic", "Enterprises": 3328, "Output Value": 4207.98, "Business Revenue": 4111.50, "Total Profits": 215.33, "Employed Persons": 85.46},
    {"Sector": "Manufacturing of Non-metallic Mineral Products", "Enterprises": 2448, "Output Value": 4033.36, "Business Revenue": 3825.19, "Total Profits": 270.44, "Employed Persons": 59.16},
    {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 534, "Output Value": 2587.43, "Business Revenue": 2437.64, "Total Profits": 104.67, "Employed Persons": 11.71},
    {"Sector": "Smelting and Pressing of Non-ferrous Metals", "Enterprises": 660, "Output Value": 3023.90, "Business Revenue": 2910.44, "Total Profits": 99.07, "Employed Persons": 16.30},
    {"Sector": "Manufacturing of Metal Products", "Enterprises": 3320, "Output Value": 4918.96, "Business Revenue": 4730.51, "Total Profits": 311.66, "Employed Persons": 80.05},
    {"Sector": "Manufacturing of General Purpose Equipment", "Enterprises": 1467, "Output Value": 3237.58, "Business Revenue": 3127.16, "Total Profits": 177.35, "Employed Persons": 46.38},
    {"Sector": "Manufacturing of Special Purpose Equipment", "Enterprises": 1319, "Output Value": 1856.66, "Business Revenue": 1783.19, "Total Profits": 137.73, "Employed Persons": 33.92},
    {"Sector": "Manufacture of Automobile", "Enterprises": 620, "Output Value": 4707.60, "Business Revenue": 4714.55, "Total Profits": 433.17, "Employed Persons": 32.57},
    {"Sector": "Manufacturing of Electric Machinery and Equipment", "Enterprises": 4153, "Output Value": 10895.32, "Business Revenue": 10783.39, "Total Profits": 657.85, "Employed Persons": 180.15},
    {"Sector": "Manufacture of Computers, Communications and Other Electronic Equipment", "Enterprises": 4621, "Output Value": 25835.51, "Business Revenue": 24668.39, "Total Profits": 1105.92, "Employed Persons": 330.90},
    {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 308, "Output Value": 5862.80, "Business Revenue": 5817.27, "Total Profits": 490.22, "Employed Persons": 21.13},
    {"Sector": "Production and Supply of Gas", "Enterprises": 77, "Output Value": 615.19, "Business Revenue": 594.42, "Total Profits": 50.70, "Employed Persons": 1.40},
]

data_2003 = [
    {"Sector": "Processing of Food from Agricultural Products", "Enterprises": 611, "Output Value": 503.65, "Business Revenue": 484.23, "Total Profits": 10.26, "Employed Persons": 10.41},
    {"Sector": "Manufacturing of Foods", "Enterprises": 492, "Output Value": 297.51, "Business Revenue": 275.69, "Total Profits": 22.43, "Employed Persons": 10.25},
    {"Sector": "Textile Industry", "Enterprises": 1444, "Output Value": 784.52, "Business Revenue": 736.15, "Total Profits": 13.38, "Employed Persons": 38.64},
    {"Sector": "Manufacture of Textile Wearing Apparel, Clothing", "Enterprises": 2069, "Output Value": 765.07, "Business Revenue": 725.95, "Total Profits": 9.23, "Employed Persons": 70.88},
    {"Sector": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", "Enterprises": 622, "Output Value": 333.28, "Business Revenue": 324.19, "Total Profits": 10.10, "Employed Persons": 41.03},
    {"Sector": "Processing of Petroleum, Coking, Processing of Nuclear", "Enterprises": 52, "Output Value": 553.03, "Business Revenue": 554.51, "Total Profits": 8.73, "Employed Persons": 1.82},
    {"Sector": "Manufacturing of Raw Chemical Material and Chemical Products", "Enterprises": 1310, "Output Value": 1140.98, "Business Revenue": 1109.71, "Total Profits": 108.55, "Employed Persons": 18.06},
    {"Sector": "Manufacturing of Medical and Pharmaceutical Products", "Enterprises": 280, "Output Value": 246.56, "Business Revenue": 209.60, "Total Profits": 21.71, "Employed Persons": 7.39},
    {"Sector": "Manufacture of Rubber and Plastic", "Enterprises": 1735, "Output Value": 802.17, "Business Revenue": 785.05, "Total Profits": 23.46, "Employed Persons": 39.27},
    {"Sector": "Manufacturing of Non-metallic Mineral Products", "Enterprises": 1665, "Output Value": 685.14, "Business Revenue": 639.01, "Total Profits": 18.79, "Employed Persons": 36.20},
    {"Sector": "Smelting and Pressing of Ferrous Metals", "Enterprises": 253, "Output Value": 332.26, "Business Revenue": 377.49, "Total Profits": 20.80, "Employed Persons": 4.72},
    {"Sector": "Smelting and Pressing of Non-ferrous Metals", "Enterprises": 306, "Output Value": 285.71, "Business Revenue": 270.61, "Total Profits": 6.63, "Employed Persons": 5.45},
    {"Sector": "Manufacturing of Metal Products", "Enterprises": 1870, "Output Value": 866.75, "Business Revenue": 845.39, "Total Profits": 29.72, "Employed Persons": 38.26},
    {"Sector": "Manufacturing of General Purpose Equipment", "Enterprises": 708, "Output Value": 312.47, "Business Revenue": 294.90, "Total Profits": 12.85, "Employed Persons": 12.91},
    {"Sector": "Manufacturing of Special Purpose Equipment", "Enterprises": 483, "Output Value": 218.30, "Business Revenue": 212.91, "Total Profits": 12.95, "Employed Persons": 10.00},
    {"Sector": "Manufacture of Automobile", "Enterprises": 613, "Output Value": 918.60, "Business Revenue": 915.31, "Total Profits": 95.26, "Employed Persons": 18.47},  # ~Transport Equipment Manufacturing
    {"Sector": "Manufacturing of Electric Machinery and Equipment", "Enterprises": 2190, "Output Value": 2160.43, "Business Revenue": 2081.48, "Total Profits": 79.49, "Employed Persons": 78.93},
    {"Sector": "Manufacture of Computers, Communications and Other Electronic Equipment", "Enterprises": 1768, "Output Value": 5932.21, "Business Revenue": 5732.69, "Total Profits": 246.51, "Employed Persons": 113.62},
    {"Sector": "Production and Supply of Electric Power and Heat Power", "Enterprises": 487, "Output Value": 880.31, "Business Revenue": 1683.40, "Total Profits": 131.10, "Employed Persons": 13.73},
]

# Соответствие названий
mapping = {
    "Processing of Farm and Sideline Food": "Processing of Food from Agricultural Products",
    "Manufacture of Food": "Manufacturing of Foods",
    "Textile Industry": "Textile Industry",
    "Manufacture of Textile Garments, Footwear and Headgear": "Manufacture of Textile Wearing Apparel, Clothing",
    "Manufacture of Cultural, Educational, Sports and Entertainment Articles": "Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies",
    "Petroleum, Coal and other Fuel Processing": "Processing of Petroleum, Coking, Processing of Nuclear",
    "Manufacture of Raw Chemical Materials and Chemical Products": "Manufacturing of Raw Chemical Material and Chemical Products",
    "Manufacture of Medicines": "Manufacturing of Medical and Pharmaceutical Products",
    "Rubber and Plastic Products": "Manufacture of Rubber and Plastic",
    "Nonmetal Mineral Products": "Manufacturing of Non-metallic Mineral Products",
    "Smelting and Pressing of Ferrous Metals": "Smelting and Pressing of Ferrous Metals",
    "Smelting and Pressing of Nonferrous Metals": "Smelting and Pressing of Non-ferrous Metals",
    "Metal Products": "Manufacturing of Metal Products",
    "Manufacture of General-purpose Machinery": "Manufacturing of General Purpose Equipment",
    "Manufacture of Special-purpose Machinery": "Manufacturing of Special Purpose Equipment",
    "Manufacture of Automobile": "Manufacture of Automobile",
    "Manufacture of Electrical Machinery and Equipment": "Manufacturing of Electric Machinery and Equipment",
    "Manufacture of Communication Equipment, Computers and Other Electronic Equipment": "Manufacture of Computers, Communications and Other Electronic Equipment",
    "Production and Supply of Electric Power and Heat Power": "Production and Supply of Electric Power and Heat Power",
    "Production and Supply of Gas": "Production and Supply of Gas",
}
df_2013 = pd.DataFrame(data_2013).copy()
df_2003 = pd.DataFrame(data_2003).copy()

merged = df_2013.merge(df_2003, on="Sector", suffixes=("_2013", "_2003"), how="inner")

# базовые метрики уровня 2013
merged["workers_share"] = merged["Employed Persons_2013"] / merged["Employed Persons_2013"].sum() * 100
merged["avg_workers_per_enterprise"] = (merged["Employed Persons_2013"] * 10000 / merged["Enterprises_2013"]) 
merged["output_share"] = merged["Output Value_2013"] / merged["Output Value_2013"].sum() * 100
merged["margin_on_sales"] = merged["Total Profits_2013"] / merged["Business Revenue_2013"] * 100
merged["profit_per_worker"] = merged["Total Profits_2013"] / merged["Employed Persons_2013"]

# прибыль на работника и её рост
merged["profit_per_worker_2003"] = merged["Total Profits_2003"] / merged["Employed Persons_2003"]
merged["profit_per_worker_2013"] = merged["Total Profits_2013"] / merged["Employed Persons_2013"]
# merged["Profit per Worker growth (%)"] = (
#     (merged["profit_per_worker_2013"] / merged["profit_per_worker_2003"] - 1) * 100
# )
merged["Profit per Worker growth (%)"] = (
    np.arcsinh(merged["profit_per_worker_2013"]) 
    - np.arcsinh(merged["profit_per_worker_2003"])
) * 100

# рост 2003 → 2013 по ключевым показателям
for col in ["Enterprises", "Output Value", "Business Revenue", "Total Profits", "Employed Persons"]:
    merged[f"{col}_abs_growth"] = merged[f"{col}_2013"] - merged[f"{col}_2003"]
    merged[f"{col}_pct_growth"] = (merged[f"{col}_2013"] / merged[f"{col}_2003"] - 1) * 100

# вес = доля отрасли в прибыли 2013
merged["Weight"] = merged["Total Profits_2013"] / merged["Total Profits_2013"].sum() * 100


print(
    merged[[
        "Sector",
        "Employed Persons_2003",
        "Employed Persons_2013",
        "Employed Persons_pct_growth"
    ]].to_string(index=False, float_format="{:.2f}".format)
)

total_emp_2003 = merged["Employed Persons_2003"].sum()
total_emp_2013 = merged["Employed Persons_2013"].sum()

total_growth = (total_emp_2013 - total_emp_2003) / total_emp_2003 * 100
print(f"Total employment growth: {total_growth:.2f}%")

# print(
#     merged[[
#         "Sector", 
#         "profit_per_worker_2003", 
#         "profit_per_worker_2013", 
#         "Profit per Worker growth (%)"
#     ]].to_string(index=False, float_format="{:.2f}".format)
# )




# финальная таблица (никаких *_2023 здесь быть не должно)
table = merged.sort_values("Output Value_pct_growth", ascending=False).copy()
table.insert(0, "Sector (2013 names)", table["Sector"])  # явная колонка с названием сектора

# оставляем нужные колонки
table = table[[
    "Sector (2013 names)",
    "Output Value_pct_growth",
    "Business Revenue_pct_growth",
    "Total Profits_pct_growth",
    "Employed Persons_pct_growth",
    "workers_share",
    "avg_workers_per_enterprise",
    "output_share",
    "margin_on_sales",
    "profit_per_worker",
    "Profit per Worker growth (%)",
    "Weight",
]]

# функция z-score относительно базы с защитой от std==0
def zscore_relative_to_base(series, base_value):
    std = series.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=series.index)
    return (series - base_value) / std

# базовые опоры
base_sector = "Manufacturing of Metal Products"       
base_value_avg_workers = 400
base_emp_growth = 135.57
base_profit_per_worker_growth = 0.0

# безопасное извлечение базовых значений по названию сектора
def base_value(df, sector_name, colname):
    mask = df["Sector (2013 names)"].astype(str).str.strip().eq(sector_name.strip())
    if not mask.any():
        raise ValueError(f"Сектор '{sector_name}' не найден. Доступные: {df['Sector (2013 names)'].unique()}")
    return df.loc[mask, colname].squeeze()

# компоненты индекса
table["comp_avg_workers"] = 0.20 * zscore_relative_to_base(table["avg_workers_per_enterprise"], base_value_avg_workers)

table["comp_emp_growth"] = 0.40 * zscore_relative_to_base(table["Employed Persons_pct_growth"], base_emp_growth)


# std_emp = table["Employed Persons_pct_growth"].std(ddof=0)

# print("STD =", std_emp)
# print("Base =", base_emp_growth)

# table["emp_growth_diff"] = table["Employed Persons_pct_growth"] - base_emp_growth
# table["emp_growth_zscore"] = table["emp_growth_diff"] / std_emp
# table["comp_emp_growth_calc"] = 0.40 * table["emp_growth_zscore"]

# print(table[[
#     "Sector (2013 names)",
#     "Employed Persons_pct_growth",
#     "emp_growth_diff",
#     "emp_growth_zscore",
#     "comp_emp_growth_calc",
#     "comp_emp_growth"   # оригинал
# ]].to_string(index=False, float_format="{:.2f}".format))


median_value_2013 = table["profit_per_worker"].median()


table["comp_profit_worker"] = 0.15 * (
    np.log1p(table["profit_per_worker"]) / np.log1p(median_value_2013)
)
# print("Медиана 2013 =", median_value_2013)
# print(table[["Sector (2013 names)", "avg_workers_per_enterprise"]])

table["comp_profit_per_worker_growth"] = 0.20 * zscore_relative_to_base(
    table["Profit per Worker growth (%)"], base_profit_per_worker_growth
)


def penalize(series, alpha=2):
    return np.where(series >= 0, 1 + series, 1 / (1 + np.abs(series) * alpha))

table["strike_leverage"] = (
    penalize(table["comp_avg_workers"]) *
    penalize(table["comp_emp_growth"]) *
    penalize(table["comp_profit_worker"]) *
    penalize(table["comp_profit_per_worker_growth"]) - 1
)

# вывод с компонентами
cols_to_show = [
    "Sector (2013 names)",
    "comp_avg_workers",
    "comp_emp_growth",
    "comp_profit_worker",
    "comp_profit_per_worker_growth",
    "strike_leverage"
]

print(table[cols_to_show]
      .sort_values("strike_leverage", ascending=False)
      .to_string(index=False, float_format="{:.2f}".format))


# нормировка 0–100
s = table["strike_leverage"]
table["strike_leverage_norm"] = 100 * (s - s.min()) / (s.max() - s.min())

# удобные подписи для графика
table = table.rename(columns={
    "Output Value_pct_growth": "Output growth (%)",
    "Business Revenue_pct_growth": "Revenue growth (%)",
    "Total Profits_pct_growth": "Profit growth (%)",
    "Employed Persons_pct_growth": "Employment growth (%)"
})


table["strategy_class"] = pd.qcut(
    table["strike_leverage_norm"],
    q=4,
    labels=["Низкая", "Средняя", "Высокая", "Критическая"]
)

# Подготовим массив словарей (для удобного дальнейшего использования/сериализации)
classified = (
    table
    .sort_values("strike_leverage_norm", ascending=False)
    [["Sector (2013 names)", "strike_leverage", "strike_leverage_norm", "strategy_class"]]
    .rename(columns={
        "Sector (2013 names)": "sector",
        "strike_leverage": "strategic_index_raw",
        "strike_leverage_norm": "strategic_index_norm",
        "strategy_class": "class"
    })
    .to_dict("records")
)
import json
# Печать как JSON-подобный массив
print(json.dumps(classified, ensure_ascii=False, indent=2))

# sanity-check перед графиком
needed = ["Employment growth (%)", "Profit per Worker growth (%)", "Weight", "strike_leverage"]
missing = [c for c in needed if c not in table.columns]
if missing:
    raise KeyError(f"Нет колонок для графика: {missing}")


fig = px.scatter(
    table,
    x="Employment growth (%)",
    y="Profit per Worker growth (%)",
    color="strike_leverage",
    size="Weight",
    size_max=80,
    hover_name="Sector (2013 names)",
    hover_data={
        "Output growth (%)": True,
        "Employment growth (%)": True,
        "Profit per Worker growth (%)": True,
        "profit_per_worker": True,
        "Weight": True,
        "strike_leverage": True
    },
    labels={
        "Employment growth (%)": "Рост занятости (%)",
        "Profit per Worker growth (%)": "Рост прибыли на 1 рабочего (%)",
        "Output growth (%)": "Рост выпуска (%)",
        "Weight": "Доля отрасли в прибыли (%)",
        "strike_leverage": "Индекс уязвимости"
    },
    title="Уязвимость отраслей к стачкам: рост занятости × прибыль (2003 → 2013)",
    color_continuous_scale="Plasma",
    range_color=[-1.5, 1.5]   
)
fig.update_traces(text=None, hoverinfo="all")
fig.update_layout(xaxis=dict(zeroline=True), yaxis=dict(zeroline=True),
                  margin=dict(l=40, r=40, t=60, b=40))
fig.show()