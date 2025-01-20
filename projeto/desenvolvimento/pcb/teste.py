from scipy.interpolate import interp1d
import numpy as np

# Dados fornecidos
tensao_fonte = [
    0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5,
    10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5,
    18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5,
    26, 26.5, 27, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31, 31.5, 32, 32.5, 33, 33.5,
    34, 34.5, 35, 35.5, 36, 36.5, 37, 37.5, 38
]

pino_medido = [
    1.48, 1.5, 1.51, 1.52, 1.54, 1.56, 1.57, 1.59, 1.61, 1.62, 1.64, 1.65, 1.67, 1.69,
    1.7, 1.72, 1.74, 1.75, 1.76, 1.77, 1.78, 1.8, 1.81, 1.83, 1.85, 1.86, 1.88, 1.89,
    1.91, 1.92, 1.94, 1.96, 1.98, 1.99, 2.0, 2.02, 2.04, 2.05, 2.07, 2.08, 2.09, 2.11,
    2.12, 2.14, 2.15, 2.17, 2.18, 2.2, 2.22, 2.23, 2.25, 2.26, 2.28, 2.3, 2.31, 2.33,
    2.34, 2.36, 2.37, 2.39, 2.41, 2.42, 2.44, 2.46, 2.47, 2.48, 2.5, 2.52, 2.53, 2.55,
    2.56, 2.57, 2.59, 2.61, 2.63, 2.65, 2.67
]

# Criando a função de interpolação
funcao_interpolacao = interp1d(pino_medido, tensao_fonte, kind='linear', fill_value="extrapolate")

def calcular_tensao_fonte(pino_medido_valor):
    """
    Calcula a tensão da fonte com base no valor medido no pino usando interpolação linear.
    
    Parâmetros:
        pino_medido_valor (float): Valor medido no pino.
        
    Retorna:
        float: Tensão estimada da fonte.
    """
    return float(funcao_interpolacao(pino_medido_valor))

# Exemplo de uso
valores_exemplo = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
for valor in valores_exemplo:
    tensao = calcular_tensao_fonte(valor)
    print(f"Pino medido: {valor} V -> Tensão da fonte: {tensao:.2f} V")
