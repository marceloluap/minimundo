class Pagamento():
    def __init__(self, valor, taxa = 1):
        self.valor = valor
        self.taxa = taxa


    # POLIMORFISMO PARA INSERIR NO BANCO DE DADOS "PONTO"(FLOAT) AO INVES DE "VIRGULA"
    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, val):
        self._valor = val.replace(",", ".") 
    

    



    def totalPagar(self):
        return float(self.valor) * float(self.taxa)


    