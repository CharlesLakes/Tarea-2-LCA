import random

# Definir paquetes, versiones y posibles dependencias/conflictos
packages = [
    "python", "java", "ruby", "c++", "c", "openssl", "jdk", "perl", "php",
    "nodejs", "rust", "go", "swift", "kotlin", "dotnet", "typescript", "scala",
    "haskell", "elixir", "dart", "lua", "groovy", "fortran", "bash", "shell",
    "R", "objective-c", "swift", "visual-basic", "assembly", "matlab", "sql",
    "powershell", "tcl", "csharp", "f#", "clojure", "erlang", "prolog"
]

versions = [
    "1.0", "1.1", "1.2", "1.3", "2.0", "2.1", "2.2", "2.9.1", "3.0", "3.1",
    "3.6.0", "3.7.2", "3.8.5", "4.0", "5.0", "6.1.0", "7.2", "8.0", "9.3",
    "10.0", "11", "11.0.2", "12", "13", "14", "15.0", "16.5", "17.2",
    "1.0.0", "1.1.0", "1.1.1", "1.2.3", "2.1.0", "3.2.0",
    "4.0.0", "4.1.0", "5.0.0", "6.0.0", "7.0.0", "8.0.0", "9.0.0", "10.0.0",
    "11.0.0", "12.0.0", "13.0.0", "14.0.0", "15.0.0"
]


max_deps = 100
max_conflicts = 100
max_installed = 1000

# Función para crear dependencias o conflictos aleatorios
def create_random_reqs(package_list, version_list, max_count):
    reqs = []
    count = random.randint(0, max_count)
    for _ in range(count):
        pkg = random.choice(package_list)
        ver = random.choice(version_list)
        reqs.append((pkg, ver))
    return reqs

# Generador de casos de prueba
def generate_testcase(filename):
    # Estructura de datos para almacenar el universo
    universe = {}
    U = random.randint(5, len(packages) * len(versions) // 2)

    for _ in range(U):
        package = random.choice(packages)
        version = random.choice(versions)

        # Asegurarse de que cada paquete+versión sea único
        if package not in universe:
            universe[package] = {}
        if version in universe[package]:
            continue

        # Generar dependencias y conflictos aleatorios
        depends = [create_random_reqs(packages, versions, max_deps) for _ in range(random.randint(0, max_deps))]
        conflicts = create_random_reqs(packages, versions, max_conflicts)
        universe[package][version] = {'depends': depends, 'conflicts': conflicts}

    # Generar dependencias ya instaladas
    installed = [(random.choice(packages), random.choice(versions)) for _ in range(random.randint(1, max_installed))]

    # Seleccionar el programa a instalar
    program_to_install = f"{random.choice(packages)} {random.choice(versions)}"

    U = sum([len(universe[package]) for package in universe])
    
    # Ahora escribe los datos en el archivo
    with open(filename, 'w') as f:
        # Número total de paquetes y versiones en el universo
        f.write(f"{U}\n")
        for package in universe:
            for version in universe[package]:
                # Escribir información del paquete y versión
                f.write(f"{package} {version}\n")
                depends = universe[package][version]['depends']
                f.write(f"{len(depends)}\n")
                for depend_list in depends:
                    f.write(f"{len(depend_list)}\n")
                    for dep_pkg, dep_ver in depend_list:
                        f.write(f"{dep_pkg} {dep_ver}\n")

                conflicts = universe[package][version]['conflicts']
                f.write(f"{len(conflicts)}\n")
                for conflict_pkg, conflict_ver in conflicts:
                    f.write(f"{conflict_pkg} {conflict_ver}\n")

        # Escribir dependencias ya instaladas
        f.write(f"{len(installed)}\n")
        for inst_pkg, inst_ver in installed:
            f.write(f"{inst_pkg} {inst_ver}\n")

        # Escribir el programa a instalar
        f.write(f"{program_to_install}\n")

    print("Caso de prueba generado y guardado en", filename)
    return universe, installed, program_to_install

# Generar un caso de prueba aleatorio en `testcase.txt`
generate_testcase('testcase.txt')
