import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_and_save(fig_func, filename, *args, **kwargs):
    try:
        plt.figure()  
        fig_func(*args, **kwargs)
        plt.savefig(filename, dpi=300, bbox_inches='tight')  # Guardar como PNG
        plt.show() 
        plt.close() 
        print(f"Figura guardada como: {filename}")
    except Exception as e:
        print(f"Error al generar figura {filename}: {e}")


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
df = pd.read_csv(url)
print("Dataset cargado correctamente")
print(df.head(5))


print("\nGráfico Inicial: FlightNumber vs PayloadMass")
plot_and_save(
    sns.catplot, "flightnumber_vs_payloadmass.png",
    y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=5
)
plt.xlabel("Número de Vuelo", fontsize=20)
plt.ylabel("Masa de Carga (kg)", fontsize=20)
plt.title("Número de Vuelo vs Masa de Carga por Clase", fontsize=20)


print("\nTarea 1: FlightNumber vs LaunchSite")
plot_and_save(
    sns.catplot, "flightnumber_vs_launchsite.png",
    x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=5
)
plt.xlabel("Número de Vuelo", fontsize=20)
plt.ylabel("Sitio de Lanzamiento", fontsize=20)
plt.title("Número de Vuelo vs Sitio de Lanzamiento por Clase", fontsize=20)


print("\nTarea 2: PayloadMass vs LaunchSite")
plot_and_save(
    sns.catplot, "payloadmass_vs_launchsite.png",
    x="PayloadMass", y="LaunchSite", hue="Class", data=df, aspect=5
)
plt.xlabel("Masa de Carga (kg)", fontsize=20)
plt.ylabel("Sitio de Lanzamiento", fontsize=20)
plt.title("Masa de Carga vs Sitio de Lanzamiento por Clase", fontsize=20)


print("\nTarea 3: Success Rate by Orbit Type")
orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
plot_and_save(
    sns.barplot, "success_rate_by_orbit.png",
    x="Class", y="Orbit", data=orbit_success
)
plt.xlabel("Tasa de Éxito", fontsize=20)
plt.ylabel("Tipo de Órbita", fontsize=20)
plt.title("Tasa de Éxito por Tipo de Órbita", fontsize=20)


print("\nTarea 4: FlightNumber vs Orbit Type")
plot_and_save(
    sns.catplot, "flightnumber_vs_orbit.png",
    x="FlightNumber", y="Orbit", hue="Class", data=df, aspect=5
)
plt.xlabel("Número de Vuelo", fontsize=20)
plt.ylabel("Tipo de Órbita", fontsize=20)
plt.title("Número de Vuelo vs Tipo de Órbita por Clase", fontsize=20)


print("\nTarea 5: PayloadMass vs Orbit Type")
plot_and_save(
    sns.catplot, "payloadmass_vs_orbit.png",
    x="PayloadMass", y="Orbit", hue="Class", data=df, aspect=5
)
plt.xlabel("Masa de Carga (kg)", fontsize=20)
plt.ylabel("Tipo de Órbita", fontsize=20)
plt.title("Masa de Carga vs Tipo de Órbita por Clase", fontsize=20)


print("\nTarea 6: Yearly Success Rate Trend")
df['Year'] = df['Date'].apply(lambda x: x.split('-')[0])  # Extraer año
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
plot_and_save(
    sns.lineplot, "yearly_success_trend.png",
    x="Year", y="Class", data=yearly_success, marker='o'
)
plt.xlabel("Año", fontsize=20)
plt.ylabel("Tasa de Éxito", fontsize=20)
plt.title("Tasa de Éxito de Lanzamiento por Año", fontsize=20)