import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
from adjustText import adjust_text

# Preparing Data
hours = pd.read_excel("./OECD_AnnualHours.xlsx")
hours = hours.drop(columns=["Unnamed: 1", "Unnamed: 16"])
hours = hours.fillna(0)
hours.columns = hours.columns.astype(str)
hours = hours.melt(id_vars=["Country"], var_name="Year", value_name="Working Hours")
hours = hours[hours["Year"] == "2022"]
hours = hours.iloc[:-3]

strictness = pd.read_excel("./OECD_EmploymentStrictness.xlsx")
strictness = strictness.fillna(0)
strictness.columns = strictness.columns.astype(str)
strictness = strictness.melt(id_vars=["Country"], var_name="Year", value_name="Labour_Market_Strictness")

wages = pd.read_excel("./OECD_WagesPPPDollar2023.xlsx")
wages = wages.drop(columns=["Unnamed: 25"])
wages = wages.fillna(0)
wages.columns = wages.columns.astype(str)
wages = wages.melt(id_vars=["Country"], var_name="Year", value_name="Average_Annual_Wage")

law_metrics = pd.read_excel("./cbr-lri-117-countries-data-2023-update.xlsx", sheet_name=None)
del law_metrics["Title page"]
present = ["UK", "USA", "turkey"] + [country.lower() for country in hours["Country"]][:-3]
present = list(map(lambda x: 'slovakia' if x == 'slovak republic' else x, present))
not_present = [country for country in law_metrics.keys() if country not in present]
for country in not_present:
    del law_metrics[country]
print(len(law_metrics.keys()) == len(hours["Country"]))

df_dict = {}
overtime_premia, max_daily_working_time, right_to_collective_bargaining, right_to_industrial_action = 11, 15, 26, 36
for key, value in law_metrics.items():
    value = value[["Unnamed: 2", overtime_premia, max_daily_working_time, right_to_collective_bargaining, right_to_industrial_action]]
    value = value[value["Unnamed: 2"] == 2022]
    value = value.drop(columns=["Unnamed: 2"])
    value.columns = ["Overtime Premia", "Maximum Daily Working Time", "Right to Collective Bargaining", "Right to Industrial Action"]
    df_dict[key] = value

df_from_dict = pd.concat(df_dict, names=["Country"])
df_from_dict.reset_index(level=0, inplace=True)
df_from_dict["Country"] = df_from_dict["Country"].apply(lambda x: x.title())
df_from_dict["Country"] = df_from_dict["Country"].replace({
    "Uk": "UK",
    "Usa": "USA"
})
hours["Country"] = hours["Country"].replace({
    "Slovak Republic": "Slovakia",
    "Türkiye": "Turkey",
    "United Kingdom": "UK",
    "United States": "USA"
})
hours["Working Hours"] = hours["Working Hours"].replace(0.0, 1732.0)

final_df = hours.merge(df_from_dict, on="Country", how="inner")



# Visualisation 1

sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Maximum Daily Working Time Against Average Annual Hours Worked (2022)")
plt.scatter(final_df['Maximum Daily Working Time'], final_df['Working Hours'], color='blue')
plt.ylabel('Average Annual Working Hours')
plt.xlabel('Maximum Daily Working Time')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(final_df['Maximum Daily Working Time'], final_df['Working Hours'])

x_values = np.linspace(final_df['Maximum Daily Working Time'].min(), final_df['Maximum Daily Working Time'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

for idx, row in final_df.iterrows():
    plt.annotate(row['Country'], (row['Maximum Daily Working Time'], row['Working Hours']), fontsize=10)

plt.legend()
plt.show()



# Visualisation 2

sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Overtime Premia Against Average Annual Hours Worked (2022)")
plt.scatter(final_df['Overtime Premia'], final_df['Working Hours'], color='blue')
plt.ylabel('Average Annual Working Hours')
plt.xlabel('Overtime Premia')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(final_df['Overtime Premia'], final_df['Working Hours'])

x_values = np.linspace(final_df['Overtime Premia'].min(), final_df['Overtime Premia'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

for idx, row in final_df.iterrows():
    plt.annotate(row['Country'], (row['Overtime Premia'], row['Working Hours']), fontsize=10)

plt.legend()
plt.show()



# Visualisation 3

sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Right to Collective Bargaining Against Average Annual Hours Worked (2022)")
plt.scatter(final_df['Right to Collective Bargaining'], final_df['Working Hours'], color='blue')
plt.ylabel('Average Annual Working Hours')
plt.xlabel('Right to Collective Bargaining')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(final_df['Right to Collective Bargaining'], final_df['Working Hours'])

x_values = np.linspace(final_df['Right to Collective Bargaining'].min(), final_df['Right to Collective Bargaining'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

for idx, row in final_df.iterrows():
    plt.annotate(row['Country'], (row['Right to Collective Bargaining'], row['Working Hours']), fontsize=10)

plt.legend()
plt.show()



# Visualisation 4

sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Right to Industrial Action Against Average Annual Hours Worked (2022)")
plt.scatter(final_df['Overtime Premia'], final_df['Working Hours'], color='blue')
plt.ylabel('Average Annual Working Hours')
plt.xlabel('Right to Industrial Action')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(final_df['Right to Industrial Action'], final_df['Working Hours'])

x_values = np.linspace(final_df['Right to Industrial Action'].min(), final_df['Right to Industrial Action'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

for idx, row in final_df.iterrows():
    plt.annotate(row['Country'], (row['Right to Industrial Action'], row['Working Hours']), fontsize=10)

plt.legend()
plt.show()