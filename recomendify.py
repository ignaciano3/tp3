#!/usr/bin/python3

import pandas as pd
from grafo import Grafo
from biblioteca import camino_mas_corto_bfs, pagerank, todos_en_rango, ciclo_n
import numpy as np

def crear_usuarios_canciones(usuarios, canciones, data):
    '''
    Tener un grafo no dirigido que relacione si a un usuario le gusta una canción (a un usuario le gusta una canción si armó una playlist con ella).
    Esto formará un grafo bipartito en el cual en un grupo estarán los usuarios, y en el otro las canciones.
    O(U + C)
    '''
    usuarios_canciones = Grafo(len(usuarios) + len(canciones), list(usuarios) + list(canciones))
    canciones_por_index = dict(zip(canciones, range(len(canciones))))
    usuarios_por_index = dict(zip(usuarios, range(len(usuarios))))
    
    for _, linea in data.iterrows():
        playlist_name = linea.PLAYLIST_NAME
        cancion = linea.TRACK_NAME + " - " + linea.ARTIST
        cancion = canciones_por_index[cancion]
        usuario = linea.USER_ID
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
        tabla_usuario = data[data.USER_ID == i]
        tabla_usuario = tabla_usuario.TRACK_NAME + " - " + tabla_usuario.ARTIST
        tabla_usuario = set(tabla_usuario)
        while len(tabla_usuario) > 0:
            cancion_1 = tabla_usuario.pop()
            for cancion_2 in tabla_usuario:
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


def mas_importantes(req, canciones_ordenadas, usuarios_canciones):
    n = int(req[0])
    for i in range (n-1):
        print(usuarios_canciones.info(canciones_ordenadas[i]+169), end = "; ")
    
    print(usuarios_canciones.info(i+1+169))
    

def recomendacion_canciones(req):


    pass

def recomendacion_usuarios(n):
    pass


def main():
    data = pd.read_csv('spotify-mini.tsv',sep='\t')
    data = data[["USER_ID", "TRACK_NAME", "ARTIST", "PLAYLIST_NAME"]] #unicos necesarios
    
    lista_usuarios = data.USER_ID.unique()
    lista_canciones = (data.TRACK_NAME + " - " + data.ARTIST).unique()
    lista_playlists = data.PLAYLIST_NAME.unique()
    canciones_por_index = dict(zip(lista_canciones, range(len(lista_canciones))))

    usuarios_canciones = crear_usuarios_canciones(lista_usuarios, lista_canciones, data)
    canciones_grafo = crear_canciones_grafo(lista_canciones, lista_usuarios, data)
    
    """
    recomendacion canciones 10 
    Love Story - Taylor Swift
    Toxic - Britney Spears
    I Wanna Be Yours - Arctic Monkeys
    Hips Don't Lie (feat. Wyclef Jean) - Shakira
    Death Of A Martian - Red Hot Chili Peppers
    """
    pagerank_list = pagerank(usuarios_canciones)[169:]
    canciones_ordenadas = np.argsort(pagerank_list)
    canciones_ordenadas = np.flip(canciones_ordenadas)

    while True:
        req = input().split()
        
        if not req: break

        if req[0] == "camino":
            camino_mas_corto(req[1:], usuarios_canciones, canciones_por_index)

        elif req[0] == "recomendacion":
            if req[1] == "canciones":
                recomendacion_canciones(req[2])
            if req[1] == "usuarios":
                recomendacion_usuarios(req[2])
        
        
        elif req[0] == "mas_importantes":
            mas_importantes(req[1:], canciones_ordenadas, usuarios_canciones)

        elif req[0] == "ciclo":
            ciclo_n_canciones(req[1:], canciones_grafo, canciones_por_index)

        elif req[0] == "rango":
            rango_n_canciones(req[1:], canciones_grafo, canciones_por_index)
            
            

main()