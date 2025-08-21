import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('salaries.csv')  

print("Kształt danych:", df.shape)
print("\\nPierwsze 5 wierszy:")
print(df.head())
print("\\nInformacje o kolumnach:")
print(df.info())
print("\\nBraki danych:")
print(df.isnull().sum())

print("Statystyki płac w USD:")
print(df['salary_in_usd'].describe())

print(f"\\nLata: {sorted(df['work_year'].unique())}")
print(f"Poziomy doświadczenia: {df['experience_level'].unique()}")
print(f"Remote ratio: {sorted(df['remote_ratio'].unique())}")

yearly_salary = df.groupby('work_year')['salary_in_usd'].mean()
print("Średnia płaca per rok:")
print(yearly_salary)

plt.figure(figsize=(10, 6))
plt.plot(yearly_salary.index, yearly_salary.values, marker='o', linewidth=2, markersize=8)
plt.title('Trend średniej płacy 2020-2025', fontsize=14, fontweight='bold')
plt.xlabel('Rok')
plt.ylabel('Średnia płaca (USD)')
plt.grid(True, alpha=0.3)
plt.xticks(yearly_salary.index)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.tight_layout()
plt.show()




job_stats = df.groupby('job_title')['salary_in_usd'].agg([
    'count', 'mean', 'median', 'std', 'min', 'max'
]).round(0)

# Tylko stanowiska z min. 5 pracownikami (żeby była reprezentatywność)
job_stats_filtered = job_stats[job_stats['count'] >= 5].sort_values('mean', ascending=False)

print("Top 15 najlepiej płatnych stanowisk:")
print(job_stats_filtered.head(15))


plt.figure(figsize=(12, 8))
top_jobs = job_stats_filtered.head(15)

y_pos = range(len(top_jobs))
plt.barh(y_pos, top_jobs['mean'], 
         xerr=top_jobs['std'], capsize=3, alpha=0.7, color='skyblue')

plt.yticks(y_pos, top_jobs.index, fontsize=10)
plt.xlabel('Średnia płaca (USD)')
plt.title('Top 15 stanowisk - średnia płaca ze standardowym odchyleniem', fontweight='bold')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
plt.gca().invert_yaxis()  
plt.tight_layout()
plt.show()




company_size_stats = df.groupby('company_size')['salary_in_usd'].agg([
    'count', 'mean', 'median', 'std'
]).round(0)

print("Płace według rozmiaru firmy:")
print(company_size_stats)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='company_size', y='salary_in_usd')
plt.title('Rozkład płac według rozmiaru firmy', fontweight='bold')
plt.xlabel('Rozmiar firmy (S=Mała, M=Średnia, L=Duża)')
plt.ylabel('Płaca (USD)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

