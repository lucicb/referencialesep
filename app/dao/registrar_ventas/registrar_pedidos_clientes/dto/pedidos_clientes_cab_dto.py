class PedidosClientesCabDto:
    """
    DTO para la cabecera del Pedido de Cliente.
    Contiene todos los datos del pedido y su detalle.
    """

    def __init__(
        self,
        id_cliente,
        fecha_pedido,
        fecha_entrega,
        estado,
        total,
        observaciones,
        usu_id,
        id_suc,
        detalle,
        id_pedido_cab=None
    ):
        self.id_pedido_cab = id_pedido_cab  # Se completa luego del INSERT
        self.id_cliente = id_cliente
        self.fecha_pedido = fecha_pedido
        self.fecha_entrega = fecha_entrega
        self.estado = estado
        self.total = total
        self.observaciones = observaciones
        self.usu_id = usu_id
        self.id_suc = id_suc
        self.detalle = detalle  # Lista de detalles

    def to_dict(self):
        """
        Convierte el DTO a diccionario (útil para APIs y debugging).
        """
        return {
            "id_pedido_cab": self.id_pedido_cab,
            "id_cliente": self.id_cliente,
            "fecha_pedido": self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            "fecha_entrega": self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            "estado": self.estado,
            "total": float(self.total) if self.total is not None else 0,
            "observaciones": self.observaciones,
            "usu_id": self.usu_id,
            "id_suc": self.id_suc,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
