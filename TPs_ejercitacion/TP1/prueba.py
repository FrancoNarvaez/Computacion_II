import os, sys, time, signal

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
def padre_handler(signum, frame):
    print('padre recibio señal del hijo\n')

def hijo_handler(signum, frame):
    print('hijo recibio señal del padre\n')

for i in lines_arch:
       padre_hijo, hijo_padre = os.pipe()
       pid = os.fork()

       if pid == 0:
            #Proceso hijo
            os.close(hijo_padre)
            signal.signal(signal.SIGUSR1, hijo_handler)
            signal.pause()

            line = os.read(padre_hijo, 100)
            line_str = line.decode("utf-8")
            reverseline_str = line_str[::-1]
            os.open(hijo_padre)
            os.write(hijo_padre, reverseline_str)
            os.kill(os.getppid(), signal.SIGUSR1)
            os.close(padre_hijo)
            os.close(hijo_padre)

       else:
            