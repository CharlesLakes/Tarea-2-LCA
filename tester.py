import os

def read_data(file):
    f = open(file)
    d = f.read()
    f.close()
    return d

def write_data(file,data):
    f = open(file,"w")
    f.write(data)
    f.close()

tests = os.listdir("testcases")
for test in tests:
    data = read_data(f"testcases/{test}")
    write_data("testcase.txt",data)

    if "output" not in os.listdir("."):
        os.mkdir("output")

    os.system(f"python3 main.py > output/{test}")
    os.remove("testcase.txt")



