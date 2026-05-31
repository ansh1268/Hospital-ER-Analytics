import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv('hospital_er_data_raw.csv')

# 1. Remove Duplicates
initial_count = len(df)
df.drop_duplicates(inplace=True)
duplicates_removed = initial_count - len(df)

# 2. Handle Missing Values
# Fill missing satisfaction scores with median
df['Patient Satisfaction Score'] = df['Patient Satisfaction Score'].fillna(df['Patient Satisfaction Score'].median())
# Fill missing department referrals with 'Unknown'
df['Department Referral'] = df['Department Referral'].fillna('Unknown')

# 3. Standardize Date and Time
df['Patient Admission Date'] = pd.to_datetime(df['Patient Admission Date'])
df['Admission Hour'] = pd.to_datetime(df['Patient Admission Time'], format='%H:%M:%S').dt.hour

# 4. Feature Engineering
# Age Groups
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100]
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
df['Age Group'] = pd.cut(df['Patient Age'], bins=bins, labels=labels, right=False)

# Wait Time Status (Threshold: 60 mins)
df['Wait Time Status'] = np.where(df['Patient Wait Time'] > 60, 'Delay', 'On Time')

# Date features
df['Month'] = df['Patient Admission Date'].dt.month_name()
df['Quarter'] = 'Q' + df['Patient Admission Date'].dt.quarter.astype(str)
df['Year'] = df['Patient Admission Date'].dt.year
df['Weekday'] = df['Patient Admission Date'].dt.day_name()

# Peak Hour Flag (e.g., 08:00-11:00 and 17:00-20:00)
df['Peak Hour Flag'] = df['Admission Hour'].apply(lambda x: 1 if (8 <= x <= 11) or (17 <= x <= 20) else 0)

# 5. Create Calendar Table (Star Schema requirement)
min_date = df['Patient Admission Date'].min()
max_date = df['Patient Admission Date'].max()
calendar_df = pd.DataFrame({'Date': pd.date_range(min_date, max_date)})
calendar_df['Year'] = calendar_df['Date'].dt.year
calendar_df['Quarter'] = 'Q' + calendar_df['Date'].dt.quarter.astype(str)
calendar_df['Month'] = calendar_df['Date'].dt.month_name()
calendar_df['Month_Num'] = calendar_df['Date'].dt.month
calendar_df['Day'] = calendar_df['Date'].dt.day
calendar_df['Weekday'] = calendar_df['Date'].dt.day_name()
calendar_df['Weekday_Num'] = calendar_df['Date'].dt.weekday

# Save cleaned data and calendar table
df.to_csv('hospital_er_data_cleaned.csv', index=False)
calendar_df.to_csv('calendar_table.csv', index=False)

# Data Quality Report
report = f"""
Data Quality Report
-------------------
Initial Records: {initial_count}
Duplicates Removed: {duplicates_removed}
Missing Values Handled:
  - Satisfaction Score: {df['Patient Satisfaction Score'].isna().sum()} (Imputed with median)
  - Department Referral: {df['Department Referral'].isna().sum()} (Filled with 'Unknown')
Final Record Count: {len(df)}
"""
with open('data_quality_report.txt', 'w') as f:
    f.write(report)

print("Cleaning and feature engineering complete.")
