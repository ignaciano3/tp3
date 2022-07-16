#!/usr/bin/python3

import csv
from grafo import Grafo
from biblioteca import camino_mas_corto_bfs, pagerank, pagerank_personalizado, todos_en_rango, ciclo_n
import sys

def crear_usuarios_canciones(usuarios, canciones, data):
    '''
    Tener un grafo no dirigido que relacione si a un usuario le gusta una canción (a un usuario le gusta una canción si armó una playlist con ella).
    Esto formará un grafo bipartito en el cual en un grupo estarán los usuarios, y en el otro las canciones.
    O(U + C)
    '''
    usuarios_canciones = Grafo(len(usuarios) + len(canciones), list(usuarios) + list(canciones))
    canciones_por_index = dict(zip(canciones, range(len(canciones))))
    usuarios_por_index = dict(zip(usuarios, range(len(usuarios))))
    
    for linea in data:
        playlist_name = linea[3]
        cancion = linea[1] + " - " + linea[2]
        cancion = canciones_por_index[cancion]
        usuario = linea[0]
        usuario = usuarios_por_index[usuario]
        usuarios_canciones.add_edge(usuario, cancion + len(usuarios), playlist_name)
    
    return usuarios_canciones

def crear_canciones_grafo(canciones, usuarios, data):
    '''
    Tener un grafo no dirigido relacionando canciones si aparecen en playlists de un mismo usuario 
    (no necesariamente ambas en la misma playlist; es decir, si una canción aparece en alguna playlist del usuario X,
    y otra canción aparece en alguna playlist del mismo usuario X, pudiendo ser la misma playlist, o no).
    Este es el grafo a tener en cuenta para los útimos 2 comandos (rango y ciclo).
    '''
    canciones_grafo = Grafo(len(canciones), canciones)
    canciones_por_index = dict(zip(canciones, range(len(canciones)))) # muy clave este
    
    dict_usuarios = dict.fromkeys(usuarios)
    for key in dict_usuarios.keys():
        dict_usuarios[key] = set() # esta porqueria q no hace bien el fromkeys sino asigna todas las keys a la misma lista :(
    
    for d in data:
        cancion = d[1] + ' - ' + d[2]
        usuario = d[0]
        dict_usuarios[usuario].add(cancion)
    
    for usuario in dict_usuarios.keys():
        canciones_del_usuario = dict_usuarios[usuario]
        while len(canciones_del_usuario) > 0:
            cancion_1 = canciones_del_usuario.pop()
            for cancion_2 in canciones_del_usuario:
                canciones_grafo.add_edge(canciones_por_index[cancion_1], canciones_por_index[cancion_2])        
        
    return canciones_grafo


def crear_canciones_ordenadas(usuarios_canciones, desfase):
    '''
    Pagerank en otras palabras
    '''
    canciones_ordenadas = pagerank(usuarios_canciones)[desfase:] #np.argsort 

    i = 0
    for v in range(len(canciones_ordenadas)):
        canciones_ordenadas[v] = (canciones_ordenadas[v], i)
        i += 1
    
    canciones_ordenadas.sort(key = lambda x : x[0], reverse= True)
    return canciones_ordenadas


def camino_mas_corto(req, usuario_canciones_grafo, usuarios_canciones_index, desfase):
    canciones = " ".join(req)
    canciones = canciones.split(" >>>> ")
    try:
        cancion_1 = usuarios_canciones_index[canciones[0]]
        cancion_2 = usuarios_canciones_index[canciones[1]]
        if (cancion_1 < desfase or cancion_2 < desfase): raise NotADirectoryError #metodos poco ortodoxos pero 100% validos
    except:
        print("Tanto el origen como el destino deben ser canciones")
        return
    camino_mas_corto_bfs(usuario_canciones_grafo, cancion_1, cancion_2)


def ciclo_n_canciones(req, canciones_grafo, canciones_por_index):
    n = int(req[0])
    cancion = canciones_por_index[" ".join(req[1:])]
    ciclo_n(canciones_grafo, cancion, n)


def rango_n_canciones(req, canciones_grafo, canciones_por_index):
    n = int(req[0])
    cancion = canciones_por_index[" ".join(req[1:])]
    todos_en_rango(canciones_grafo, cancion, n)


def mas_importantes(n, canciones_ordenadas, usuarios_canciones, desfase):
    for i in range (n-1):
        print(usuarios_canciones.info(canciones_ordenadas[i][1]+desfase), end = "; ")
    print(usuarios_canciones.info(i+1+desfase))
    

def recomendacion_canciones(n, req, usuarios_canciones, usuarios_canciones_index, desfase, canciones_ordenadas):
    canciones = " ".join(req)
    canciones = canciones.split(sep=" >>>> ")
    for i in range(len(canciones)):
        canciones[i] = usuarios_canciones_index[canciones[i]]

    canciones_ordenadas = pagerank_personalizado(usuarios_canciones, canciones)[desfase:]
    
    i = 0
    for v in range(len(canciones_ordenadas)):
        canciones_ordenadas[v] = (canciones_ordenadas[v], i)
        i += 1
    
    canciones_ordenadas.sort(key = lambda x : x[0], reverse= True)

    mas_importantes(n, canciones_ordenadas, usuarios_canciones, desfase)


def recomendacion_usuarios(n, req, usuarios_canciones, usuarios_canciones_index, desfase):
    canciones = " ".join(req)
    canciones = canciones.split(sep=" >>>> ")
    for i in range(len(canciones)):
        canciones[i] = usuarios_canciones_index[canciones[i]]
    usuarios_ordenados = pagerank_personalizado(usuarios_canciones, canciones)[:desfase]
    
    i = 0
    for v in range(len(usuarios_ordenados)):
        usuarios_ordenados[v] = (usuarios_ordenados[v], i)
        i += 1
    
    usuarios_ordenados.sort(key = lambda x : x[0], reverse= True)

    mas_importantes(n, usuarios_ordenados, usuarios_canciones, desfase=0)



def main():
    if len(sys.argv) == 1:
        filename = 'spotify-mini.tsv'
    else:
        filename = sys.argv[-1]
    
    with open (filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        data = list(reader)

    del data[0] # header
    for elem in data:
        del elem[0]
        del elem[3]
        del elem[4]
    
    #data = data[["USER_ID", "TRACK_NAME", "ARTIST", "PLAYLIST_NAME"]] #unicos necesarios

    usuarios_unicos = list(set([v[0] for v in data]))
    canciones_unicas = list(set([v[1] + ' - '+ v[2] for v in data]))

    canciones_grafo_index = dict(zip(canciones_unicas, range(len(canciones_unicas))))
    lista_usuarios_canciones = usuarios_unicos + canciones_unicas
    usuario_canciones_index = dict(zip(lista_usuarios_canciones, range(len(lista_usuarios_canciones))))

    desfase = len(usuarios_unicos)

    canciones_grafo = None # lo hago asi para solo cargarlo cuando sea necesario y no todo al mismo tiempo
    canciones_ordenadas = None
    usuarios_canciones = None

    while True:
        try:
            req = input().split()
        except:
            break
        
        if not req: break
        
        if req[0] == "camino":
            if usuarios_canciones == None:
                usuarios_canciones = crear_usuarios_canciones(usuarios_unicos, canciones_unicas, data)
            camino_mas_corto(req[1:], usuarios_canciones, usuario_canciones_index, desfase)

        elif req[0] == "recomendacion":
            if usuarios_canciones == None:
                usuarios_canciones = crear_usuarios_canciones(usuarios_unicos, canciones_unicas, data)
            if canciones_ordenadas == None:
                canciones_ordenadas = crear_canciones_ordenadas(usuarios_canciones, desfase)
                
            n = int(req[2])
            if req[1] == "canciones":
                recomendacion_canciones(n, req[3:], usuarios_canciones, usuario_canciones_index, desfase, canciones_ordenadas)
            if req[1] == "usuarios":
                recomendacion_usuarios(n, req[3:], usuarios_canciones, usuario_canciones_index, desfase)
        
        
        elif req[0] == "mas_importantes":
            if usuarios_canciones == None:
                usuarios_canciones = crear_usuarios_canciones(usuarios_unicos, canciones_unicas, data)
            if canciones_ordenadas == None:
                canciones_ordenadas = crear_canciones_ordenadas(usuarios_canciones, desfase)
            n = int(req[1])
            mas_importantes(n, canciones_ordenadas, usuarios_canciones, desfase)

        

        elif req[0] == "ciclo":
            if canciones_grafo == None:
                canciones_grafo = crear_canciones_grafo(canciones_unicas, usuarios_unicos, data)
            ciclo_n_canciones(req[1:], canciones_grafo, canciones_grafo_index)

        elif req[0] == "rango":
            if canciones_grafo == None:
                canciones_grafo = crear_canciones_grafo(canciones_unicas, usuarios_unicos, data)
            rango_n_canciones(req[1:], canciones_grafo, canciones_grafo_index)
            
            

main()