from banco import Banco
from datetime import date
from pagamento import Pagamento
from pagamentoCartao import PagamentoCartao
class EmpresaVendas():

    def __init__(self):
        # nova linha
         self.__bd = Banco()


    def comprar(self, item, forma, totalCompra):
        # CHAMANDO FUNÇÃO CREAT PARA INSERT NA TABELA PEDIDO
        pedido = self.__bd.created('pedidos', '(pedidos_id_clientes, pedidos_data, pedidos_status, pedidos_tipo_pagamento, pedidos_total)', '({}, "{}", {}, {}, {})'.format(1, str(date.today()), 0, forma, totalCompra))
        idPedido = pedido.lastrowid
        if pedido.lastrowid > 0:
            itemPedido = 0
            for i in item:
                # CHAMANDO FUNÇÃO CREATED PARA INSERT NA TABELA ITEMPEDIDO
                itemPedido = self.__bd.created('itemPedidos', '(itemPedidos_id_pedidos, itemPedidos_id_produtos, itemPedidos_quantidade, pedidos_data)', '({}, {}, {}, "{}")'.format(idPedido, i[0], i[3], str(date.today())))
            if itemPedido.lastrowid > 0:
                return [idPedido]
            else:
                return 0
        else:
            return 0



    def mostrarLista(self):
        listarProdutos = self.__bd.getAll("produtos")
        lista = []
        for prod in listarProdutos:
            lista.append(prod[1])
        return lista


    def mostrarValores(self, nome):
        return self.__bd.findOne("produtos", "produtos_nome", nome)

    def totalCompra(self, lista):
        total = 0
        for valor in lista:
            val = valor[4].replace(",", ".")
            total += float(val)
        totalValor = str(total)
        return totalValor


    def registrarVenda(self, lista):
        # CHAMANDO FUNÇÃO CREAT PARA INSERT NA TABELA VENDAS
        venda = self.__bd.created("vendas", "(vendas_id_pedidos, vendas_total, vendas_recebido, vendas_troco, vendas_tipo_pagamento, vendas_data)", '({}, {}, {}, {}, {}, {})'.format(lista[0], lista[1], 0, 0, lista[2], str(date.today())))
        return venda.lastrowid

    def getTotalVenda(self, id):
        total = self.__bd.findOne("vendas", "vendas_id", id)
        return total[2]

    # CHAMANDO CREATED PARA INSERIR = INSERT

    def enderecoEntrega(self, dados):
        endereco = self.__bd.created('enderecos', '(enderecos_cep, enderecos_rua, enderecos_numero, enderecos_bairro, enderecos_complemento, enderecos_cidade, enderecos_id_pedidos, enderecos_estado, enderecos_data)', '({}, "{}", {}, "{}", "{}", "{}", {}, "{}", "{}")'.format(int(dados[0]), dados[1], int(dados[2]), dados[3], dados[4], dados[5], dados[6][0], dados[7], str(date.today())))
        return endereco.lastrowid


    def getPedido(self, id):
        pedido = self.__bd.joinTable("itemPedidos_quantidade, produtos_preco", "itemPedidos", "produtos", "itemPedidos_id_produtos", "produtos_id", "itemPedidos_id_pedidos", id)
        return pedido


    def sairBanco(self):
        self.__bd.closeBD()

    def pagamento(self, tipo, soma):
        if tipo == 1:
            total = Pagamento(soma)
            return total.totalPagar()
        else:
            total = PagamentoCartao(soma, 0.02)
            return total.totalPagar()




