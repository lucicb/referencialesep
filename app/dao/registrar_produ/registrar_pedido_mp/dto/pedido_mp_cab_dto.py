class PedidoMpCabDto:
    """
    DTO para la cabecera del Pedido de Materia Prima.
    Contiene los datos principales del pedido y su detalle.
    """

    def __init__(
        self,
        usu_id,
        id_suc,
        fecha_pedido,              # NUEVO
        fecha_entrega_estimada,     # NUEVO
        observaciones,
        prioridad,
        detalle,
        cod_pedido_mp=None
    ):
        self.cod_pedido_mp = cod_pedido_mp  # se asigna después si viene desde la BD
        self.usu_id = usu_id
        self.id_suc = id_suc
        self.fecha_pedido = fecha_pedido
        self.fecha_entrega_estimada = fecha_entrega_estimada
        self.observaciones = observaciones
        self.prioridad = prioridad
        self.detalle = detalle  # lista de PedidoMpDetDto

    def to_dict(self):
        """
        Devuelve una representación tipo diccionario.
        Ideal para enviarlo como JSON.
        """
        return {
            "cod_pedido_mp": self.cod_pedido_mp,
            "usu_id": self.usu_id,
            "id_suc": self.id_suc,
            "fecha_pedido": self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            "fecha_entrega_estimada": self.fecha_entrega_estimada.isoformat() if self.fecha_entrega_estimada else None,
            "observaciones": self.observaciones,
            "prioridad": self.prioridad,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
