import sqlite3
from datetime import date
 

class Banco():
    def __init__(self):
        # Linha obrigatória para conectar banco
        self.__conecta = sqlite3.connect('banco.db')
        self.__banco = self.__conecta.cursor()
        # fim
        # VERIFICA SE EXISTE ALGUMA TABELA
        produtos = self.is_table()

        if produtos == False:
            # CHAMANDO MÉTODO PARA CRIAR UMA TABELA BÁSICA
            result = self.createTable()
            #Após criar a tabela caso não exista, acrescenta os dados basicos como 1 usuario e produtos
            if result == True:
                # VERIFICA SE A TABELA PRODUTOS EXISTE
                getAll = self.getAll("produtos")
                if len(getAll) == 0:
                    # CRIANDO DADOS (PRODUTOS, PRECO ETC)
                    lista = [{"nome": "Banana", "preco": 2.50},
                                 {"nome": "Macarrão", "preco": 3.50},
                                 {"nome": "Fandangos", "preco": 1.90},
                                 {"nome": "Refrigerante", "preco": 8.0}]

                    # CHAMANDO FUNÇÃO CREATED PARA INSERT NA TABELA CLIENTE (usuario)
                    self.created('clientes', '(clientes_nome, clientes_cpf, clientes_senha, clientes_date)', '("{}", {}, {},"{}")'.format("Marcel", 45784236652, 1234, str(date.today())))

                    # CHAMANDO FUNÇÃO CREATED PARA INSERT NA TABELA PRODUTOS
                    for produtos in lista:
                        self.insert = self.created('produtos', '(produtos_nome, produtos_preco, produtos_date)', '("{}", {}, "{}")'.format(str(produtos["nome"]), produtos["preco"], str(date.today())))
                # fim nova linha


    #Verifica se a tabela existe!
    def is_table(self):
        query = "SELECT count(*) FROM sqlite_master WHERE type='table'"
        cursor = self.__banco.execute(query)
        result = cursor.fetchone()[0]

        if result != 0:
            return True
        else:
            return False


    ############## INSERTS


    def created(self, tabela, campo, valor):
        resposta = self.__banco.execute("INSERT INTO "+tabela+ campo+" VALUES "+valor)
        self.__conecta.commit()
        return resposta

    ###### PEGAR TODOS ITENS DA TABELA
    def getAll(self, tabela):
        resposta = self.__banco.execute("select * from "+tabela)
        retorno = resposta.fetchall()
        self.__conecta.commit()
        return retorno

    def delete(self, tabela, id, name):
        resposta = self.__banco.execute("delete from "+tabela+" where "+id+" == "+name)
        self.__conecta.commit()
        return resposta

    def findOne(self, tabela, id, name):
        resposta = self.__banco.execute("select * from {} where {} == '{}'".format(tabela, id, name))
        retorno = resposta.fetchone()
        self.__conecta.commit()
        return retorno

    def joinTable(self, selecao, tabela1, tabela2, id1, id2, cond1, cond2):
        # resposta = self.__banco.execute("SELECT {} FROM {} INNER JOIN {} ON {}.{} = {}.{} WHERE {}.{} = {}".format(selecao, tabela1, tabela2, tabela1, id1, tabela2, id2, tabela1, cond1, cond2))
        resposta = self.__banco.execute("SELECT {} FROM {} INNER JOIN {} ON {}.{} = {}.{} WHERE {}.{} = {}".format(selecao, tabela1, tabela2, tabela1, id1, tabela2, id2, tabela1, cond1, cond2))
        retorno = resposta.fetchall()
        self.__conecta.commit()
        return retorno

    def closeBD(self):
        self.__conecta.close()

    # METODO PARA CRIAR TABELA DO BANCO DE DADOS 
    def createTable(self):
        #EXCEPTION 
        try:
            self.__banco.execute('''CREATE TABLE produtos
                         (produtos_id integer primary key, produtos_nome text, produtos_preco float, produtos_date text)''')

            self.__banco.execute('''CREATE TABLE clientes
                         (clientes_id integer primary key, clientes_nome text, clientes_cpf int, clientes_senha int, clientes_date text)''')

            self.__banco.execute('''CREATE TABLE enderecos
                         (enderecos_id integer primary key, enderecos_cep int, enderecos_rua text, enderecos_numero int, enderecos_bairro text, enderecos_complemento text, enderecos_cidade text, enderecos_id_pedidos int, enderecos_estado, enderecos_data text,
                         FOREIGN KEY(enderecos_id_pedidos) REFERENCES pedidos(pedidos_id))''')

            self.__banco.execute('''CREATE TABLE pedidos
                         (pedidos_id integer primary key, pedidos_id_clientes int, pedidos_data text, pedidos_status int, pedidos_tipo_pagamento int, pedidos_total float,
                         FOREIGN KEY(pedidos_id_clientes) REFERENCES clientes(clientes_id))''')

            self.__banco.execute('''CREATE TABLE itemPedidos
                         (itemPedidos_id integer primary key, itemPedidos_id_pedidos int, itemPedidos_id_produtos int, itemPedidos_quantidade int, pedidos_data text,
                         FOREIGN KEY(itemPedidos_id_pedidos) REFERENCES pedidos(pedidos_id)
                         FOREIGN KEY(itemPedidos_id_produtos) REFERENCES produtos(produtos_id))''')

            self.__banco.execute('''CREATE TABLE vendas
                         (vendas_id integer primary key, vendas_id_pedidos int, vendas_total real, vendas_recebido real, vendas_troco real, vendas_tipo_pagamento text, vendas_data text,
                         FOREIGN KEY(vendas_id_pedidos) REFERENCES pedidos(pedidos_id))''')

            self.__conecta.commit()
        except:
            return False
        return True