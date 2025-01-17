medicoes = [
(1.48, 0.16),
(1.5, 0.5),
(1.51, 1),
(1.52, 1.5),
(1.54, 2),
(1.56, 2.5),
(1.57, 3),
(1.59, 3.5),
(1.61, 4),
(1.62, 4.5),
(1.64, 5),
(1.65, 5.5),
(1.67, 6),
(1.69, 6.5),
(1.7, 7),
(1.72, 7.5),
(1.74, 8),
(1.75, 8.5),
(1.76, 9),
(1.77, 9.5),
(1.78, 10),
(1.8, 10.5),
(1.81, 11),
(1.83, 11.5),
(1.85, 12),
(1.86, 12.5),
(1.88, 13),
(1.89, 13.5),
(1.91, 14),
(1.92, 14.5),
(1.94, 15),
(1.96, 15.5),
(1.98, 16),
(1.99, 16.5),
(2, 17),
(2.02, 17.5),
(2.04, 18),
(2.05, 18.5),
(2.07, 19),
(2.08, 19.5),
(2.09, 20),
(2.11, 20.5),
(2.12, 21),
(2.14, 21.5),
(2.15, 22),
(2.17, 22.5),
(2.18, 23),
(2.2, 23.5),
(2.22, 24),
(2.23, 24.5),
(2.25, 25),
(2.26, 25.5),
(2.28, 26),
(2.3, 26.5),
(2.31, 27),
(2.33, 27.5),
(2.34, 28),
(2.36, 28.5),
(2.37, 29),
(2.39, 29.5),
(2.41, 30),
(2.42, 30.5),
(2.44, 31),
(2.46, 31.5),
(2.47, 32),
(2.48, 32.5),
(2.5, 33),
(2.52, 33.5),
(2.53, 34),
(2.55, 34.5),
(2.56, 35),
(2.57, 35.5),
(2.59, 36),
(2.61, 36.5),
(2.63, 37),
(2.65, 37.5),
(2.67, 38)
# es conforme necessário
]

def calcular_coeficientes(medicoes):
    """Calcula os coeficientes a e b para a calibração linear."""
    n = len(medicoes)
    soma_x = sum(x for x, y in medicoes)
    soma_y = sum(y for x, y in medicoes)
    soma_xy = sum(x * y for x, y in medicoes)
    soma_x2 = sum(x ** 2 for x, y in medicoes)
    
    # Média dos valores
    media_x = soma_x / n
    media_y = soma_y / n
    
    # Coeficientes a e b
    a = (soma_xy - n * media_x * media_y) / (soma_x2 - n * media_x ** 2)
    b = media_y - a * media_x
    
    return a, b

def corrigir_tensao(tensao_lida, a, b):
    """Aplica a correção para a tensão lida."""
    return a * tensao_lida + b

# Calcular coeficientes
a, b = calcular_coeficientes(medicoes)
print(f"Coeficientes calculados: a={a}, b={b}")

# Exemplo de correção
tensao_lida = 1.8  # Valor lido pelo ESP32
tensao_corrigida = corrigir_tensao(tensao_lida, a, b)
print(f"Tensão corrigida: {tensao_corrigida:.2f} V")