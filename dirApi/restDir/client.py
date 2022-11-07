import json

import requests


HEADERS = {"content-type": "application/json"}

'''
    Interfaces para el acceso al servicio de directorio
'''

class ServerError(Exception):
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'Server Error: {self.msg}'

class DirectoryService:
    '''Cliente de acceso al servicio de directorio'''

    def get_root(self, user):
        '''Obtiene el directorio raiz'''
        


class Directory:
    '''Cliente de acceso a un directorio'''

    def __init__(self, uri, timeout = 120):
        ''' uri should be the root of the API,
            example: https://127.0.0.1:5000/
        '''

        self.root = uri

        if not self.root.endswith('/'):
            self.root = f'{self.root}/'

        self.timeout = timeout
        self.header = {"user-token": "mi_token_de_prueba"}

    def list_directories(self, dir):
        ''' Obtiene una lista de todos los subdirectorios del directorio indicado '''

        if not isinstance(dir, str):
            raise ValueError("Error en el formato del directorio")

        result = requests.get(
            f'{self.root}/v1/directory/{dir}',
            timeout=self.timeout,
            headers=self.header
        )

        if result.status_code == 404:
            raise IndexError("No existe el directorio")

        if result.status_code == 401:
            raise ServerError(f'El usuario no tiene permisos para realizar esta operacion: {result.status_code}')

        if result.status_code != 200:
            raise ServerError(f'Error inexperado: {result.status_code}')

        return result.content.decode('utf-8')


    def new_directory(self, id_directory, nombre):
        ''' Crea un nuevo subdirectorio en el directorio '''

        if not isinstance(id_directory, str):
            raise ValueError("El id del padre debe ser un string")

        if not isinstance(nombre, str):
            raise ValueError("El nombre del directorio debe ser un string")

        result = requests.put(
            f'{self.root}/v1/directory/{id_directory}/{nombre}',
            timeout=self.timeout,
            headers=self.header
        )

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code == 409:
            raise ServerError(f'Ya existe un directorio hijo con ese nombre: {result.status_code}')

        if result.status_code == 401:
            raise ServerError(f'El usuario no tiene permisos para realizar esta operacion: {result.status_code}')

        if result.status_code != 200:
            raise ServerError(f'Unexpected status code: {result.status_code}')

        return result.content.decode('utf-8')

    def remove_directory(self, id_directory, nombre):
        ''' Elimina un subdirectorio del directorio '''

        if not isinstance(id_directory, str):
            raise ValueError("El id del padre debe ser un string")

        if not isinstance(nombre, str):
            raise ValueError("El nombre del directorio debe ser un string")

        result = requests.delete(
            f'{self.root}/v1/directory/{id_directory}/{nombre}',
            timeout=self.timeout,
            headers=self.header
        )

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code == 401:
            raise ServerError(f'El usuario no tiene permisos para realizar esta operacion: {result.status_code}')

        if result.status_code != 204:
            raise ServerError(f'Unexpected status code: {result.status_code}')

        return result.content.decode('utf-8')

    def list_files(self, dir):
        ''' Obtiene una lista de todos los archivos del directorio indicado '''

        if not isinstance(dir, str):
            raise ValueError("Error en el formato del directorio")

        result = requests.get(
            f'{self.root}/v1/files/{dir}',
            timeout=self.timeout,
            headers=self.header
        )
        
        if result.status_code == 401:
            raise ServerError(f'EL usuario no tiene permisos para realizar esta operacion: {result.status_code}')

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code != 200:
            raise ServerError(f'Error inexperado: {result.status_code}')

        return result.content.decode('utf-8')

    def get_file(self, dir, filename):
        ''' Obtiene la url de un archivo '''

        if not isinstance(dir, str):
            raise ValueError("El id debe ser un string")

        if not isinstance(filename, str):
            raise ValueError("El nombre del directorio debe ser un string")

        result = requests.get(
            f'{self.root}/v1/files/{dir}/{filename}',
            timeout=self.timeout,
            headers=self.header
        )

        if result.status_code == 401:
            raise ServerError(f'EL usuario no tiene permisos para realizar esta operacion: {result.status_code}')

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code != 200:
            raise ServerError(f'Error inexperado: {result.status_code}')

        return result.content.decode('utf-8')

    def new_file(self, dir, filename, file_url):
        '''Crea un nuevo fichero a partir de la url de un blob'''

        if not isinstance(dir, str):
            raise ValueError("El id debe ser un string")

        if not isinstance(filename, str):
            raise ValueError("El nombre del directorio debe ser un string")

        if not isinstance(file_url, str):
            raise ValueError("La url debe ser un string")

        req_body = {"URL": file_url}

        cabeceras = self.header
        cabeceras['content-type'] = 'application/json'
        
        result = requests.put(
            f'{self.root}/v1/files/{dir}/{filename}',
            headers=cabeceras,
            data=json.dumps(req_body),
            timeout=self.timeout
        )

        if result.status_code == 401:
            raise ServerError(f'No tienes permiso para realizar esta operacion: {result.status_code}')

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code == 400:
            raise ServerError(f'Falta informacion en la peticion: {result.status_code}')

        if result.status_code != 200:
            raise ServerError(f'Error inexperado: {result.status_code}')

        return result.content.decode('utf-8')

    def remove_file(self, dir, filename):
        '''Elimina un fichero del directorio'''

        if not isinstance(dir, str):
            raise ValueError("El id debe ser un string")

        if not isinstance(filename, str):
            raise ValueError("El nombre del directorio debe ser un string")

        result = requests.delete(
            f'{self.root}/v1/files/{dir}/{filename}',
            timeout=self.timeout,
            headers=self.header
        )

        if result.status_code == 401:
            raise ServerError(f'No tienes permiso para realizar esta operacion: {result.status_code}')

        if result.status_code == 404:
            raise ServerError(f'No existe el directorio: {result.status_code}')

        if result.status_code != 204:
            raise ServerError(f'Error inexperado: {result.status_code}')

        return result.content.decode('utf-8')

    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        raise NotImplementedError()

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        raise NotImplementedError()

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        raise NotImplementedError()

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        raise NotImplementedError()
