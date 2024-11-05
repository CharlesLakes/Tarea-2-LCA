import matplotlib.pyplot as plt
import numpy as np

# Datos de la tabla
testcase_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
sizes = [15, 32, 10, 37, 20, 25, 16, 143, 145, 203, 179, 195, 651, 343, 251]
times = [0.00189, 0.00231, 0.00186, 0.00246, 0.00221, 0.00237, 0.00240, 0.00540, 
         0.01497, 0.01726, 0.01552, 0.01635, 2.91683, 1.43746, 1.04309]

# Crear una figura y un eje
plt.figure(figsize=(12, 6))

# Gráfico de dispersión para el tamaño del universo en función del tiempo
plt.scatter(times, sizes, color='blue', marker='o')

# Etiquetas y título
plt.xlabel('Tiempo (s)')
plt.ylabel('Tamaño del Universo')
plt.title('Tamaño del Universo vs Tiempo de Ejecución de los Testcases')

# Añadir líneas de referencia
for i, txt in enumerate(testcase_numbers):
    plt.annotate(txt, (times[i], sizes[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Mostrar el gráfico
plt.grid()
plt.show()
