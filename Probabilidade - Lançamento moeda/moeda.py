import random
import matplotlib.pyplot as plt

def jogar_moeda(n):
    caras = 0
    coroas = 0
    for i in range(n):
        if random.random() < 0.5:
            caras += 1
        else:
            coroas += 1
    return caras/n, coroas/n

valores_n = [10, 100, 1000, 10000, 100000]
resultados = []
for n in valores_n:
    resultados.append(jogar_moeda(n))

prop_caras = [r[0] for r in resultados]
prop_coroas = [r[1] for r in resultados]

plt.plot(valores_n, prop_caras, label='Caras')
plt.plot(valores_n, prop_coroas, label='Coroas')
plt.xlabel('Número de lançamentos')
plt.ylabel('Proporção')
plt.title('Simulação de Lançamento de Moeda')
plt.legend()
plt.show()
