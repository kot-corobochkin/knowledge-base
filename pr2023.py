
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import numpy as np

columns = [
    "Sector", "Enterprises", "Output Value", "Total Assets", "Working Capital", 
    "Business Revenue", "Business Cost", "Tax and Charges", "Total Profits", 
    "Pre-tax Profits", "Tax Payable", "Employed Persons"
]



# Данные из таблицы
data = [
    ["Extraction of Petroleum and Natural Gas", 3, 1061.26, 1669.15, 417.73, 973.90, 344.17, 82.08, 537.97, 702.56, 82.51, 0.55],
    ["Mining and Dressing of Ferrous Metal Ores", 9, 45.70, 50.81, 29.46, 45.25, 35.22, 0.39, 6.32, 8.18, 1.47, 0.10],
    ["Mining and Dressing of Nonferrous Metal Ores", 29, 92.65, 113.62, 35.23, 95.16, 66.37, 3.23, 16.16, 25.39, 6.00, 0.58],
    ["Mining and Dressing of Nonmetal Ores", 216, 256.38, 468.07, 153.69, 240.73, 164.73, 7.15, 23.22, 39.41, 9.04, 1.32],
    ["Mining Specialized and Auxiliary Operations", 7, 57.05, 105.91, 62.90, 56.24, 43.45, 0.11, 9.37, 10.43, 0.95, 0.17],
    ["Processing of Farm and Sideline Food", 1338, 4328.56, 2860.96, 1896.42, 4770.20, 4459.40, 8.71, 107.50, 148.77, 32.56, 15.05],
    ["Manufacture of Food", 1007, 2180.43, 2226.69, 1309.48, 2398.02, 1645.36, 14.69, 232.25, 336.30, 89.36, 19.46],
    ["Manufacture of Wine, Beverage and Refined Tea", 230, 1246.30, 1246.28, 734.95, 1311.38, 960.17, 24.08, 124.21, 189.47, 41.18, 7.43],
    ["Tobacco Products", 98, 824.76, 673.33, 525.11, 822.98, 321.13, 341.22, 78.25, 477.54, 58.07, 4.07],
    ["Textile Industry", 1756, 2257.43, 1729.41, 1055.69, 2136.08, 1825.57, 9.82, 113.79, 172.25, 48.64, 22.21],
       ["Manufacture of Textile Garments, Footwear and Headgear", 2484, 2409.95, 1702.38, 1243.40, 2209.83, 1785.02, 12.29, 97.41, 167.37, 57.67, 41.59],
    ["Leather, Fur, Feather, Down and Related Products", 1755, 1439.01, 792.57, 595.78, 1396.18, 1200.75, 6.10, 49.53, 80.53, 24.90, 30.59],
    ["Timber Processing, Bamboo, Cane, Palm Fiber & Straw Products", 537, 398.52, 426.32, 266.66, 381.46, 331.83, 1.88, 13.40, 24.50, 9.22, 4.62],
    ["Manufacture of Furniture", 1838, 2150.43, 2306.16, 1517.27, 2090.64, 1706.62, 10.50, 121.09, 176.65, 45.06, 29.61],
    ["Papermaking and Paper Products", 1566, 2637.44, 2637.17, 1471.71, 2453.72, 2183.95, 10.37, 29.59, 96.45, 56.49, 19.00],
    ["Printing and Record Medium Reproduction", 1179, 1310.68, 1621.06, 978.50, 1265.19, 1046.66, 6.01, 81.56, 113.87, 26.29, 18.65],
    ["Manufacture of Cultural, Educational, Sports and Entertainment Articles", 2094, 4020.44, 2649.68, 2107.05, 4056.29, 3631.67, 11.55, 105.20, 152.37, 35.62, 47.22],
    ["Petroleum, Coal and other Fuel Processing", 123, 5493.51, 2720.72, 920.92, 5599.09, 4697.80, 697.14, 98.21, 1103.38, 308.03, 2.45],
    ["Manufacture of Raw Chemical Materials and Chemical Products", 3496, 7384.32, 7839.61, 4367.45, 7597.59, 6260.59, 39.96, 384.88, 614.89, 190.05, 34.71],
    ["Manufacture of Medicines", 642, 2017.40, 4466.24, 2397.20, 1937.89, 1052.00, 15.42, 249.90, 344.51, 79.18, 16.70],
    ["Manufacture of Chemical Fibers", 95, 191.27, 213.23, 102.65, 187.93, 158.92, 0.89, 14.16, 18.81, 3.76, 1.34],
    ["Rubber and Plastic Products", 6461, 6118.03, 6144.30, 3789.89, 5987.08, 5002.85, 25.21, 314.83, 455.44, 115.39, 77.72],
    ["Nonmetal Mineral Products", 3904, 6351.17, 7350.30, 4508.06, 6052.55, 5161.07, 31.13, 266.22, 451.99, 154.64, 49.24],
    ["Smelting and Pressing of Ferrous Metals", 592, 4591.48, 2474.98, 1157.78, 4621.68, 4370.92, 14.84, 90.44, 158.17, 52.89, 7.87],
    ["Smelting and Pressing of Nonferrous Metals", 1273, 3973.63, 2287.21, 1673.81, 4277.11, 4033.29, 7.14, 60.07, 100.73, 33.53, 14.55],
    ["Metal Products", 7166, 8794.14, 6556.37, 4501.24, 8610.65, 7434.52, 35.39, 379.24, 586.02, 171.39, 92.17],
    ["Manufacture of General-purpose Machinery", 4218, 6157.39, 6906.15, 5023.19, 6076.04, 4893.80, 24.50, 402.45, 542.41, 115.47, 59.94],
    ["Manufacture of Special-purpose Machinery", 4230, 5936.59, 8251.90, 5950.75, 5615.13, 4170.93, 28.47, 609.56, 772.76, 134.74, 65.35],
    ["Manufacture of Automobile", 1202, 12846.58, 10917.78, 7678.42, 13315.83, 11617.85, 293.92, 529.21, 1052.15, 229.02, 49.11],
    ["Manufacture of Railway, Ship, Aeronautics and Other Transport Equipment", 543, 1595.38, 2102.75, 1518.44, 1626.75, 1431.74, 6.68, 66.22, 89.84, 16.93, 11.07],
    ["Manufacture of Electrical Machinery and Equipment", 8463, 22192.47, 24749.46, 16807.53, 21702.98, 17611.94, 89.80, 1584.71, 2207.51, 533.00, 174.15],
    ["Manufacture of Communication Equipment, Computers and Other Electronic Equipment", 9966, 47168.02, 62221.23, 42400.91, 47689.96, 38846.36, 174.93, 3628.09, 4399.55, 596.53, 317.53],
    ["Manufacture of Instruments and Meters", 1234, 1503.82, 2181.41, 1605.49, 1541.49, 1146.41, 7.48, 111.59, 158.05, 38.97, 20.27],
    ["Other Manufactures", 526, 636.39, 682.46, 525.02, 611.63, 482.63, 2.75, 40.98, 54.31, 10.58, 9.47],
    ["Comprehensive Utilization of Waste", 283, 783.85, 600.80, 359.17, 790.49, 730.80, 2.33, 19.63, 32.16, 10.21, 2.29],
    ["Manufacture of Metal Products, Machinery and Equipment Maintenance", 99, 302.55, 361.61, 250.30, 313.43, 263.91, 1.50, 22.39, 31.39, 7.50, 2.77],
    ["Production and Supply of Electric Power and Heat Power", 604, 10511.89, 23697.26, 4807.42, 10617.81, 9540.96, 45.15, 726.43, 1058.72, 287.15, 17.11],
    ["Production and Supply of Gas", 324, 3075.62, 1777.57, 650.20, 3166.36, 2953.73, 3.43, 145.80, 166.88, 17.65, 2.47],
    ["Production and Supply of Water", 406, 811.69, 3701.32, 947.61, 854.17, 630.21, 5.72, 103.38, 126.59, 17.49, 6.57],
]

df = pd.DataFrame(data, columns=columns)

# Вычисляем необходимые показатели
df["profit_per_worker"] = df["Total Profits"] / (df["Employed Persons"] * 10000)
df["avg_workers_per_enterprise"] = df["Employed Persons"] / df["Enterprises"] * 10000
# df["profitability_ratio"] = df["Total Profits"] / (df["Business Revenue"])  # Можно заменить на Value Added, если есть

total_workers = 1297.06 
df["workers_share"] = df["Employed Persons"] / total_workers * 100
total_output = 185154.19 		 # общий выпуск в млрд юаней
df["output_share"] = df["Output Value"] / total_output * 100  # в процентах
df = df[df["output_share"] > 1.0]

total_profit = 11595.24
df["profit_share"] = df["Total Profits"] / total_profit * 100	
# df["smsi"] = df["profit_per_worker"] * np.log1p(df["Employed Persons"] * 10000) * df["output_share"]

# N_max = df["Employed Persons"].max() * 10000  # переводим в человек
# # 3. Рассчитаем масштабную поправку: sqrt(N / N_max)
# df["employment_share_scaled"] = np.sqrt((df["Employed Persons"] * 10000) / N_max)
# # 4. Рассчитываем интегральный индекс масштаба и концентрации
# df["ICS"] = df["avg_workers_per_enterprise"] * df["employment_share_scaled"]


# emp_max = df["Employed Persons"].max() * 10000
# df["lrvi"] = df["profit_per_worker"] * np.sqrt(emp_max / (df["Employed Persons"] * 10000))

# N = df["Employed Persons"] * 10000
# mu = N.mean()
# k = 8 / mu  # крутизна: чем выше, тем быстрее рост

# df["employment_weight"] = 1 / (1 + np.exp(-k * (N - mu)))  # логистическая кривая

# # финальный индекс
# df["srri"] = df["profit_per_worker"] * df["employment_weight"]


# Убираем нули и пропуски
df_clean = df.dropna(subset=["profit_per_worker", "avg_workers_per_enterprise", "profit_share"])
df_clean = df_clean[(df_clean["profit_per_worker"] > 0) & (df_clean["avg_workers_per_enterprise"] > 0)]

# # Построение пузырьковой диаграммы
# fig = px.scatter(
#     df_clean,
#     x="avg_workers_per_enterprise",
#     y="profit_per_worker",
#     size="profit_share",
#     text="Sector",
#     size_max=60,
#     hover_name="Sector",
#     color="Sector",
#     labels={
#         "avg_workers_per_enterprise": "Среднее число работников на предприятие",
#         "profit_per_worker": "Прибыль на одного работника",
#         "profit_share": "Прибыль в отрасли"
#     },
#     hover_data={
#         "Sector": False,  # не дублировать в теле
#         "avg_workers_per_enterprise": True,
#         "profit_per_worker": True,
#         "profit_share": True,
#     },
#     title="Уязвимость и прибыльность отраслей"
# )

# fig.update_traces(text=None) 
# fig.update_layout(height=700)
# fig.show()

df["margin_on_sales"] = df["Total Profits"] / df["Business Revenue"] * 100
df["margin_on_cost"] = df["Total Profits"] / df["Business Cost"] * 100
df["return_on_assets"] = df["Total Profits"] / df["Total Assets"] * 100
df["profit_per_worker"] = df["Total Profits"] / df["Employed Persons"] * 100
df["return_on_working_capital"] = df["Total Profits"] / df["Working Capital"] * 100
df["worker_impact_index"] = (
    df["profit_per_worker"] *
    df["output_share"] *
    (1 - df["margin_on_sales"] / 100) *
    (df["return_on_working_capital"] / 100)
)


# Список метрик, для которых хотим посчитать z-score
metrics = [
    "margin_on_sales",
    "margin_on_cost",
    "return_on_assets",
    "profit_per_worker",
    "return_on_working_capital",
    "output_share",
    "profit_share",
    "workers_share",
    "worker_impact_index"
]

# Расчёт z-score для каждой метрики
for col in metrics:
    z_col = f"{col}_zscore"
    df[z_col] = (df[col] - df[col].mean()) / df[col].std()
    
# Убираем строки с нулями или NaN
df_clean = df.dropna(subset=[
    "margin_on_sales", "margin_on_cost", "return_on_assets", "profit_per_worker", "return_on_working_capital"
])
df_clean = df_clean[(df_clean["Total Profits"] > 0) & (df_clean["Business Revenue"] > 0)]

# Топ-10 по рентабельности продаж
top_profitable = df_clean.sort_values(by="margin_on_sales", ascending=False)


df_clean = df.dropna(subset=[
    "margin_on_sales", "margin_on_cost", "return_on_assets", "profit_per_worker", "return_on_working_capital"
])
df_clean = df_clean[(df_clean["Total Profits"] > 0) & (df_clean["Business Revenue"] > 0)]


# Топ-10 по рентабельности продаж
top_profitable = df_clean.sort_values(by="margin_on_sales", ascending=False)


import json

# result_array = df_clean.to_dict(orient="records")
# print(json.dumps(result_array, ensure_ascii=False, indent=2))    

result_array = df_clean.to_dict(orient="records")

# Сохраняем в файл JSON
with open("df_clean_results.json", "w", encoding="utf-8") as f:
    json.dump(result_array, f, ensure_ascii=False, indent=2)

print("Результаты сохранены в df_clean_results.json")

app = dash.Dash(__name__)
app.title = "Tables only"

all_columns = df_clean.columns.tolist()
# Запуск Dash
app.layout = html.Div([
    html.H4("Выберите, какие столбцы скрыть:"),
    dcc.Dropdown(
        id='column-selector',
        options=[{"label": col, "value": col} for col in all_columns],
        value=all_columns,  
        multi=True,
        placeholder="Скрыть столбцы..."
    ),
    html.P(id='table_out'), 
    html.Br(),
    dash_table.DataTable(
        id='table',
        columns=[{"name": col, "id": col} for col in all_columns],
        data=df_clean.to_dict('records'),
        sort_action='native',
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': "paleturquoise", 'fontWeight': 'bold'},
        style_data={'backgroundColor': "lavender"},
        page_size=50,
    )
])

@app.callback(
    Output('table', 'hidden_columns'),
    Input('column-selector', 'value')
)
def update_hidden_columns(selected):
    return selected 


@app.callback(
    Output('table_out', 'children'),
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        cell_data = top_profitable.iloc[active_cell['row']][active_cell['column_id']]
        return f"Значение: \"{cell_data}\" — строка: {active_cell['row']}, колонка: {active_cell['column_id']}"
    return "Нажмите на ячейку таблицы"

if __name__ == '__main__':
    app.run(debug=True)
