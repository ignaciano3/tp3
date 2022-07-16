#!/usr/bin/python3

import csv
from grafo import Grafo
from biblioteca import camino_mas_corto_bfs, pagerank, pagerank_personalizado, todos_en_rango, ciclo_n
import numpy as np
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
    
    for i in usuarios:
        tabla_usuario = np.where(data[:,0] == i)
        canciones_del_usuario = set()
        for x in data[tabla_usuario]:
            canciones_del_usuario.add(x[1] + ' - '+ x[2])
        while len(canciones_del_usuario) > 0:
            cancion_1 = canciones_del_usuario.pop()
            for cancion_2 in canciones_del_usuario:
                canciones_grafo.add_edge(canciones_por_index[cancion_1], canciones_por_index[cancion_2])
        
    return canciones_grafo


def camino_mas_corto(req, usuario_canciones_grafo, canciones_por_index):
    canciones = " ".join(req)
    canciones = canciones.split(" >>>> ")
    try:
        cancion_1 = canciones_por_index[canciones[0]]
        cancion_2 = canciones_por_index[canciones[1]]
    except:
        print("Tanto el origen como el destino deben ser canciones")
        return
    camino_mas_corto_bfs(usuario_canciones_grafo, cancion_1+169, cancion_2+169)


def ciclo_n_canciones(req, canciones_grafo, canciones_por_index):
    n = int(req[0])
    cancion = canciones_por_index[" ".join(req[1:])]
    ciclo_n(canciones_grafo, cancion, n)


def rango_n_canciones(req, canciones_grafo, canciones_por_index):
    n = int(req[0])
    cancion = canciones_por_index[" ".join(req[1:])]
    todos_en_rango(canciones_grafo, cancion, n)


def mas_importantes(n, canciones_ordenadas, usuarios_canciones, desfase = 169):
    for i in range (n-1):
        print(usuarios_canciones.info(canciones_ordenadas[i]+desfase), end = "; ")
    print(usuarios_canciones.info(i+1+desfase))
    

def recomendacion_canciones(n, req, usuarios_canciones, usuarios_canciones_index):
    canciones = " ".join(req)
    canciones = canciones.split(sep=" >>>> ")
    for i in range(len(canciones)):
        canciones[i] = usuarios_canciones_index[canciones[i]]
    pagerank_personalizado_list = pagerank_personalizado(usuarios_canciones, canciones)[169:]
    canciones_ordenadas = np.argsort(pagerank_personalizado_list)
    canciones_ordenadas = np.flip(canciones_ordenadas)

    mas_importantes(n, canciones_ordenadas, usuarios_canciones)


def recomendacion_usuarios(n, req, usuarios_canciones, usuarios_canciones_index):
    canciones = " ".join(req)
    canciones = canciones.split(sep=" >>>> ")
    for i in range(len(canciones)):
        canciones[i] = usuarios_canciones_index[canciones[i]]
    pagerank_personalizado_list = pagerank_personalizado(usuarios_canciones, canciones)[:169]
    usuarios_ordenados = np.argsort(pagerank_personalizado_list)
    usuarios_ordenados = np.flip(usuarios_ordenados)

    mas_importantes(n, usuarios_ordenados, usuarios_canciones, desfase=0)


def main():
    if len(sys.argv) == 1:
        filename = 'spotify-mini.tsv'
    else:
        filename = sys.argv[-1]
    
    with open (filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        data = np.array(list(reader))
        data = np.delete(data, 0, 0) # saco headers
        data = np.delete(data, [0, 4, 6], 1) # saco columnas innecesarias
        
    #data = data[["USER_ID", "TRACK_NAME", "ARTIST", "PLAYLIST_NAME"]] #unicos necesarios
    
    usuarios_unicos = np.unique(data[:,0], axis=0)
    canciones_unicas = set()
    for i in data: # que lindo no poder usar pandas arroba sarcasmo
        canciones_unicas.add(i[1] + " - " + i[2])
    canciones_unicas = np.array(list(canciones_unicas))


    canciones_grafo_index = dict(zip(canciones_unicas, range(len(canciones_unicas))))
    lista_usuarios_canciones = np.concatenate((usuarios_unicos, canciones_unicas))
    usuario_canciones_index = dict(zip(lista_usuarios_canciones, range(len(lista_usuarios_canciones))))

    usuarios_canciones = crear_usuarios_canciones(usuarios_unicos, canciones_unicas, data)
    canciones_grafo = crear_canciones_grafo(canciones_unicas, usuarios_unicos, data)
    
    pagerank_list = pagerank(usuarios_canciones)[169:]
    canciones_ordenadas = np.argsort(pagerank_list)
    canciones_ordenadas = np.flip(canciones_ordenadas)

    while True:
        req = input().split()
        
        if not req: break

        if req[0] == "camino":
            camino_mas_corto(req[1:], usuarios_canciones, canciones_grafo_index)

        elif req[0] == "recomendacion":
            n = int(req[2])
            if req[1] == "canciones":
                recomendacion_canciones(n, req[3:], usuarios_canciones, usuario_canciones_index)
            if req[1] == "usuarios":
                recomendacion_usuarios(n, req[3:], usuarios_canciones, usuario_canciones_index)
        
        
        elif req[0] == "mas_importantes":
            n = int(req[1])
            mas_importantes(n, canciones_ordenadas, usuarios_canciones)

        elif req[0] == "ciclo":
            ciclo_n_canciones(req[1:], canciones_grafo, canciones_grafo_index)

        elif req[0] == "rango":
            rango_n_canciones(req[1:], canciones_grafo, canciones_grafo_index)
            
            

main()