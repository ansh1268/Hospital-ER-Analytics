import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
num_records = 5000
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

# Helper function to generate random dates
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

# Data Generation
data = []
races = ['White', 'African American', 'Hispanic', 'Asian', 'Other']
genders = ['Male', 'Female', 'Non-binary']
departments = ['General Practice', 'Orthopaedics', 'Cardiology', 'Neurology', 'Pediatrics', 'ENT']
satisfaction_scores = [1, 2, 3, 4, 5]

for i in range(num_records):
    admission_dt = random_date(start_date, end_date)
    patient_id = f"PAT-{100000 + i}"
    
    # Introduce some duplicates
    if i > 0 and i % 500 == 0:
        data.append(data[-1])
        continue

    # Age distribution
    age = int(np.random.normal(45, 20))
    age = max(0, min(100, age))
    
    # Wait time distribution (in minutes)
    wait_time = int(np.random.exponential(45))
    wait_time = max(5, wait_time)
    
    # Admission Flag (1 if wait time is high or random severity)
    admission_flag = 1 if wait_time > 120 or random.random() > 0.7 else 0
    
    # Satisfaction score (lower if wait time is high)
    if wait_time > 90:
        sat_score = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
    else:
        sat_score = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 20, 30, 35])[0]

    record = {
        'Patient ID': patient_id,
        'Patient Admission Date': admission_dt.date(),
        'Patient Admission Time': admission_dt.time().strftime('%H:%M:%S'),
        'Patient Gender': random.choice(genders),
        'Patient Age': age,
        'Patient Race': random.choice(races),
        'Department Referral': random.choice(departments),
        'Patient Satisfaction Score': sat_score,
        'Patient Wait Time': wait_time,
        'Admission Flag': admission_flag
    }
    data.append(record)

df = pd.DataFrame(data)

# Introduce some missing values
df.loc[df.sample(frac=0.02).index, 'Patient Satisfaction Score'] = np.nan
df.loc[df.sample(frac=0.01).index, 'Department Referral'] = np.nan

# Save to CSV
df.to_csv('hospital_er_data_raw.csv', index=False)
print(f"Generated {len(df)} records in hospital_er_data_raw.csv")
