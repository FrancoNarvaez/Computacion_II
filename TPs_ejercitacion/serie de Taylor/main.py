#Serie de Taylor
import threading as th
import math as m


def taylor(valor_X, i):
    global f_taylor
    global signo
    if signo == -1:
        signo= 1
    else:
        signo=-1
    l.acquire()
    term_taylor =signo*(1/(m.factorial(i+1))) * (float(valor_X)**(i+1))
    f_taylor.append(term_taylor)
    l.release()

def sumas():
    global f_taylor
    global suma

    for i in f_taylor:
        l.acquire()
        suma += i
        l.release()

if __name__ == '__main__':

    signo=int(-1)
    suma = float(0.0) 
    f_taylor=[]
    cantidad_de_terminos=int(12)
    valor_X=float(0.7853981633974483)
    valor_referencia=float(0.7071067811865475)
    l = th.Lock()

    for i in range(cantidad_de_terminos+1):
        hilo_terminos = th.Thread(target=taylor, args= (valor_X, i))
        hilo_terminos.start()
        hilo_terminos.join()

    hilo_suma = th.Thread(target=sumas)
    hilo_suma.start()
    hilo_suma.join()

    print(f'cantidad de terminos: {cantidad_de_terminos}')
    print(f'valor de X: {suma}')
    print(f'valor de referencia: {valor_referencia}')
    print(f'\nlista {f_taylor}')