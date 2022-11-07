# dirApi
Implementacion de una Api Rest para gestion de directorios

Oscar Escabias González
Carlos Rodriguez Gómez-Carreño

Crear un entorno virtual y activarlo:

python3 -m venv .venv
source .venv/bin/activate

Instalar las dependencias:

pip install -r requeriments.txt

Se puede lanzar en un terminal el servidor:

python3 -m dirApiScripts.server

Las diferentes opciones son:

-a, --admin <token> Establece un token de administracion
-p, --port <puerto> Establece un puerto de escucha
-l, --listening <direccion> Establece una direccion de escucha
-d, --db <bbdd> Establece la ruta de la base de datos

Y en otro el cliente (que ejecuta código de prueba):

python3 -m dirApiScripts.client

