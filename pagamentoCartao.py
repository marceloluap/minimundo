from pagamento import Pagamento
class PagamentoCartao(Pagamento):# HERANÇA 

    def totalPagar(self): # POLIFORMFISMO, ALTERANDO REGRA DE NEGÓCIO
        # CHAMANDO O MESMO MÉTODO HERDADO MAS ALTERANDO 
        return (float(self.valor) * float(self.taxa)) + float(self.valor)
    

    
