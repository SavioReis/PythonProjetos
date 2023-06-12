import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r"C:\Users\Sávio Reis\Desktop\Probabilidade - Estatistica Descritiva\empresa.xls")

num_cols = df.select_dtypes(include=["float64", "int64"]).columns
resumo = df[num_cols].describe()

print(resumo)

for col in num_cols:
    plt.figure()
    plt.title(f"BoxPlot - {col}")
    plt.boxplot(df[col])
    plt.show()

for col in num_cols:
    plt.figure()
    plt.title(f"Histograma - {col}")
    plt.hist(df[col], bins=10)
    plt.show()

cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    plt.figure()
    plt.title(f"Gráfico de Barra - {col}")
