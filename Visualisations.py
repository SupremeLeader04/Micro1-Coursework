import pandas as pd

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

print(wages.head())