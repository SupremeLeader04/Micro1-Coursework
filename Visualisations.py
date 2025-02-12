import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns

# Preparing Data
hours = pd.read_excel("./OECD_AnnualHours.xlsx")
hours = hours.drop(columns=["Unnamed: 1", "Unnamed: 16"])
hours = hours.fillna(0)
hours.columns = hours.columns.astype(str)
hours = hours.melt(id_vars=["Country"], var_name="Year", value_name="Working_Hours")

strictness = pd.read_excel("./OECD_EmploymentStrictness.xlsx")
strictness = strictness.fillna(0)
strictness.columns = strictness.columns.astype(str)
strictness = strictness.melt(id_vars=["Country"], var_name="Year", value_name="Labour_Market_Strictness")

wages = pd.read_excel("./OECD_WagesPPPDollar2023.xlsx")
wages = wages.drop(columns=["Unnamed: 25"])
wages = wages.fillna(0)
wages.columns = wages.columns.astype(str)
wages = wages.melt(id_vars=["Country"], var_name="Year", value_name="Average_Annual_Wage")

merged_h_s = pd.merge(hours[['Country', 'Year', 'Working_Hours']], strictness[['Country', 'Year', 'Labour_Market_Strictness']], on=['Country', 'Year'], how='inner')
df = pd.merge(merged_h_s, wages[['Country', 'Year', 'Average_Annual_Wage']], on=['Country', 'Year'], how='inner')
df = df.drop_duplicates(subset=["Country", "Year"])
df["Year"] = pd.to_numeric(df["Year"])

# use only latest year
df = df[df["Year"] == 2019]
df = df.reset_index()
df = df.drop("index", axis=1)

# Visualisation 1
sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Labour Market Strictness Against Average Annual Hours Worked (2019)")
plt.scatter(df['Labour_Market_Strictness'], df['Working_Hours'], color='blue')
plt.ylabel('Average Annual Working Hours')
plt.xlabel('Labour Market Strictness Indicator')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Labour_Market_Strictness'], df['Working_Hours'])

x_values = np.linspace(df['Labour_Market_Strictness'].min(), df['Labour_Market_Strictness'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

plt.legend()
plt.show()

# Visualisation 2
sns.set_theme(style="darkgrid")
plt.figure(figsize=(6, 4))
plt.suptitle("OECD Countries: Labour Market Strictness Against Average Annual Wage (2019)")
plt.scatter(df['Labour_Market_Strictness'], df['Average_Annual_Wage'], color='blue')
plt.ylabel('Average Annual Wage in 2023 PPP US Dollars (2019)')
plt.xlabel('Labour Market Strictness Indicator')

# Adding LR Line
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Labour_Market_Strictness'], df['Average_Annual_Wage'])

x_values = np.linspace(df['Labour_Market_Strictness'].min(), df['Labour_Market_Strictness'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', label=f'Linear Regression (r = {r_value:.4f})\nP-value (p = {p_value:.4f})')

plt.legend()
plt.show()