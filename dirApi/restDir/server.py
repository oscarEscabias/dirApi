#!/usr/bin/env python3

from flask import make_response, request
from clients.auth import AuthService
import json

def routeApp(app, BBDD):
    ''' Enruta la API REST a la webapp'''

    au = AuthService()

    @app.route('/v1/directory/<dir_id>', methods=['GET'])
    def list_directories(dir_id):
        '''Obtener los subdirectorios'''

        headers = request.headers["user-token"]
        user = au.user_of_token(headers)

        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_lectura_id(dir_id, user)):
            return make_response('', 401)

        lista_directorios = BBDD.listar_directorios(dir_id)
        padre = BBDD.obtener_directorio_padre(dir_id)
        req_response = {"dir_id": dir_id, "childs": lista_directorios, "parent": padre}

        return make_response(req_response, 200)

    @app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['PUT'])
    def create_new_directory(dir_id, nombre_hijo):
        ''' Se crea un nuevo directorio '''
        
        headers = request.headers["user-token"]
        user = au.user_of_token(headers)
        
        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_hijo_mismo_nombre(nombre_hijo, dir_id)):
            return make_response('', 409)

        if(BBDD.comprobar_escritura_id(dir_id, user)):
            return make_response('', 401)

        new_directory = BBDD.insertar_directorio(nombre_hijo, dir_id, user)
        req_response = {"dir_id": new_directory}

        return make_response(req_response, 200)


    @app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['DELETE'])
    def delete_directory(dir_id, nombre_hijo):
        ''' Se elimina un directorio '''
        
        headers = request.headers["user-token"]
        user = au.user_of_token(headers)
        
        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_hijo_mismo_nombre(nombre_hijo, dir_id) == False):
            return make_response('', 404)

        if(BBDD.comprobar_escritura_id(dir_id, user)):
            return make_response('', 401)

        BBDD.borrar_directorio(nombre_hijo, dir_id, user)

        return make_response('', 204)

    @app.route('/v1/files/<dir_id>', methods=['GET'])
    def get_files_names(dir_id):
        ''' Se devuelven los nombres de los archivos del directorio dado '''
        
        headers = request.headers["user-token"]
        user = au.user_of_token(headers)

        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_lectura_id(dir_id, user)):
            return make_response('', 401)

        lista_archivos = BBDD.listar_archivos(dir_id)
        req_response = {"dir_id": lista_archivos}

        return make_response(req_response, 200)

    @app.route('/v1/files/<dir_id>/<filename>', methods=['GET'])
    def get_url(dir_id, filename):
        ''' Se devuelve la url asociada a un archivo '''

        headers = request.headers["user-token"]
        user = au.user_of_token(headers)

        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_lectura_id(dir_id, user)):
            return make_response('', 401)

        url = BBDD.obtener_url_archivo(dir_id, filename) 
        req_response = {"URL": url}

        return make_response(req_response, 200)

    @app.route('/v1/files/<dir_id>/<filename>', methods=['PUT'])
    def create_file(dir_id, filename):
        ''' Se crea un archivo y se devuelve su url '''
        
        headers = request.headers["user-token"]
        user = au.user_of_token(headers)

        print(request.is_json)

        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404) 

        if(BBDD.comprobar_escritura_id(dir_id, user)):
            return make_response('', 401)
        
        if not request.is_json:
            print('Hola')
            return make_response('', 400)

        if 'URL' not in request.get_json():
            print('Adios')
            return make_response('', 400)

        direccion = request.get_json()['URL']
        BBDD.añadir_fichero(dir_id, user, filename, direccion)

        url = BBDD.obtener_url_archivo(dir_id, filename) 
        req_response = {"URL": url}

        return make_response(req_response, 200)

    @app.route('/v1/files/<dir_id>/<filename>', methods=['DELETE'])
    def delete_file(dir_id, filename):
        ''' Se elimina un archivo y su tupla asociada '''
        
        headers = request.headers["user-token"]
        user = au.user_of_token(headers)

        if(BBDD.comprobar_existe_por_id(dir_id)):
            return make_response('', 404)

        if(BBDD.comprobar_escritura_id(dir_id, user)):
            return make_response('', 401)

        BBDD.borrar_fichero(dir_id, user, filename)

        return make_response('', 204)