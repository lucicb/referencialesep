class PedidosClientesDetDto:
    """
    DTO para el detalle del Pedido de Cliente.
    """

    def __init__(
        self,
        id_producto,
        cantidad,
        precio_unitario,
        observaciones=None,
        id_pedido_det=None
    ):
        self.id_pedido_det = id_pedido_det  # Se setea luego del INSERT
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.observaciones = observaciones

    def to_dict(self):
        """
        Convierte el DTO a diccionario (útil para APIs).
        No se incluye subtotal porque la BD lo calcula.
        """
        return {
            "id_pedido_det": self.id_pedido_det,
            "id_producto": self.id_producto,
            "cantidad": float(self.cantidad),
            "precio_unitario": float(self.precio_unitario),
            "observaciones": self.observaciones
        }
