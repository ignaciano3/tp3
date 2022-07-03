import pandas as pd
from Grafo import Grafo, Grafo_con_datos

# Grafo ejemplo
dijk = Grafo(7)
dijk.add_edge(0,1,2)
dijk.add_edge(0,2,4)
dijk.add_edge(1,3,7)
dijk.add_edge(1,4,5)
dijk.add_edge(2,4,1)
dijk.add_edge(2,5,3)
dijk.add_edge(3,4,2)
dijk.add_edge(3,6,5)
dijk.add_edge(4,5,4)
dijk.add_edge(4,6,7)
dijk.add_edge(5,6,3)

def crear_usuarios_canciones(usuarios, canciones, data):
    '''
    Tener un grafo no dirigido que relacione si a un usuario le gusta una canción (a un usuario le gusta una canción si armó una playlist con ella).
    Esto formará un grafo bipartito en el cual en un grupo estarán los usuarios, y en el otro las canciones.
    O(U + C)
    '''
    usuarios_canciones = Grafo_con_datos(len(usuarios) + len(canciones), list(usuarios) + list(canciones))
    for usuario in range(len(usuarios)):
        tabla_usuario = data[data.USER_ID == usuarios_canciones.info(usuario)]
        for _, cancion in tabla_usuario.iterrows():
            cancion = cancion.TRACK_NAME + " - " + cancion.ARTIST
            cancion = list(canciones).index(cancion)
            usuarios_canciones.add_edge(usuario, cancion + len(usuarios))
    
    return usuarios_canciones

def crear_canciones_por_playlist(canciones, playlists, data):
    '''
    Tener un grafo no dirigido relacionando canciones si aparecen en una misma playlist (al menos una playlist lista a ambas canciones).
    O (P + C²)
    '''
    canciones = list(canciones)
    canciones_grafo = Grafo_con_datos(len(canciones), canciones)
    for i in playlists:
        tabla_playlist = data[data.PLAYLIST_NAME == i]
        canciones_playlist = tabla_playlist.TRACK_NAME + " - " + tabla_playlist.ARTIST
        for v in canciones_playlist:
            for w in canciones_playlist:
                if v is not w:
                    canciones_grafo.add_edge(canciones.index(v), canciones.index(w))

    return canciones_grafo


def main():
    data = pd.read_csv('spotify-mini.tsv',sep='\t')
    
    lista_usuarios = data.USER_ID.unique()
    lista_canciones = (data.TRACK_NAME + " - " + data.ARTIST).unique()
    lista_playlists = data.PLAYLIST_NAME.unique()

    usuarios_canciones = crear_usuarios_canciones(lista_usuarios, lista_canciones, data)
    #canciones_grafo = crear_canciones_por_playlist(lista_canciones, lista_playlists, data)
    print(usuarios_canciones.todos_en_rango(100, 8))
     
    
    
    

main()