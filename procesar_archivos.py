### Utilidades para procesar archivos
import os
####################################################################
# Recorre la carpeta_origen, y por cada subcarpeta que se encuentra
# entra y cambia el nombre de todos los ficheros eliminando la cadena
####################################################################
def eliminar_cadena_de_subcarpetas(carpeta_origen, cadena_a_eliminar):
    lista_subdirectorios = os.listdir(carpeta_origen)
    for dir in lista_subdirectorios:
        lista_ficheros = os.listdir(carpeta_origen+'\\'+dir)
        for fichero in lista_ficheros:
            nuevo_nombre = fichero.replace(cadena_a_eliminar,'')
            print(nuevo_nombre)
            os.rename(carpeta_origen+'\\'+dir+'\\'+fichero,carpeta_origen+'\\'+dir+'\\'+nuevo_nombre)
    return 0
    
print(eliminar_cadena_de_subcarpetas('H:\Fuentes de audio\Musica\MP3\Resto\Pink Floyd', 'Pink Floyd - '))