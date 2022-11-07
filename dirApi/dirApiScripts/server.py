#!/usr/bin/env python3

from flask import Flask
import argparse
import uuid
import pathlib
from restDir.server import routeApp
from restDir.managerbd import ManagerBDS

parser = argparse.ArgumentParser(description='Lanzar el servidor')
parser.add_argument('-a', '--admin', type= str, metavar='', help='Establece un token de administracion')
parser.add_argument('-p', '--port', type= int, metavar='', help='Establece un puerto de escucha')
parser.add_argument('-l', '--listening', type= str, metavar='', help='Establece una direccion de escucha')
parser.add_argument('-d', '--db', type= str, metavar='', help='EStablece la ruta de la base de datos')
args = parser.parse_args()

def main():
    '''Entry point'''

    admin_token = args.admin
    if(admin_token == None):
        admin_token = uuid.uuid1()

    puerto = args.port
    if(puerto == None):
        puerto = 3002

    direccion = args.listening
    if(direccion == None):
        direccion = '0.0.0.0'

    bbdd = args.db
    if(bbdd == None):
        bbdd = pathlib.Path(__file__).parent.absolute()

    app = Flask("restdir")
    routeApp(app, ManagerBDS())
    app.run(debug=True, host=direccion, port=puerto)


if __name__ == '__main__':
    main()