class EtapaProduCabDto:
    """
    DTO para la cabecera de Etapa de Producción.
    Contiene los datos principales de la cabecera y su detalle (etapas).
    """

    def __init__(
        self,
        cod_orden_prod_cab,
        fecha,
        id_producto,
        cantidad_planificada,
        estado,
        observaciones,
        fecha_inicio,
        fecha_fin,
        usu_id,
        id_suc,
        detalle,
        id_etapa_cab=None
    ):
        self.id_etapa_cab = id_etapa_cab  # opcional, se completa al insertar en BD
        self.cod_orden_prod_cab = cod_orden_prod_cab
        self.fecha = fecha
        self.id_producto = id_producto
        self.cantidad_planificada = cantidad_planificada
        self.estado = estado
        self.observaciones = observaciones
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.usu_id = usu_id
        self.id_suc = id_suc
        self.detalle = detalle  # lista de objetos EtapaProduDetDto

    def to_dict(self):
        """
        Retorna un diccionario serializable (json).
        """
        return {
            "id_etapa_cab": self.id_etapa_cab,
            "cod_orden_prod_cab": self.cod_orden_prod_cab,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "id_producto": self.id_producto,
            "cantidad_planificada": float(self.cantidad_planificada)
                if self.cantidad_planificada is not None else None,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "usu_id": self.usu_id,
            "id_suc": self.id_suc,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
