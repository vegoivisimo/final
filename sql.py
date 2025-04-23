import sqlite3

import pandas as pd
import prettytable


prettytable.DEFAULT = 'DEFAULT'


con = sqlite3.connect("my_data1.db")
cur = con.cursor()


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)


df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")


cur.execute("DROP TABLE IF EXISTS SPACEXTABLE")
cur.execute("CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL")
con.commit()


print("\n=== Task 1: Unique Launch Sites ===")
cur.execute('SELECT DISTINCT "Launch_Site" FROM SPACEXTABLE')
results = cur.fetchall()
table = prettytable.PrettyTable(['Launch_Site'])
for row in results:
    table.add_row(row)
print(table)


print("\n=== Task 2: 5 Records with Launch Sites Starting with 'CCA' ===")
cur.execute('SELECT * FROM SPACEXTABLE WHERE "Launch_Site" LIKE "CCA%" LIMIT 5')
results = cur.fetchall()
table = prettytable.PrettyTable(['Date', 'Time (UTC)', 'Booster_Version', 'Launch_Site', 'Payload', 'PAYLOAD_MASS__KG_', 'Orbit', 'Customer', 'Mission_Outcome', 'Landing_Outcome'])
for row in results:
    table.add_row(row)
print(table)


print("\n=== Task 3: Total Payload Mass by NASA (CRS) ===")
cur.execute('SELECT SUM("PAYLOAD_MASS__KG_") AS Total_Payload_Mass FROM SPACEXTABLE WHERE "Customer" = "NASA (CRS)"')
result = cur.fetchone()
table = prettytable.PrettyTable(['Total_Payload_Mass'])
table.add_row([result[0]])
print(table)

print("\n=== Task 4: Average Payload Mass for F9 v1.1 ===")
cur.execute('SELECT AVG("PAYLOAD_MASS__KG_") AS Average_Payload_Mass FROM SPACEXTABLE WHERE "Booster_Version" = "F9 v1.1"')
result = cur.fetchone()
table = prettytable.PrettyTable(['Average_Payload_Mass'])
table.add_row([result[0]])
print(table)


print("\n=== Task 5: First Successful Ground Pad Landing Date ===")
cur.execute('SELECT MIN("Date") AS First_Successful_Ground_Pad_Landing FROM SPACEXTABLE WHERE "Landing_Outcome" = "Success (ground pad)"')
result = cur.fetchone()
table = prettytable.PrettyTable(['First_Successful_Ground_Pad_Landing'])
table.add_row([result[0]])
print(table)

print("\n=== Task 6: Boosters with Drone Ship Success and Payload Mass 4000-6000 kg ===")
cur.execute('SELECT "Booster_Version" FROM SPACEXTABLE WHERE "Landing_Outcome" = "Success (drone ship)" AND "PAYLOAD_MASS__KG_" > 4000 AND "PAYLOAD_MASS__KG_" < 6000')
results = cur.fetchall()
table = prettytable.PrettyTable(['Booster_Version'])
for row in results:
    table.add_row(row)
print(table)


print("\n=== Task 7: Total Successful and Failure Mission Outcomes ===")
cur.execute('SELECT "Mission_Outcome", COUNT(*) AS Count FROM SPACEXTABLE GROUP BY "Mission_Outcome"')
results = cur.fetchall()
table = prettytable.PrettyTable(['Mission_Outcome', 'Count'])
for row in results:
    table.add_row(row)
print(table)


print("\n=== Task 8: Booster Versions with Maximum Payload Mass ===")
cur.execute('SELECT "Booster_Version" FROM SPACEXTABLE WHERE "PAYLOAD_MASS__KG_" = (SELECT MAX("PAYLOAD_MASS__KG_") FROM SPACEXTABLE)')
results = cur.fetchall()
table = prettytable.PrettyTable(['Booster_Version'])
for row in results:
    table.add_row(row)
print(table)


print("\n=== Task 9: Failure Drone Ship Landings in 2015 ===")
cur.execute('SELECT substr("Date", 6, 2) AS Month, "Landing_Outcome", "Booster_Version", "Launch_Site" FROM SPACEXTABLE WHERE "Landing_Outcome" = "Failure (drone ship)" AND substr("Date", 0, 5) = "2015"')
results = cur.fetchall()
table = prettytable.PrettyTable(['Month', 'Landing_Outcome', 'Booster_Version', 'Launch_Site'])
for row in results:
    table.add_row(row)
print(table)

print("\n=== Task 10: Count of Landing Outcomes (2010-06-04 to 2017-03-20) ===")
cur.execute('SELECT "Landing_Outcome", COUNT(*) AS Count FROM SPACEXTABLE WHERE "Date" BETWEEN "2010-06-04" AND "2017-03-20" GROUP BY "Landing_Outcome" ORDER BY Count DESC')
results = cur.fetchall()
table = prettytable.PrettyTable(['Landing_Outcome', 'Count'])
for row in results:
    table.add_row(row)
print(table)

con.close()