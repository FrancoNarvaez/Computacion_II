import os, sys, time

if len(sys.argv) > 3:
    print('Hay argumentos de más')
    sys.exit()

if sys.argv[1] != '-f':
    print('Falta el argumento "-f" antes del path o nombre del archivo')
    sys.exit()

archivo = sys.argv[2]

if not os.path.isfile(archivo):
    print(f"No se encontró el archivo: {archivo}")
    sys.exit()

with open(archivo, "r") as f:
    lines_arch = f.readlines()
print('se abrio el archivo')
# def main():
for i in lines_arch:
    r, w = os.pipe()
    r2, w2 = os.pipe()
    
    os.write(w,i.encode())
    
    pid = os.fork()
    
    if pid == 0:
        line = os.read(r, 100)

        line_str = line.decode("utf-8")
        reverseline_str = line_str[::-1]

        os.write(w2,reverseline_str.encode())
        sys.exit(0)
    
    inversed_line = os.read(r2, 100)
    print(f'linea original:\n{i}')     
    print(f'linea inversa:{inversed_line.decode("utf-8")}\n')

# por terminal (python3 TP1.py -f texto.txt)