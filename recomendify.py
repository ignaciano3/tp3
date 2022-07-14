#!/usr/bin/python3

import pandas as pd
from grafo import Grafo
from biblioteca import camino_mas_corto_bfs, todos_en_rango, ciclo_n

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

def crear_canciones_por_playlist(canciones, playlists, data):
    '''
    Tener un grafo no dirigido relacionando canciones si aparecen en una misma playlist (al menos una playlist lista a ambas canciones).
    O (P + C)
    '''
    cancion_vs_playlist = list()
    
    for i in playlists:
        tabla_playlist = data[data.PLAYLIST_NAME == i]
        tabla_playlist = tabla_playlist.TRACK_NAME + " - " + tabla_playlist.ARTIST
        cancion_vs_playlist.append(set(tabla_playlist))

    canciones = list(canciones)
    canciones_por_playlist = Grafo(len(canciones), canciones)
    canciones_por_index = dict(zip(canciones, range(len(canciones)))) # muy clave este
    
    for p in cancion_vs_playlist:
        while len(p) > 0:
            cancion_1 = p.pop()
            for cancion_2 in p:
                canciones_por_playlist.add_edge(canciones_por_index[cancion_1], canciones_por_index[cancion_2])
    
    return canciones_por_playlist


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


def mas_importantes(n):
    pass

def recomendacion_canciones(n):
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
    canciones_grafo = crear_canciones_por_playlist(lista_canciones, lista_playlists, data)
    
    while True:
        req = input().split()
        
        if not req: break

        if (req[0] == "camino"):
            #tengo que arreglar este
            camino_mas_corto(req[1:], usuarios_canciones, canciones_por_index)

        elif (req[0] == "recomendacion"):
            if (req[1] == "canciones"):
                recomendacion_canciones(req[2])
            if (req[1] == "usuarios"):
                recomendacion_usuarios(req[2])
        
        
        elif (req[0] == "mas_importantes"):
            mas_importantes(req[1:])

        elif (req[0] == "ciclo"):
            ciclo_n_canciones(req[1:], canciones_grafo, canciones_por_index)

        elif (req[0] == "rango"):
            rango_n_canciones(req[1:], canciones_grafo, canciones_por_index)
            
            

main()