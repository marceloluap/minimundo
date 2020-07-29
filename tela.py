import PySimpleGUI as sg
from login import Login
from minprincpal import EmpresaVendas

class TelaPython:
    #Inicialização da tela PYSIMPLEGUI
    def __init__(self):
        sg.change_look_and_feel('Reddit')
        # CHAMANDO TELA DE LOGIN
        telaLogin = self.telaLogin()
        if telaLogin == True:
            # INSTANCIANDO CLASSE DO MODULO MINPRINCIAL.PY  
            self._venda = EmpresaVendas()# # ENCAPSULAMENTO UMA UNDERSCORE
            # INICIANDO TELA PRINCIPAL
            self.Iniciar()
        elif telaLogin == "Sair":
            sg.popup_ok('Você saiu do sistema, até a próxima!', title="Alerta!")
        else:
            sg.popup_ok('Erro no sistema, consulte o desenvolvedor ou tente novamente mais tarde!', title="Alerta!")

    #CRIANDO TELA DE LOGIN
    
    def telaLogin(self):
        # GERANDO LAYOUT
        layout4 =       [[sg.Text('', size=(12,1)), sg.Text('\n Insira o Login e Senha \n', size=(71,3), justification='center', background_color='#000000', text_color='#FFFFFF'), sg.Text('', size=(10,1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('', size=(12, 1)), sg.Text('Login: ', size=(10, 1), font=('Helvetica', 16)), sg.InputText('', size=(29, 1), font=('Helvetica', 20, 'bold'), key="login"), sg.Text('', size=(10, 1))],
                        [sg.Text('', size=(12, 1)), sg.Text('Senha: ', size=(10, 1), font=('Helvetica', 16)), sg.InputText('', size=(29, 1), font=('Helvetica', 20, 'bold'), key="senha"), sg.Text('', size=(10, 1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('', size=(12, 1)), sg.Button('Entrar', size=(20, 2), border_width=0, font=('Helvetica', 12), key='entrar', button_color=('WHITE', 'dark slate gray')), sg.Button('Sair', size=(20, 2), font=('Helvetica', 12), key='sair', button_color=('White', 'Red'), border_width=0)]]
        win4 = sg.Window('Tela de Login', layout4)
        
        # PADRAO PYSIMPLEGUI PARA CAPTURAR ENTRADA DE DADOS
        while True:
            ev3, vals3 = win4.Read()

            if ev3 == 'entrar':
                logar = Login()
                # EXCESSÃO, EXCEPTIONS
                try:
                    verificado = logar.verificaLogin(vals3['login'], int(vals3['senha']))
                    if verificado == 1:
                        sg.popup_ok('Login não existe!', title="Alerta!" )
                    elif verificado == 2:
                        sg.popup_ok('Senha incorreta!', title="Alerta!" )
                    else:
                        win4.close()
                        return True
                except:
                    win4.close()
                    return False

            if ev3 == sg.WIN_CLOSED or ev3 == 'sair':
                win4.Close()
                break
        return "Sair"
        
    # TELA PRINCIPAL APOS O LOGIN
    def Iniciar(self):
            self.produtos = self._venda.mostrarLista()
            self.totalSomado = '0,00'
            self.selecionado = []
            headings = ['COD.', 'NOME PROD.', 'VALOR UNI.', 'QUANTIDADE', 'VALOR TOTAL']
            self.dados = []
            table = [[sg.Table(values=self.dados, headings=headings, def_col_width=23, auto_size_columns=False, max_col_width=23, justification="right", alternating_row_color='#DFB2F4', header_font=('Helvetica', 11),
                               vertical_scroll_only=True, hide_vertical_scroll=False, size=(60, 15), enable_events=True, key='Table', visible=True)]]
            valorTotal = [
                         [sg.Text('', size=(1, 1))],
                         [sg.Text('', size=(30, 1)), sg.Text('TOTAL:', size=(18, 1), font=('Helvetica', 18)), sg.Text('  R$  '+self.totalSomado, size=(15, 1), font=('Helvetica', 35, 'bold'), background_color='#343434', text_color='#FFFFFF', key='Soma')]
                         ]
            layout = [
                [sg.Text('', size=(30,1)), sg.Text('\n ADICIONAR ITENS DA LISTA \n', size=(60,3), justification='center', background_color='#000000', text_color='#FFFFFF'), sg.Text('', size=(30,1))],
                [sg.Text('', size=(1, 0))],
                [sg.Text('Selecione o Item: ', size=(30, 0)), sg.Combo(self.produtos, size=(67, 0), key='Produtos'), sg.Text('', size=(12, 0)), sg.Text('Quantidade: ', size=(10, 0)), sg.InputText('1', size=(8, 0), key='Quantidade')],
                [sg.Text('', size=(1, 0))],
                [sg.Text('', size=(30, 0)), sg.Text('Valor Un.:', size=(8, 0)), sg.Text('R$ 0,00', size=(18, 0), font=('Helvetica', 15), justification='center', key='ValorUn'), sg.Text('Valor Total.:', size=(10, 0)), sg.Text('R$ 0,00', size=(18, 0), font=('Helvetica', 15), justification='center', key='ValorTotal')],
                [sg.Text('', size=(1, 0))],
                [sg.Text('', size=(12, 2)), sg.Button('Add Item', size=(20, 2), font=('Helvetica', 12), key='Add', button_color=('Black', 'SeaGreen2'), border_width=0), sg.Button('Cancelar Item', size=(20, 2), font=('Helvetica', 12), key='Cancelar', button_color=('White', 'Red'), border_width=0),  sg.Button('Finalizar Pedido', size=(20, 2), font=('Helvetica', 12), key='Finalizar', border_width=0), sg.Button('Sair', size=(20, 2), font=('Helvetica', 12), key='Sair', button_color=('White', 'FireBrick4'), border_width=0), sg.Text('', size=(12, 2))],
                [sg.Text('', size=(1, 0))],
            ] + table + valorTotal

            self.janela = sg.Window("PROGRAMA DE VENDA ONLINE",  size=(1080,680)).layout(layout)
            
            
            while True:
                self.event, self.values = self.janela.Read(timeout=100)

                

                if self.values['Quantidade'] == "":
                    self.values['Quantidade'] = 1

                elif self.values['Quantidade'].isdigit() == False:
                    sg.popup_ok('Digite uma quantidade válida!',title="Alerta!")
                    self.janela.FindElement("Quantidade").Update(1)
                    self.values['Quantidade'] = 1


                if self.event is None or self.event == "Sair":
                    self._venda.sairBanco()
                    break
                if self.values['Produtos'] != "":
                    valores = self._venda.mostrarValores(self.values['Produtos'])
                    self.janela.FindElement("ValorUn").Update('R$ '+self.dinheiroFormat(valores[2]))


                    if self.values['Quantidade'] == '1' or self.values['Quantidade'] == '':
                        self.janela.FindElement("ValorTotal").Update('R$ ' + self.dinheiroFormat(valores[2]))
                        self.selecionado = [valores[0], self.values['Produtos'], self.dinheiroFormat(valores[2]), 1, self.dinheiroFormat(valores[2])]
                    else:
                        self.janela.FindElement("ValorTotal").Update('R$ ' + self.dinheiroFormat(valores[2]* int(self.values['Quantidade'])))
                        self.selecionado = [valores[0], self.values['Produtos'], self.dinheiroFormat(valores[2]), int(self.values['Quantidade']), self.dinheiroFormat(valores[2]*int(self.values['Quantidade']))]

                if self.event == 'Add':

                    if len(self.selecionado) == 0:
                        sg.popup_ok('Você deve selecionar ao menos 1 produto!', title="Alerta!")
                    else:
                        self.dados.append(self.selecionado)
                        val = self._venda.totalCompra(self.dados)
                        self.totalSomado = self.dinheiroFormat(str(val))
                        self.janela.FindElement("Table").Update(self.dados)
                        self.janela.FindElement("Soma").Update('  R$  ' + self.totalSomado)

                if self.event == 'Cancelar':
                    if self.values['Table'] != []:
                        self.dados.pop(self.values['Table'][0])
                        self.janela.FindElement("Table").Update(self.dados)
                    else:
                        sg.popup_ok('Você deve selecionar ao menos 1 produto na tabela para excluir!', title="Alerta!", )

                if self.event == 'Finalizar':

                    if len(self.dados) != 0:
                        # 0 - Cancela Compra, 1 - Pagou em Dinheiro, 2 - Pagou em Cartão, 3 - Acrescentar Item
                        result = self.telaFormasDePagamento()
                        if result == 0:
                            self.reset()
                        elif result == 3:
                            pass
                        else:
                            # Colocar a atualização do pagamento
                            setPagamento = self.telaPagamento(self.dados, result)

                            if type(setPagamento) == float:
                                idPedido = self._venda.comprar(self.dados, result, setPagamento)
                                if idPedido != 0:
                                   endereco = self.telaEndereco(idPedido)
                                   if endereco != 0:
                                       tipoPagamento = result
                                       dadosVenda = [idPedido[0], setPagamento, tipoPagamento]
                                       venda = self._venda.registrarVenda(dadosVenda)
                                       if venda > 0:
                                            status = self.telaRegistroDeVenda(venda)
                                            if status == True:
                                                self.reset()
                                            else:
                                                self._venda.sairBanco()
                                                break

                                       else:
                                            sg.popup_ok('Deu algo errado ao finalizar o pedido, tente novamente ou entre em contato com o desenvolvedor!', title="Alerta!", )
                                            self.reset()
                                   else:
                                       self.reset()
                                else:
                                    sg.popup_ok('Deu algo errado ao finalizar o pedido, tente novamente ou entre em contato com o desenvolvedor!', title="Alerta!", )
                            else:
                                sg.popup_ok('Ocorreu um erro desconhecido, tente novamente ou entre em contato com o desenvolvedor!', title="Alerta!")

                    else:
                        sg.popup_ok('Você deve registrar ao menos 1 item para finalizar o pedido!', title="Alerta!")

    def telaEndereco(self, pedido):
        retorno = []
        layout2 = [[sg.Text('', size=(30,1)), sg.Text('\n ADICIONAR O ENDEREÇO DE ENTREGA! \n', size=(60,3), justification='center', background_color='#000000', text_color='#FFFFFF'), sg.Text('', size=(30,1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('CEP: ', size=(30,1)), sg.InputText('', size=(30,1), key='cep'), sg.Text('', size=(10,1)), sg.Text('NUM: ', size=(10,1)), sg.InputText('', size=(20, 1), key='num')],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('RUA: ', size=(30,1)), sg.InputText('', size=(30,1), key='rua'), sg.Text('', size=(10,1)), sg.Text('BAIRRO: ', size=(10,1)), sg.InputText('', size=(20, 1), key='bairro')],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('COMPLEMENTO: ', size=(30, 1)), sg.InputText('', size=(30, 1), key='complemento'), sg.Text('', size=(10, 1)), sg.Text('CIDADE: ', size=(10, 1)), sg.InputText('', size=(20, 1), key='cidade')],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('ESTADO: ', size=(30, 1)), sg.InputText('', size=(30, 1), key='estado'), sg.Text('', size=(10,1)), sg.Text(': ', size=(10, 1)), sg.Text('', size=(20, 1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('', size=(16, 1)), sg.Button('Salvar', size=(20, 2), border_width=0, font=('Helvetica', 12), key='Salvar', button_color=('WHITE', 'dark slate gray')), sg.Button('CANCELAR COMPRA', size=(20, 2), font=('Helvetica', 12), key='CancelarCompra', button_color=('White', 'Red'), border_width=0)],
                        [sg.Text('', size=(1, 1))]]
        win2 = sg.Window('Window 2', layout2)


        #  PADRAO PYSIMPLEGUI PARA CAPTURAR ENTRADA DE DADOS
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == 'CancelarCompra':
                win2.Close()
                break

            if ev2 == 'Salvar':
                dados = [vals2['cep'], vals2['rua'], vals2['num'], vals2['bairro'], vals2['complemento'], vals2['cidade'], pedido, vals2['estado']]
                dadosVerificado = self.verificaEndereco(dados)
                if dadosVerificado == True:
                    retorno = self._venda.enderecoEntrega(dados)
                    win2.Close()
                    break
  

        return retorno

    def telaFormasDePagamento(self):
        retorno = 0
        layout3 = [
                        [sg.Text('', size=(30,1)), sg.Text('\n FINALIZAR COMPRA! \n', size=(71,3), justification='center', background_color='#000000', text_color='#FFFFFF'), sg.Text('', size=(10,1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('', size=(30, 1)), sg.Text('Total á Pagar: ', size=(32, 1), font=('Helvetica', 16)), sg.Text('  R$  '+self.totalSomado, size=(20, 1), font=('Helvetica', 20, 'bold'), key="totalFinaliza"), sg.Text('', size=(10, 1))],
                        [sg.Text('', size=(1, 1))],
                        [sg.Text('', size=(16, 1)), sg.Button('PAGAR (Dinheiro)', size=(20, 2), border_width=0, font=('Helvetica', 12), key='PagarDinheiro', button_color=('WHITE', 'dark slate gray')), sg.Button('PAGAR (Cartão)', size=(20, 2), font=('Helvetica', 12), key='PagarCartao', button_color=('Black', 'SeaGreen2'), border_width=0), sg.Button('CANCELAR COMPRA', size=(20, 2), font=('Helvetica', 12), key='CancelarCompra', button_color=('White', 'Red'), border_width=0), sg.Button('ADICIONAR ITEM', size=(20, 2), font=('Helvetica', 12), key='AddItem', border_width=0)]]




        win3 = sg.Window('TOTAL Á PAGAR', layout3)




        while True:
            ev3, vals3 = win3.Read()

            if ev3 == 'PagarDinheiro':
                retorno = 1
                win3.Close()
                break
            if ev3 == 'PagarCartao':
                retorno = 2
                win3.Close()
                break
            if ev3 == sg.WIN_CLOSED or ev3 == 'AddItem':
                retorno = 3
                win3.Close()
                break
            if ev3 == 'CancelarCompra':
                retorno = 0
                win3.Close()
                break


        return retorno




    def telaPagamento(self, dados, pedido):
        soma =  self._venda.totalCompra(dados)
        if pedido == 1:
            self.tipoPagamento = "Dinheiro"
            total = self._venda.pagamento(pedido, soma)
        else:
            self.tipoPagamento = "Cartão(+0.02%)"
            total = self._venda.pagamento(pedido, soma)

        layout = [[sg.Text("", size=(10,1)), sg.Text('Pagamento em {}'.format(self.tipoPagamento), size=(30,1), justification='center', font=('Helvetica', 18), background_color='#7371FC', text_color='#FFFFFF'), sg.Text("", size=(10,1))],
                  [sg.Text("", size=(10, 2))],
                  [sg.Text('VALOR: ', font=('Helvetica', 14), size=(26, 1)), sg.Text('    R$ {}    '.format(self.dinheiroFormat(total)), font=('Helvetica', 25), background_color='#343434', text_color='#FFFFFF'), sg.Text("", size=(10,1))],
                  [sg.Text("", size=(10, 1))],
                  [sg.Button('Continuar', size=(20, 2), border_width=0, font=('Helvetica', 12), key='continuar', button_color=('WHITE', 'dark slate gray')), sg.Button('Cancelar', size=(20, 2), font=('Helvetica', 12), key='cancelar', button_color=('White', 'Red'), border_width=0)]]

        window = sg.Window('Total a Pagar!', layout)

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'cancelar':
            window.Close()
        if event == 'continuar':
            window.Close()
            return total


    def telaRegistroDeVenda(self, venda):

        total = self._venda.getTotalVenda(venda)
        headings = ['COD.', 'NOME PROD.', 'VALOR UNI.', 'QUANTIDADE', 'VALOR TOTAL']
        dadosLista = self.dados
        table = [[sg.Table(values=dadosLista, headings=headings, def_col_width=23, auto_size_columns=False,
                           max_col_width=23, justification="right", alternating_row_color='#DFB2F4',
                           header_font=('Helvetica', 11),
                           vertical_scroll_only=True, hide_vertical_scroll=False, size=(60, 20), enable_events=True,
                           key='Table', visible=True)]]

        layout = [[sg.Text("", size=(30,1)), sg.Text('Venda recebida em {}'.format(self.tipoPagamento), size=(40,1), justification='center', font=('Helvetica', 18), background_color='#7371FC', text_color='#FFFFFF'), sg.Text("", size=(10,1))],
                  [sg.Text("", size=(10, 2))],
                  ]+ table + [[sg.Text("", size=(10, 2))],
        [sg.Text('TOTAL: ', font=('Helvetica', 14), size=(26, 1)),
         sg.Text('    R$ {}    '.format(self.dinheiroFormat(total)), font=('Helvetica', 25), background_color='#343434',
                 text_color='#FFFFFF'), sg.Text("", size=(10, 1))],
        [sg.Text("", size=(10, 1))],
        [sg.Button('Nova Venda', size=(20, 2), border_width=0, font=('Helvetica', 12), key='venda',
                   button_color=('WHITE', 'green')),
         sg.Button('Sair do Programa', size=(20, 2), font=('Helvetica', 12), key='cancelar', button_color=('White', 'Red'),
                   border_width=0)],]

        window = sg.Window('Venda Finalizada com Sucesso!', layout)

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'cancelar':
            window.Close()
            return False
        if event == 'venda':
            window.Close()
            return True
    def verificaEndereco(self, dados):
        if dados[0].isdigit() == False:
            sg.popup_ok('Você deve colocar somente números no campo de CEP', title="Alerta!")
            return False
        else:
            return True

    def dinheiroFormat(self, valor):
        if type(valor) == float:
            a = '{:,.2f}'.format(valor)
        else:
            a = '{:,.2f}'.format(float(valor))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        return c.replace('v', '.')

    def reset(self):
        self.totalSomado = '0,00'
        self.selecionado = []
        self.dados = []
        self.janela.FindElement('Produtos').Update('')
        self.janela.FindElement('Quantidade').Update('1')
        self.janela.FindElement('ValorUn').Update('R$ 0,00')
        self.janela.FindElement('ValorTotal').Update('R$ 0,00')
        self.janela.FindElement('Table').Update('')
        self.janela.FindElement('Soma').Update('  R$  ' + self.totalSomado)
