from banco import Banco

class Login():
    def __init__(self):
        self.bd = Banco()

    # VERIFICANDO LOGIN E SENHA CADASTRADA    login: Marcel Senha: 1234
    def verificaLogin(self, user, password):
        setUser = self.bd.findOne("clientes", "clientes_nome", user)

        if setUser == None:
            return 1
        elif setUser[3] != password:
           return 2
        else:
           return 3


