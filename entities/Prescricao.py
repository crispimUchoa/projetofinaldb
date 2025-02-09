class Prescricao:
    def __init__(self, id_consulta, nome_composto_medicamento, observacao='') -> None:
        self.id_consulta = id_consulta
        self.nome_composto_medicamento = nome_composto_medicamento
        self.observacao = observacao