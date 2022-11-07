#!/usr/bin/env python3

import sqlite3
import uuid
from restDir import excepciones

class ManagerBDS:
    ''' Clase que se comunica con la bbdd'''

    def __init__(self):
        '''Crea (si no existe) y se conecta a la bbdd e inicializa el directorio raíz'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("""create table if not exists Directorios ( 
                                    id text primary key,
                                    nombre text,
                                    padre text,
                                    hijos text,
                                    readable text,
                                    writable text,
                                    archivos text
                                    )""")

            conexion.commit()

            if(self.comprobar_raiz(cursor)):
                self.establecer_raiz(conexion)

            conexion.close()

        except sqlite3.OperationalError:
            print(f'Error al crear la tabla Directorios')  
    
    #Metodos base de datos
    def insertar_directorio(self, nombre, padre, user):
        '''Inserta un directorio en la bbdd'''

        id_dir = uuid.uuid1()
        readable = user
        writable = user

        dir = (str(id_dir), nombre, padre, "", readable, writable, "")

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_hijo_mismo_nombre(nombre, padre)):
                raise excepciones.hijo_mismo_nombre

            if(self.comprobar_existe_por_id(padre)):
                raise excepciones.directorio_no_existe

            conexion.execute("insert into Directorios(id,nombre,padre,hijos,readable,writable,archivos) values (?, ?, ?, ?, ?, ?, ?)", dir)
            conexion.commit()

            self.agregar_hijo_lista_padre(nombre, padre, cursor, conexion)

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.hijo_mismo_nombre:
            print(f'Ya existe un hijo con el mismo nombre')
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio padre introducido')

        return id_dir
        
    def borrar_directorio (self, nombre, padre, user):
        '''Elimina un directorio de la bbdd'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_exite_por_nombre_idPadre(nombre, padre, cursor)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_nombre_padre(nombre, padre, user, cursor)):
                raise excepciones.permiso_escritura

            conexion.execute("delete from Directorios where nombre=? and padre=?",(nombre, padre))
            conexion.commit()

            self.eliminar_hijo_lista_padre(nombre, padre, cursor, conexion)

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')   
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')     
    
    def añadir_permiso_lectura(self, id, propietario, invitado):
        '''Incluye a invitado en el atributo readable del directorio indicado'''
        
        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, propietario)):
                raise excepciones.permiso_escritura

            cursor.execute("select readable from Directorios where id=?",(id,))
            readable = cursor.fetchall()

            if(readable[0][0] == ""):
                cursor.execute("update Directorios set readable=? where id=?",(invitado, id))
                conexion.commit()
            else:
                usuarios = readable[0][0]
                usuarios += " "
                usuarios += invitado

                cursor.execute("update Directorios set readable=? where id=?",(usuarios, id))   
                conexion.commit()

                conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')   
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')        
    
    def añadir_permiso_escritura(self, id, propietario, invitado):
        '''Incluye a invitado en el atributo writable del directorio indicado'''
        
        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, propietario)):
                raise excepciones.permiso_escritura

            cursor.execute("select writable from Directorios where id=?",(id,))
            writable = cursor.fetchall()

            if(writable[0][0] == ""):
                cursor.execute("update Directorios set writable=? where id=?",(invitado, id))
                conexion.commit()
            else:
                usuarios = writable[0][0]
                usuarios += " "
                usuarios += invitado

                cursor.execute("update Directorios set writable=? where id=?",(usuarios, id))   
                conexion.commit()

                conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')   
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')
    
    def quitar_permiso_lectura(self, id, propietario, invitado):
        ''' Elimina a invitado del atributo readable del directorio indicado'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, propietario)):
                raise excepciones.permiso_escritura
            if(self.comprobar_lectura_id(id, invitado)):
                raise excepciones.permiso_lectura
            if(invitado == 'admin'):
                raise excepciones.quitar_permiso_admin

            cursor.execute("select readable from Directorios where id=?",(id,))
            readable = cursor.fetchall()
            usuarios = readable[0][0]

            if(usuarios.find(invitado) == 0):
                usuario = invitado + " "
            else:
                usuario = " " + invitado
                
            rep = usuarios.replace(usuario, "")
            cursor.execute("update Directorios set readable=? where id=?",(rep, id))
            conexion.commit()

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura') 
        except excepciones.permiso_lectura:
             print(f'El usuario no tiene permisos de lectura')  
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')
        except excepciones.quitar_permiso_admin:
            print(f'No se le pueden quitar permisos al admin')   
    
    def quitar_permiso_escritura(self, id, propietario, invitado):
        '''Elimina a invitado del atributo writable del directorio indicado'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, propietario)):
                raise excepciones.permiso_escritura
            if(self.comprobar_escritura_id(id, invitado)):
                raise excepciones.permiso_escritura
            if(invitado == 'admin'):
                raise excepciones.quitar_permiso_admin

            cursor.execute("select writable from Directorios where id=?",(id,))
            writable = cursor.fetchall()
            usuarios = writable[0][0]

            if(usuarios.find(invitado) == 0):
                usuario = invitado + " "
            else:
                usuario = " " + invitado
                
            rep = usuarios.replace(usuario, "")
            cursor.execute("update Directorios set writable=? where id=?",(rep, id))
            conexion.commit()

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')  
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')
        except excepciones.quitar_permiso_admin:
            print(f'No se le pueden quitar permisos al admin')
    
    def añadir_fichero (self, id, user, nombre, url):
        '''Añade un fichero a un directorio donde el user tenga permisos'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, user)):
                raise excepciones.permiso_escritura
            if(self.comprobar_hijo_mismo_nombre(nombre, id)):
                raise excepciones.hijo_mismo_nombre
            if(self.comprobar_archivo_mismo_nombre(id, nombre, cursor)):
                raise excepciones.hijo_mismo_nombre
            
            cursor.execute("select archivos from Directorios where id=?",(id,))
            archivos = cursor.fetchall()
            files = archivos[0][0]

            if(files == ""):
                files += nombre
                files += ','
                files += url
                cursor.execute("update Directorios set archivos=? where id=?",(files, id))
                conexion.commit()
            else:
                files += ' '
                files += nombre
                files += ','
                files += url
                cursor.execute("update Directorios set archivos=? where id=?",(files, id))
                conexion.commit()
            
            conexion.commit()

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')  
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')
        except excepciones.hijo_mismo_nombre:
            print(f'Ya existe un directorio o un archivo con el mismo nombre')
    
    def borrar_fichero (self, id, user, nombre):
        '''Elimina un fichero de un directorio donde le user tenga permisos'''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            if(self.comprobar_existe_por_id(id)):
                raise excepciones.directorio_no_existe
            if(self.comprobar_escritura_id(id, user)):
                raise excepciones.permiso_escritura
            if(self.comprobar_archivo_mismo_nombre(id, nombre, cursor) == False):
                raise excepciones.archivo_no_existe

            cursor.execute("select archivos from Directorios where id=?",(id,))
            archivos = cursor.fetchall()
            files = archivos[0][0]
            file = ''
            aux = files.split(' ')
            nombre_coma = nombre + ','
            j = True

            for i in aux:
                if(i.find(nombre_coma) == 0 and j):
                    file += i + ' '
                    break
                elif(i.find(nombre_coma) == 0 and j == False):
                    file += ' ' + i
                    break

                j = False
                
            rep = files.replace(file, "")
            cursor.execute("update Directorios set archivos=? where id=?",(rep, id))
            conexion.commit()

            conexion.close()

        except sqlite3.OperationalError:
            print (f'Error al crear el directorio')
        except excepciones.permiso_escritura:
             print(f'El usuario no tiene permisos de escritura')  
        except excepciones.directorio_no_existe:
            print(f'No existe el directorio introducido')
        except excepciones.archivo_no_existe:
            print(f'No existe ningun archivo con ese nombre')

    #Metodos de apoyo
    def establecer_raiz(self, conexion):
        ''' Establece el directorio raiz de la base de datos '''

        dir = ("root", "/", "none", "", "admin", "admin", "")

        try:
            conexion.execute("insert into Directorios(id,nombre,padre,hijos,readable,writable,archivos) values (?, ?, ?, ?, ?, ?, ?)", dir)
            conexion.commit()
        except sqlite3.OperationalError:
            print (f'Error al crear directorio raiz')

    def comprobar_raiz(self, cursor):
        ''' Comprueba si el directorio raiz ya esta creado  '''

        createRoot = True
        
        try:
            cursor.execute("select nombre from Directorios")
            directorios = cursor.fetchall()

            for i in directorios:
                if i[0] == '/':
                    createRoot = False
                    
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')
        
        return createRoot

    def listar_directorios(self, id):
        ''' Devuelve el nombre de todos los directorios en el directorios ''' 

        try:
            conexion = sqlite3.connect("directorios.db")
            cur = conexion.cursor()

            cur.execute("select hijos from Directorios where id=?",(id,))
            directorios = cur.fetchall()
            files = directorios[0][0]
            files_list = files.split(' ')
            response = ''
            counter = 0

            for i in files_list:

                if(counter == len(files_list) - 1):
                    response += f'{i}'
                    break

                response += f'{i} '
                counter += 1

            conexion.close()

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return response

    def listar_archivos(self, id):

        try:
            conexion = sqlite3.connect("directorios.db")
            cur = conexion.cursor()

            cur.execute("select archivos from Directorios where id=?",(id,))
            directorios = cur.fetchall()
            files = directorios[0][0]
            files_list = files.split(' ')
            counter = 0

            response = ''

            for i in files_list:
                
                if(counter == len(files_list) - 1):
                    file = i.split(',')
                    name = file[0]
                    response += f'{name}'
                    break

                file = i.split(',')
                name = file[0]
                response += f'{name} '
                counter += 1

            conexion.close()

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return response

    def agregar_hijo_lista_padre(self, nombre, id_padre, cursor, conexion):
        ''' Añade a la lista de hijos del padre el nuevo directorio creado '''

        try:
            cursor.execute("select hijos from Directorios where id =?",(id_padre,))
            hijos = cursor.fetchall()

            if(hijos[0][0] == ""):
                cursor.execute("update Directorios set hijos=? where id=?",(nombre, id_padre))
                conexion.commit()
            else:
                directorios = hijos[0][0]
                directorios += " "
                directorios += nombre
                cursor.execute("update Directorios set hijos=? where id=?",(directorios, id_padre))
                conexion.commit()

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

    def eliminar_hijo_lista_padre(self, nombre, id_padre, cursor, conexion):
        ''' ELimina de la lista de hijos del padre el directorio borrado '''

        try:
            cursor.execute("select hijos from Directorios where id =?",(id_padre,))
            hijos = cursor.fetchall()
            directorios = hijos[0][0]
            directorios_list = directorios.split(' ')
            j = True

            for i in directorios_list:
                if(i == nombre and j):
                    directorio = nombre + " "
                elif(i == nombre and j == False):
                   directorio = " " + nombre
                j = False 

            '''if(directorios.find(nombre) == 0):
                directorio = nombre + " "
            else:
                directorio = " " + nombre'''
                
            rep = directorios.replace(directorio, "")
            cursor.execute("update Directorios set hijos=? where id=?",(rep, id_padre))
            conexion.commit()

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

    def comprobar_hijo_mismo_nombre(self, nombre_hijo, id_padre):
        ''' Comprueba si ya existe un hijo con el mismo nombre '''
        
        mismo_nombre = False

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select nombre from Directorios where padre =?",(id_padre,))
            directorios = cursor.fetchall()

            for i in directorios:
                if i[0] == nombre_hijo:
                    mismo_nombre = True
                    
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return mismo_nombre

    def comprobar_archivo_mismo_nombre(self, id, nombre, cursor):
        ''' COmprueba si ya existe un archivo con el mismo nombre en el directorio '''

        mismo_nombre = False

        try:
            cursor.execute("select archivos from Directorios where id=?",(id,))
            archivos = cursor.fetchall()
            files = archivos[0][0]
            files_list = files.split(' ')
            nombre_coma = nombre + ','

            for i in files_list:
                if(i.find(nombre_coma) == 0):
                    mismo_nombre = True

            if(files.find(nombre_coma) != -1):
                mismo_nombre = True

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return mismo_nombre

    def comprobar_existe_por_id(self, id):
        ''' Comprueba si un directorio existe o no '''

        no_existe = True

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select id from Directorios")
            directorios = cursor.fetchall()

            for i in directorios:
                if i[0] == id:
                    no_existe = False
                    
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        conexion.close()

        return no_existe

    def comprobar_exite_por_nombre_idPadre(self, nombre, id_padre, cursor):
        ''' Comprueba si un directorio existe o no '''

        no_existe = True

        try:
            cursor.execute("select nombre from Directorios where padre=?",(id_padre,))
            directorios = cursor.fetchall()

            for i in directorios:
                if i[0] == nombre:
                    no_existe = False
                    
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return no_existe

    def comprobar_escritura_id(self, id, user):
        ''' Comprobar si cierto usuario tiene permisos de escritura '''

        sin_permiso = True
        
        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select writable from Directorios where id=?",(id,))
            writable = cursor.fetchall()
            usuarios = writable[0][0]
            usuarios_list = usuarios.split(" ")

            for i in usuarios_list:
                if(i == user):
                    sin_permiso = False

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        conexion.close()
        
        return sin_permiso

    
    def comprobar_escritura_nombre_padre(self, nombre, padre, user, cursor):
        ''' Comprobar si cierto usuario tiene permisos de escritura '''
        
        sin_permiso = True
        
        try:
            cursor.execute("select writable from Directorios where nombre=? and padre=?",(nombre, padre))
            writable = cursor.fetchall()
            usuarios = writable[0][0]
            usuarios_list = usuarios.split(" ")

            for i in usuarios_list:
                if(i == user):
                    sin_permiso = False

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')
        
        return sin_permiso

    def comprobar_lectura_id(self, id, user):
        ''' Comprobar si cierto usuario tiene permisos de lectura '''

        sin_permiso = True
        
        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select readable from Directorios where id=?",(id,))
            readable = cursor.fetchall()
            usuarios = readable[0][0]
            usuarios_list = usuarios.split(" ")

            for i in usuarios_list:
                if(i == user):
                    sin_permiso = False

        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        conexion.close()
        
        return sin_permiso

    def obtener_directorio_padre(self, id_dir):
        ''' Obtener el padre de un directorio '''

        padre = ''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select padre from Directorios where id=?",(id_dir,))
            consulta = cursor.fetchall()
            padre += consulta[0][0]

            conexion.close()
            
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return padre

    def obtener_url_archivo(self, dir_id, filename):
        ''' Obtiene la url de un archivo '''

        url = ''

        try:
            conexion = sqlite3.connect("directorios.db")
            cursor = conexion.cursor()

            cursor.execute("select archivos from Directorios where id=?",(dir_id,))
            consulta = cursor.fetchall()
            archivos = consulta[0][0]
            archivos_lista = archivos.split(' ')

            for i in archivos_lista:
                archivo = i.split(',')

                if(archivo[0] == filename):
                    url += archivo[1]
                    break

            conexion.close()
            
        except sqlite3.OperationalError:
            print(f'Error al leer la base de datos')

        return url


 # Main para probar que todo funcione
def main():
    bd = ManagerBDS()
    #bd.insertar_directorio('dir4', 'c5da5fc2-5d28-11ed-9d03-dd969f8236ef', 'oscar')
    #bd.borrar_directorio('dir3', 'root', 'oscar')
    #bd.añadir_permiso_lectura('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','oscar','pablo')
    #bd.añadir_permiso_escritura('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','oscar','juan')
    #bd.quitar_permiso_lectura('root','admin','admin')
    #bd.quitar_permiso_escritura('b9f7f180-5c77-11ed-ac53-ffd4746543d1','pablo','pepe')
    #bd.añadir_fichero('c5da5fc2-5d28-11ed-9d03-dd969f8236ef','oscar','file1','/dir1/file1')
    #bd.borrar_fichero('c5da5fc2-5d28-11ed-9d03-dd969f8236ef', 'oscar', 'file1')
    #bd.listar_directorios('root')

if __name__ == '__main__':
    main()
