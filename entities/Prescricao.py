class Prescricao:
    def __init__(self, consulta, nome_composto_medicamento, observacao='') -> None:
        self.consulta = consulta
        self.nome_composto_medicamento = nome_composto_medicamento
        self.observacao = observacao