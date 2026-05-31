import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("hospital_er_data_cleaned.csv")

# Convert date column to datetime objects
df["Patient Admission Date"] = pd.to_datetime(df["Patient Admission Date"])

# Set style for plots
sns.set_style("whitegrid")

# 1. Patient Trend Analysis (Monthly)
plt.figure(figsize=(12, 6))
df["Month_Year"] = df["Patient Admission Date"].dt.to_period("M")
monthly_patients = df.groupby("Month_Year").size().reset_index(name="Total Patients")
monthly_patients["Month_Year"] = monthly_patients["Month_Year"].astype(str)
sns.lineplot(x="Month_Year", y="Total Patients", data=monthly_patients)
plt.title("Monthly Patient Trend")
plt.xlabel("Month")
plt.ylabel("Total Patients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_patient_trend.png")
plt.close()

# 2. Gender Distribution
plt.figure(figsize=(8, 8))
df["Patient Gender"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Gender Distribution of Patients")
plt.ylabel("")
plt.tight_layout()
plt.savefig("gender_distribution.png")
plt.close()

# 3. Age Group Analysis
plt.figure(figsize=(10, 6))
sns.countplot(x="Age Group", data=df, palette="viridis", order=sorted(df["Age Group"].dropna().unique()))
plt.title("Patient Distribution by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Patients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("age_group_distribution.png")
plt.close()

# 4. Department Referral Analysis
plt.figure(figsize=(12, 6))
sns.countplot(y="Department Referral", data=df, palette="magma", order=df["Department Referral"].value_counts().index)
plt.title("Patient Distribution by Department Referral")
plt.xlabel("Number of Patients")
plt.ylabel("Department Referral")
plt.tight_layout()
plt.savefig("department_referral_distribution.png")
plt.close()

# 5. Wait Time Analysis (Distribution)
plt.figure(figsize=(10, 6))
sns.histplot(df["Patient Wait Time"], bins=30, kde=True)
plt.title("Distribution of Patient Wait Times")
plt.xlabel("Wait Time (minutes)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("wait_time_distribution.png")
plt.close()

# 6. Satisfaction Analysis (Distribution)
plt.figure(figsize=(8, 6))
sns.countplot(x="Patient Satisfaction Score", data=df, palette="cividis")
plt.title("Distribution of Patient Satisfaction Scores")
plt.xlabel("Satisfaction Score (1-5)")
plt.ylabel("Number of Patients")
plt.tight_layout()
plt.savefig("satisfaction_score_distribution.png")
plt.close()

print("Visualizations generated and saved as PNG files.")
