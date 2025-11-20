# orden_produccion_cab_dto.py

class OrdenProduccionCabDto:
    """
    DTO para la cabecera de Orden de Producción.
    Contiene los datos principales de la orden y su detalle.
    """

    def __init__(self, fecha_inicio, fecha_fin_estimada, id_producto, id_suc, usu_id, detalle, cod_orden_prod_cab=None):
        self.cod_orden_prod_cab = cod_orden_prod_cab  # opcional, se asigna después de insertar en BD
        self.fecha_inicio = fecha_inicio
        self.fecha_fin_estimada = fecha_fin_estimada
        self.id_producto = id_producto
        self.id_suc = id_suc
        self.usu_id = usu_id
        self.detalle = detalle

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "cod_orden_prod_cab": self.cod_orden_prod_cab,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin_estimada": self.fecha_fin_estimada.isoformat() if self.fecha_fin_estimada else None,
            "id_producto": self.id_producto,
            "id_suc": self.id_suc,
            "usu_id": self.usu_id,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
