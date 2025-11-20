class PedidoMpDetDto:
    """
    DTO para el detalle del Pedido de Materia Prima.
    """

    def __init__(self, id_materia_prima, cantidad, costo_unitario, cod_detalle=None):
        self.cod_detalle = cod_detalle  # se asigna después de insertar en BD
        self.id_materia_prima = id_materia_prima
        self.cantidad = cantidad
        self.costo_unitario = costo_unitario

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "cod_detalle": self.cod_detalle,
            "id_materia_prima": self.id_materia_prima,
            "cantidad": float(self.cantidad),
            "costo_unitario": float(self.costo_unitario)
        }
