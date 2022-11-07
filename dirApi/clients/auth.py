'''
    Interfaces para el acceso a la API rest del servicio de autenticacion
'''


class Administrator:
    '''Cliente de autenticacion como administrador'''

    @property
    def token(self):
        '''Retorna el token del administrador'''
        raise NotImplementedError()

    def new_user(self, username, password):
        '''Crea un nuevo usuario'''
        raise NotImplementedError()

    def remove_user(self, username):
        '''Elimina un usuario'''
        raise NotImplementedError()


class User:
    '''Cliente de autenticacion como usuario'''

    def set_new_password(self, new_password):
        '''Cambia la contraseña del usuario'''
        raise NotImplementedError()

    @property
    def token(self):
        '''Retorna el token del usuario'''
        raise NotImplementedError()


class AuthService:
    '''Cliente de acceso al servicio de autenticacion'''

    def user_of_token(self, token):
        '''Return username of the given token or error'''
        if token == 'mi_token_de_prueba':
            return "oscar"
        else:
            return "fdksfjdks"
        #raise NotImplementedError()

    def exists_user(self, username):
        '''Return if given user exists or not'''
        raise NotImplementedError()

    def administrator_login(self, token):
        '''Return Adminitrator() object or error'''
        raise NotImplementedError()

    def user_login(self, username, password):
        '''Return User() object or error'''
        raise NotImplementedError()
