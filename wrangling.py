import pandas as pd
import numpy as np


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv"
df = pd.read_csv(url)


print("Verifying BoosterVersion (should only be Falcon 9):")
print(df['BoosterVersion'].value_counts())


print("\n=== TASK 1: Number of launches per site ===")
launch_site_counts = df['LaunchSite'].value_counts()
print(launch_site_counts)


print("\n=== TASK 2: Number of launches per orbit ===")
orbit_counts = df['Orbit'].value_counts()
print(orbit_counts)


print("\n=== TASK 3: Number of mission outcomes ===")
landing_outcomes = df['Outcome'].value_counts()
print(landing_outcomes)


print("\nMission outcomes with indices:")
for i, outcome in enumerate(landing_outcomes.keys()):
    print(i, outcome)


bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
print("\nBad outcomes (unsuccessful landings):")
print(bad_outcomes)

print("\n=== TASK 4: Creating landing_class column ===")
landing_class = [1 if outcome not in bad_outcomes else 0 for outcome in df['Outcome']]
df['Class'] = landing_class


print("\nFirst 8 rows of Class column:")
print(df[['Class']].head(8))


print("\nFirst 5 rows of the updated DataFrame:")
print(df.head(5))


success_rate = df['Class'].mean()
print("\nSuccess rate of Falcon 9 first stage landings:")
print(f"{success_rate:.2%}")

df.to_csv('dataset_part_2.csv', index=False)
print("\nData exported to 'dataset_part_2.csv'")