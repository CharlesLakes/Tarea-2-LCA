from pysat.formula import WCNF, IDPool, Equals
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
import time

vpool = IDPool()
vpool_reverse = {}

def get_var(package,version):
  if f"{package}_{version}" not in vpool_reverse:
    vpool_reverse[vpool.id(f"{package}_{version}")] = f"{package}_{version}"
  return vpool.id(f"{package}_{version}")

def get_removed_var(package):
  if f"{package}_removed" not in vpool_reverse:
    vpool_reverse[vpool.id(f"{package}_removed")] = f"{package}_removed"
  return vpool.id(f"{package}_removed")

def get_changed_var(package):
  if f"{package}_changed" not in vpool_reverse:
    vpool_reverse[vpool.id(f"{package}_changed")] = f"{package}_changed"
  return vpool.id(f"{package}_changed")

def get_not_updated_var(package):
  if f"{package}_not_updated" not in vpool_reverse:
    vpool_reverse[vpool.id(f"{package}_not_updated")] = f"{package}_not_updated"
  return vpool.id(f"{package}_not_updated")

def get_new_var(package):
  if f"{package}_new" not in vpool_reverse:
    vpool_reverse[vpool.id(f"{package}_new")] = f"{package}_new"
  return vpool.id(f"{package}_new")


def get_hard_clausules(Universe,cnf):
  for package in Universe:
    atmost_clause = []
    for version in Universe[package]:
      var = get_var(package,version)
      atmost_clause.append(var)

      # Dependencias
      for depend in Universe[package][version]["depends"]:
        clause = [-var]
        for dependency in depend:
          dependency_var = get_var(dependency[0],dependency[1])
          clause.append(dependency_var)
        cnf.append(clause)

      # Conflictos
      for conflict in Universe[package][version]["conflicts"]:
        conflict_var = get_var(conflict[0],conflict[1])
        cnf.append([-var,-conflict_var])
    
    # Restricción "a lo más uno" para las versiones del paquete
    cnf.extend(CardEnc.atmost(lits=atmost_clause,vpool=vpool,encoding=EncType.bitwise))

def get_soft_clausules(Universe,cnf,INSTALLED_WITHOUT_VERSION):
  U = sum([len(Universe[package]) for package in Universe])

  for package in INSTALLED_WITHOUT_VERSION:
    cnf.append([-get_removed_var(package)],U+1)
  
  for package in Universe:
    cnf.append([-get_changed_var(package)],1)

def create_vars(Universe,cnf,INSTALLED_WITHOUT_VERSION):

  # Create removed_pi
  for package in INSTALLED_WITHOUT_VERSION:
    clause = []
    for version in Universe[package]:
      clause.append(get_var(package,version))
    clause.append(get_removed_var(package))
    cnf.append(clause)

    for version in Universe[package]:
      cnf.append([-get_removed_var(package),-get_var(package,version)])

  # Create changed_pi
  for package in Universe:
    clause = []
    for version in Universe[package]:
      if f"{package}_{version}" in INSTALLED:
        clause.append(-get_var(package,version))
      else:
        clause.append(get_var(package,version))
    clause.append(-get_changed_var(package))
    cnf.append(clause)

    for version in Universe[package]:
      if f"{package}_{version}" in INSTALLED:
        cnf.append([get_var(package,version),get_changed_var(package)])
      else:
        cnf.append([-get_var(package,version),get_changed_var(package)])

def add_package(cnf,package,version):
  cnf.append([get_var(package,version)])

def read_testcase(filename):
  with open(filename, 'r') as file:
  # Leer el total de paquetes y versiones en el universo
    U = int(file.readline().strip())
    print("Total de paquetes y versiones en el universo:", U)

    # Leer los paquetes y versiones del universo
    universe = {}
    for _ in range(U):
      # Leer nombre y versión del paquete
      package, version = file.readline().strip().split()
      if package not in universe:
        universe[package] = {}
      universe[package][version] = {'depends': [], 'conflicts': []}

      # Leer dependencias
      depends_count = int(file.readline().strip())
      for _ in range(depends_count):
        depend_list = []
        depend_items = int(file.readline().strip())
        for _ in range(depend_items):
          dep_pkg, dep_ver = file.readline().strip().split()
          depend_list.append((dep_pkg, dep_ver))
        universe[package][version]['depends'].append(depend_list)

      # Leer conflictos
      conflicts_count = int(file.readline().strip())
      for _ in range(conflicts_count):
        conflict_pkg, conflict_ver = file.readline().strip().split()
        universe[package][version]['conflicts'].append((conflict_pkg, conflict_ver))

    # Leer dependencias ya instaladas
    installed_count = int(file.readline().strip())
    installed = set()
    installed_without_version = set()
    for _ in range(installed_count):
      inst_pkg, inst_ver = file.readline().strip().split()
      installed.add(f"{inst_pkg}_{inst_ver}")
      installed_without_version.add(inst_pkg)

    # Leer el programa a instalar
    program_to_install = file.readline().strip().split()

  # Imprimir o devolver la información leída
  #print("Universo:", universe)
  #print("Dependencias instaladas:", installed)
  #print("Programa a instalar:", program_to_install)

  return universe, installed, installed_without_version, program_to_install

start_time = time.time()

Universe, INSTALLED, INSTALLED_WITHOUT_VERSION, PROGRAM_TO_INSTALL = read_testcase("testcase.txt")

CNF = WCNF()

create_vars(Universe,CNF,INSTALLED_WITHOUT_VERSION)
get_hard_clausules(Universe,CNF)
get_soft_clausules(Universe,CNF,INSTALLED_WITHOUT_VERSION)

add_package(CNF,PROGRAM_TO_INSTALL[0],PROGRAM_TO_INSTALL[1])

with RC2(CNF) as rc2:
  result = rc2.compute()
  end_time = time.time()
  print("Tiempo de ejecucion:",end_time - start_time)
  if not result:
    print("No se encontró una solución.")
  else:
    print("Solución encontrada:")
    print("Costo:",rc2.cost)
    number_of_pkg_installed = 0
    for package in Universe:
      for version in Universe[package]:
        if get_var(package,version) in result:
          number_of_pkg_installed += 1
    print("Paquetes instalados:",number_of_pkg_installed)
    print("Paquetes removidos:")
    for package in INSTALLED_WITHOUT_VERSION:
      if get_removed_var(package) in result:
        print(f"- {package}")
    print("Paquetes actualizados:")
    for package in Universe:
      if get_changed_var(package) in result:
        print(f"- {package}")

