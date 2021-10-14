#encoding: utf-8
import os
import glob

def preprocessor(code, lib_name=[]):
    lib_name = lib_name
    added = False

    lines = code.split("\n")

    prog_dir = os.path.dirname(__file__) + "/"
    pwd = os.getcwd() + "/"

    if "^^" not in code:
        code = "^^" + code

    libs = []

    for line in lines:
        line = line.split()

        if len(line) < 2: continue

        if line[0] != "import": continue

        libs += line[1:]
    
    libs = list(filter(lambda x: x not in ["", " "], sum(list(map(lambda x: x.split(","), libs)), [])))

    lib_code = ""

    for lib in libs:
        if lib in lib_name: continue
        lib_name.append(lib)

        added = True

        fn = ""
        if os.path.isfile(prog_dir + "libs/" + lib + ".se"):
            fn = prog_dir + "libs/" + lib + ".se"

        if os.path.isfile(prog_dir + lib + ".se"):
            fn = prog_dir + lib + ".se"

        elif os.path.isfile(pwd + lib + ".se"):
            fn = pwd + lib + ".se"

        elif os.path.isfile(lib + ".se"):
            fn = lib + ".se"
            
        elif os.path.isfile(lib):
            fn = lib

        if fn == "": continue

        with open(fn, mode="r", encoding="utf-8") as f:
            lib_code += f.read()

    lines = code.split("\n")
    removed_code = ""

    for line in lines:
        if line[:6] != "import":
            removed_code += line + "\n"

    return lib_code + code, added, lib_name
