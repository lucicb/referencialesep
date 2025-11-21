class ControlCalidadDetDto:
    """
    DTO para el detalle del Control de Calidad.
    """

    def __init__(
        self,
        valor_esperado,
        valor_obtenido,
        resultado,
        observaciones,
        id_cali_det=None
    ):
        # ID que se genera en BD (opcional)
        self.id_cali_det = id_cali_det

        # Campos de la tabla control_calidad_det
        self.valor_esperado = valor_esperado
        self.valor_obtenido = valor_obtenido
        self.resultado = resultado
        self.observaciones = observaciones

    def to_dict(self):
        """
        Retorna la representación como diccionario.
        """
        return {
            "id_cali_det": self.id_cali_det,
            "valor_esperado": self.valor_esperado,
            "valor_obtenido": self.valor_obtenido,
            "resultado": self.resultado,
            "observaciones": self.observaciones
        }
