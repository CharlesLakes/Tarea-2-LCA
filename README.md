# Tarea 2 - LÓGICA COMPUTACIONAL APLICADA

Este repositorio contiene un script en Python que utiliza la biblioteca `PySAT` para resolver problemas de actualizabilidad de paquetes en sistemas Linux. El objetivo del script es determinar cómo se deben instalar, eliminar o actualizar paquetes en un universo definido de paquetes y versiones, considerando sus dependencias y conflictos.

Se puede acceder al codigo desde COLAB (Este codigo no es la versión final, a comparación del contenido del repositorio): ![COLAB](https://colab.research.google.com/drive/1fwuvcV_jObPwqm5S3v-rkOx-tn-wlqVP?usp=sharing)

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Uso](#uso)
- [Descripción del Código](#descripción-del-código)
- [Ejemplo de Entrada](#ejemplo-de-entrada)
- [Resultados](#resultados)

## Requisitos

Para ejecutar este script, necesitarás tener instalados los siguientes paquetes:

- Python 3.x
- PySAT

Puedes instalar `PySAT` utilizando `pip`:

```bash
pip install pysat
```

## Uso

1. Asegúrate de que el archivo `testcase.txt` esté en el mismo directorio que el script.
2. Ejecuta el script:

```bash
python main.py
```

3. El script leerá el archivo `testcase.txt`, procesará los datos y mostrará los resultados en la consola.

## Descripción del Código

El código está organizado en varias funciones que manejan diferentes aspectos del problema de actualizabilidad:

- **Funciones de variables**: 
  - `get_var()`, `get_removed_var()`, `get_changed_var()`, `get_not_updated_var()`, `get_new_var()`: Devuelven identificadores de variables únicas para los paquetes y sus versiones.

- **Funciones de cláusulas**: 
  - `get_hard_clausules()`: Genera cláusulas duras basadas en dependencias y conflictos entre paquetes.
  - `get_soft_clausules()`: Genera cláusulas blandas que representan decisiones sobre la eliminación y cambio de paquetes.
  - `create_vars()`: Crea las variables necesarias para el problema, incluyendo las condiciones de eliminación y cambio de paquetes.

- **Función de lectura de casos de prueba**:
  - `read_testcase()`: Lee un archivo de texto que contiene la descripción del universo de paquetes, sus versiones, dependencias, conflictos y paquetes instalados.

## Ejemplo de Entrada

El archivo `testcase.txt` debe tener el siguiente formato:

```
N
paquete1 version1
número_de_dependencias
dep1 dep_ver1
dep2 dep_ver2
...
número_de_conflictos
conf1 conf_ver1
conf2 conf_ver2
...
paquete2 version2
...
número_de_paquetes_instalados
inst_pkg1 inst_ver1
inst_pkg2 inst_ver2
...
paquete_a_instalar
```

Donde `N` es el número total de paquetes y versiones en el universo.

## Resultados

Al finalizar la ejecución, el script mostrará:

- El tiempo de ejecución.
- Si se encontró o no una solución.
- El costo asociado a la solución (si corresponde).
- La cantidad de paquetes instalados, así como una lista de los paquetes eliminados y actualizados.
