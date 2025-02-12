import pandas as pd

hours = pd.read_excel("./OECD_AnnualHours.xlsx")
hours = hours.drop(columns=["Unnamed: 1", "Unnamed: 16"])
hours = hours.fillna(0)
hours.columns = hours.columns.astype(str)
hours = pd.wide_to_long(hours, stubnames="20", j="Year", i="Country")
hours = hours.rename({hours.columns[-1]: "Hours_Worked"})


strictness = pd.read_excel("./OECD_EmploymentStrictness.xlsx")
strictness = strictness.fillna(0)
strictness.columns = strictness.columns.astype(str)
strictness = pd.wide_to_long(strictness, stubnames="20", j="Year", i="Country")

wages = pd.read_excel("./OECD_WagesPPPDollar2023.xlsx")
wages = wages.drop(columns=["Unnamed: 25"])

print(hours.head())