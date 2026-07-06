import subprocess

def compile_lib():
    command = ["make", "-C", "core_c", "lib"]
    try:
        output = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Compilação concluída")
        print(output.stdout)
    except subprocess.CalledProcessError as e:
        print("Erro de compilação")
        print(e.stderr)

if __name__ == "__main__":
    compile_lib()