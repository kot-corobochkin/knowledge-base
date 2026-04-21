import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import numpy as np

columns = [
    "Sector", 
    "Enterprises", "Loss-making Enterprises",
    "Output Value", "Value-added",
    "Sales Value of Industry",
    "Business Revenue",
    "Business Cost",
    "Taxes and Charges on Core Business",
    "Total Profits", "Pre-tax Profits",
    "Income Tax Payable", "Value-added Tax Payable",
    "Working Capital",
    "Accounts Receivable", "Inventory",
    "Finished Goods Inventory",
    "Original Value of Fixed Assets at Year-end",
    "Accumulated Depreciation", "Net Value of Fixed Assets",
    "Total Assets", "Total Liabilities at Year-end (10k yuan)",
    "Total Owners' Equity at Year-end (10k yuan)",
    "Employed Persons"
]

data = [
    # ["Total", 4812, 652, 171987181, 44491105, 169212664, 165067607, 135511005, 3651929, 
    #     11053751, 19831196, 1902197, 5125516, 74129378, 22431370, 16005082, 5540642,
    #     62689307, 27733794, 34955513, 135540623, 73585807, 61954816, 1534434],
    ["Extraction of Petroleum and Natural Gas", 1, 1, 346, 6437, 316, 316, 1068, 59, 
        -661, -602, None, None, 28206, None, 79, 79,
        25869, 13499, 12370, 203151, -194, 203345, 114],
    ["Mining and Processing of Nonmetal Ores", 3, None, 17345, 5018, 17306, 17015, 14919, 348, 
        138, 836, None, 350, 2027, 556, 270, 227,
        3039, 951, 2088, 8002, 3516, 4486, 201],
    ["Processing of Food from Agricultural Products", 95, 13, 4683387, 873215, 4425268, 4448189, 4169733, 5868, 
        177896, 273722, 20834, 89958, 1922238, 191177, 413169, 156044,
        522000, 245635, 276365, 2594123, 1564943, 1029180, 13578],
    ["Manufacturing of Foods", 125, 13, 4596574, 1804131, 5073726, 5173074, 3154878, 37110, 
        699174, 1037999, 142621, 301715, 1937764, 343713, 417161, 181737,
        1426532, 617772, 808760, 3189345, 1644485, 1544860, 62935],
    ["Manufacture of Wine, Beverages and Refined Tea", 30, 4, 2918745, 945000, 2827211, 2724157, 1716081, 40367, 
        163189, 369749, 39587, 166193, 1088251, 266476, 176908, 81380,
        1019764, 500218, 519546, 2075725, 1100060, 975665, 26660],
    ["Manufacturing of Tobacco", 1, None, 2015338, 1480799, 2615581, 1876796, 576229, 938340, 
        206997, 1339634, 50359, 194297, 1735612, 83994, 1229463, 63333,
        575265, 285976, 289289, 2357743, 746542, 1611201, 2995],
    ["Textile Industry", 234, 26, 2989537, 692912, 2936598, 2861612, 2633984, 9038, 
        85092, 132104, 10715, 37974, 916836, 276925, 333038, 92520,
        912463, 471948, 440515, 1525466, 697843, 827623, 50852],
    ["Manufacture of Textile Wearing Apparel, Clothing", 587, 47, 5406914, 1759790, 5354566, 5273886, 4688004, 21071, 
        155282, 269958, 27667, 93605, 1393338, 367158, 451208, 238784,
        473672, 231713, 241959, 1895951, 1089056, 806895, 151216],
    ["Manufacture of Leather, Fur, Feather and Related Products and Footwear", 319, 42, 2779879, 873546, 2721571, 2725480, 2390960, 11554, 
        79136, 147986, 14163, 57296, 1199768, 313693, 324373, 116924,
        467532, 248377, 219155, 1551606, 1015239, 536367, 102804],
    ["Processing of Timber, Manufacture of Wood, Bamboo, Rattan, Palm and Straw Products", 35, 5, 285037, 52919, 265413, 264922, 233924, 2157, 
        10129, 18250, 1809, 5964, 362453, 40152, 63147, 20812,
        59296, 30022, 29274, 452421, 193624, 258797, 5727],
    ["Manufacturing of Furniture", 95, 14, 1460680, 471748, 1415050, 1417524, 1126883, 7219, 
        98169, 155930, 13916, 50542, 587343, 84896, 127449, 35574,
        236468, 93537, 142931, 947475, 420673, 526802, 32726],
    ["Manufacturing of Paper and Paper Products", 96, 12, 1440466, 334108, 1430972, 1437823, 1329603, 4428, 
        53981, 88131, 10113, 29722, 944253, 345336, 105977, 32248,
        633036, 206601, 426435, 1575065, 1077248, 497817, 15532],
    ["Manufacture of Culture and Education, Arts and Crafts, Sports and Entertainment Supplies", 176, 29, 2595319, 989361, 2580817, 2599521, 2264675, 8594, 
        112425, 228508, 16161, 107489, 926161, 263157, 318915, 141205,
        746277, 371696, 374581, 1511282, 602653, 908629, 84753],
    ["Processing of Petroleum, Coking, Processing of Nuclear", 12, 4, 7484898, 1407238, 7451924, 7506031, 6468578, 778586, 
        77309, 1013047, 24667, 157152, 1447161, 211815, 934892, 117444,
        2195658, 1329216, 866442, 2657215, 1736284, 920931, 7320],
    ["Manufacturing of Raw Chemical Material and Chemical Products", 408, 56, 18409815, 5757201, 17582619, 17578532, 12216867, 131514, 
        1787534, 2869638, 408894, 950590, 7023229, 1920753, 1239332, 534775,
        3931496, 1961174, 1970322, 10482329, 5149928, 5332401, 91450],
    ["Manufacturing of Medical and Pharmaceutical Products", 80, 13, 2396958, 846546, 2320630, 2275736, 1303628, 19698, 
        267298, 443934, 39265, 156938, 1511768, 336264, 365737, 155500,
        1027200, 421070, 606130, 2588467, 1130809, 1457658, 33999],
    ["Manufacturing of Chemical Fiber", 5, None, 72059, 21090, 70293, 69814, 60684, 278, 
        3840, 5224, 635, 1106, 26425, 11416, 8103, 6297,
        34345, 22196, 12149, 45012, 17813, 27199, 699],
    ["Manufacture of Rubber and Plastic", 317, 51, 3741153, 851772, 3692183, 3661100, 3182924, 14985, 
        110762, 220685, 24301, 94938, 1895009, 549362, 434696, 162787,
        1778491, 944249, 834242, 3153301, 1709551, 1443750, 63779],
    ["Manufacturing of Non-metallic Mineral Products", 173, 30, 1761999, 494855, 1696053, 1696726, 1440210, 11023, 
        73436, 143620, 14993, 59161, 973242, 376471, 184455, 59015,
        871557, 446973, 424584, 1596695, 828439, 768256, 24570],
    ["Smelting and Pressing of Ferrous Metals", 47, 11, 5408306, 368646, 5364239, 4869072, 4686068, 6930, 
        20240, 111739, 1674, 84569, 2016731, 361915, 633799, 178087,
        2087251, 561752, 1525499, 3889270, 3104012, 785258, 14492],
    ["Smelting and Pressing of Non-ferrous Metals", 60, 16, 4694842, 441753, 4458582, 4163879, 4022470, 3857, 
        51372, 112563, 15182, 57334, 1001997, 239562, 339726, 168390,
        771241, 120091, 651150, 1811496, 1173450, 638046, 11194],
    ["Manufacturing of Metal Products", 255, 37, 3762104, 882032, 3667825, 3428900, 3034446, 11937, 
        95465, 160095, 22198, 52693, 1781131, 453803, 563924, 172632,
        957394, 439903, 517491, 2507044, 1461762, 1045282, 56831],
    ["Manufacturing of General Purpose Equipment", 221, 22, 6454568, 1677378, 6263856, 6144731, 4925191, 36140, 
        488966, 705563, 84270, 180457, 3925899, 1190370, 1078417, 530398,
        1817173, 844776, 972397, 5467886, 2950297, 2517589, 62214],
    ["Manufacturing of Special Purpose Equipment", 146, 19, 1838345, 489993, 1759140, 1796123, 1461849, 8479, 
        99969, 157224, 17158, 48776, 1253661, 410993, 410050, 142485,
        586298, 219959, 366339, 1827056, 1036633, 790423, 25787],
    ["Manufacture of Automobile", 244, 21, 33182791, 9452393, 32880061, 33443560, 25963866, 1256165, 
        3558996, 6189428, 523268, 1374267, 14476850, 6519479, 1498101, 670100,
        8255998, 4007112, 4248886, 20484545, 11995905, 8488640, 125983],
    ["Manufacture of Railway, Ship, Aerospace and Other Transportation Equipment", 106, 19, 5585208, 1307539, 5456454, 5219277, 4671865, 45562, 
        104864, 215622, 24971, 65196, 4581034, 754564, 887983, 136292,
        2159350, 762957, 1396393, 6864188, 5040762, 1823426, 56894],
    ["Manufacturing of Electric Machinery and Equipment", 318, 49, 9116579, 1905252, 8880798, 8579104, 7391679, 41275, 
        347738, 578439, 73543, 189426, 3766895, 1369814, 1104229, 405161,
        2211158, 845130, 1366028, 5747470, 3280903, 2466567, 105678],
    ["Manufacture of Computers, Communications and Other Electronic Equipment", 368, 59, 19501481, 3848904, 18687892, 17551506, 15555225, 126909, 
        830931, 1132599, 143562, 174759, 9154227, 4089297, 1854218, 812473,
        3839222, 1971057, 1868165, 12714663, 7025643, 5689020, 216050],
    ["Manufacture of Instrument", 49, 6, 777407, 246308, 756431, 751898, 590958, 4316, 
        70905, 90746, 10691, 15525, 429630, 168005, 135358, 33009,
        227381, 114645, 112736, 663349, 244268, 419081, 16897],
    ["Other Manufacturing", 18, 3, 168245, 33171, 150574, 146267, 125630, 603, 
        5979, 8478, 308, 1896, 60237, 8230, 15341, 5883,
        29071, 12636, 16435, 89323, 49286, 40037, 3245],
    ["Comprehensive Utilization of Waste Resources", 8, 2, 523228, -37820, 518100, 521548, 510829, 697, 
        -48225, -43535, 3549, 3993, 197486, 22862, 10798, 4360,
        39388, 21303, 18085, 253852, 210197, 43655, 1121],
    ["Metal Products, Machinery and Equipment Repair", 14, 3, 242952, 61460, 246916, 234607, 222431, 403, 
        -13308, -10752, 261, 2153, 233872, 40499, 31192, 8425,
        262268, 48377, 213891, 483834, 363397, 120437, 5681],
    ["Production and Supply of Electric Power and Heat Power", 21, None, 11827284, 3056156, 11807099, 11008205, 10207675, 49933, 
        1151133, 1463855, 96541, 262789, 3533709, 419200, 146026, 10529,
        18820803, 8033746, 10787057, 27031362, 11424972, 15606390, 23734],
    ["Production and Supply of Gas", 13, 2, 2101628, 568350, 2105060, 1955762, 1810548, 4830, 
        74015, 90546, 16021, 11701, 441210, 74424, 51774, 29106,
        914176, 195536, 718640, 1871731, 1236818, 634913, 4022],
    ["Production and Supply of Water", 26, 6, 489597, 246959, 488288, 462639, 320924, 7109, 
        16086, 46001, 1198, 22806, 601465, 45371, 7637, 4887,
        2236742, 804820, 1431922, 2362657, 1553419, 809238, 7513]
]


df = pd.DataFrame(data, columns=columns)

# Вычисляем необходимые показатели
df["profit_per_worker"] = df["Total Profits"] / df["Employed Persons"]
df["avg_workers_per_enterprise"] = df["Employed Persons"] / df["Enterprises"] 
# df["profitability_ratio"] = df["Total Profits"] / (df["Business Revenue"])  # Можно заменить на Value Added, если есть

total_workers = 1534434
df["workers_share"] = df["Employed Persons"] / total_workers * 100

total_output = 171987181  # общий выпуск в млрд юаней
df["output_share"] = df["Output Value"] / total_output * 100  # в процентах
df = df[df["output_share"] > 1.0]

total_profit = 11053751
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

# Построение пузырьковой диаграммы
fig = px.scatter(
    df_clean,
    x="avg_workers_per_enterprise",
    y="profit_per_worker",
    size="profit_share",
    text="Sector",
    size_max=60,
    hover_name="Sector",
    color="Sector",
    labels={
        "avg_workers_per_enterprise": "Среднее число работников на предприятие",
        "profit_per_worker": "Прибыль на одного работника",
        "profit_share": "Прибыль в отрасли"
    },
    hover_data={
        "Sector": False,  # не дублировать в теле
        "avg_workers_per_enterprise": True,
        "profit_per_worker": True,
        "profit_share": True,
    },
    title="Уязвимость и прибыльность отраслей"
)

fig.update_traces(text=None) 
fig.update_layout(height=700)
fig.show()

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
    "workers_share" ,
    "worker_impact_index"
]

# Расчёт z-score для каждой метрики
for col in metrics:
    z_col = f"{col}_zscore"
    df[z_col] = (df[col] - df[col].mean()) / df[col].std()
    
# Убираем строки с нулями или NaN
df_clean = df.dropna(subset=[
    "margin_on_sales", "margin_on_cost", "return_on_assets", "profit_per_worker", "return_on_working_capital", "worker_impact_index"
])
df_clean = df_clean[(df_clean["Total Profits"] > 0) & (df_clean["Business Revenue"] > 0)]

# Топ-10 по рентабельности продаж
top_profitable = df_clean.sort_values(by="margin_on_sales", ascending=False)


df_clean = df.dropna(subset=[
    "margin_on_sales", "margin_on_cost", "return_on_assets", "profit_per_worker", "return_on_working_capital", "worker_impact_index"
])
df_clean = df_clean[(df_clean["Total Profits"] > 0) & (df_clean["Business Revenue"] > 0)]

# Топ-10 по рентабельности продаж
top_profitable = df_clean.sort_values(by="margin_on_sales", ascending=False)

import json

result_array = df_clean.to_dict(orient="records")
print(json.dumps(result_array, ensure_ascii=False, indent=2))    

result_array = df_clean.to_dict(orient="records")

# Сохраняем в файл JSON
with open("df_clean_results-2.json", "w", encoding="utf-8") as f:
    json.dump(result_array, f, ensure_ascii=False, indent=2)

print("Результаты сохранены в df_clean_results.json")

app = dash.Dash(__name__)

all_columns = df_clean.columns.tolist()
# Запуск Dash
app.layout = html.Div([
    html.H4("Выберите, какие столбцы скрыть:"),
    dcc.Dropdown(
        id='column-selector',
        options=[{"label": col, "value": col} for col in all_columns],
        value=[],  # по умолчанию ничего не скрыто
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