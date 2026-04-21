import plotly.express as px
import pandas as pd



task_open = [
		{
			"year": 2024,
			"month": 1,
			"total_tickets": 66
		},
		{
			"year": 2024,
			"month": 2,
			"total_tickets": 87
		},
		{
			"year": 2024,
			"month": 3,
			"total_tickets": 84
		},
		{
			"year": 2024,
			"month": 4,
			"total_tickets": 70
		},
		{
			"year": 2024,
			"month": 5,
			"total_tickets": 68
		},
		{
			"year": 2024,
			"month": 6,
			"total_tickets": 67
		},
		{
			"year": 2024,
			"month": 7,
			"total_tickets": 86
		},
		{
			"year": 2024,
			"month": 8,
			"total_tickets": 119
		},
		{
			"year": 2024,
			"month": 9,
			"total_tickets": 247
		},
		{
			"year": 2024,
			"month": 10,
			"total_tickets": 96
		},
		{
			"year": 2024,
			"month": 11,
			"total_tickets": 83
		},
		{
			"year": 2024,
			"month": 12,
			"total_tickets": 174
		},
		{
			"year": 2025,
			"month": 1,
			"total_tickets": 73
		},
		{
			"year": 2025,
			"month": 2,
			"total_tickets": 88
		}
	]

# SELECT 
#     YEAR(`date`) AS year,
#     MONTH(`date`) AS month,
#     COUNT(*) AS total_tickets
# FROM `tickets_status_history`
# WHERE `date` >= '2024-01-01' AND (`status_id` != '1' AND `status_id` != '2') AND user_id != 1
# GROUP BY YEAR(`date`), MONTH(`date`)
# ORDER BY year, month;


task_closed = [
		{
			"year": 2024,
			"month": 1,
			"total_tickets": 56
		},
		{
			"year": 2024,
			"month": 2,
			"total_tickets": 111
		},
		{
			"year": 2024,
			"month": 3,
			"total_tickets": 171
		},
		{
			"year": 2024,
			"month": 4,
			"total_tickets": 77
		},
		{
			"year": 2024,
			"month": 5,
			"total_tickets": 76
		},
		{
			"year": 2024,
			"month": 6,
			"total_tickets": 76
		},
		{
			"year": 2024,
			"month": 7,
			"total_tickets": 91
		},
		{
			"year": 2024,
			"month": 8,
			"total_tickets": 116
		},
		{
			"year": 2024,
			"month": 9,
			"total_tickets": 254
		},
		{
			"year": 2024,
			"month": 10,
			"total_tickets": 86
		},
		{
			"year": 2024,
			"month": 11,
			"total_tickets": 98
		},
		{
			"year": 2024,
			"month": 12,
			"total_tickets": 183
		},
		{
			"year": 2025,
			"month": 1,
			"total_tickets": 68
		},
		{
			"year": 2025,
			"month": 2,
			"total_tickets": 86
		}
	]

df_open = pd.DataFrame(task_open)
df_closed = pd.DataFrame(task_closed)

df_open["date"] = pd.to_datetime(df_open[["year", "month"]].assign(day=1))
df_closed["date"] = pd.to_datetime(df_closed[["year", "month"]].assign(day=1))

df_open["status"] = "Открытые"
df_closed["status"] = "Закрытые"

df_combined = pd.concat([df_open, df_closed])

fig = px.line(df_combined, x="date", y="total_tickets", color="status", title="Открытые и закрытые задачи", markers=True)
fig.show()
