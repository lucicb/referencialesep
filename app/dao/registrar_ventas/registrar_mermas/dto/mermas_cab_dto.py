# mermas_cab_dto.py

class MermasCabDto:
    """
    DTO para la cabecera de Mermas.
    Contiene los datos principales de la merma y su detalle.
    """

    def __init__(self, cod_orden_prod_cab, fecha_registro, responsable, motivo_general, observaciones,
                 usu_id, suc_id, detalle, id_merma_cab=None):
        self.id_merma_cab = id_merma_cab  # opcional, se asigna después de insertar en BD
        self.cod_orden_prod_cab = cod_orden_prod_cab
        self.fecha_registro = fecha_registro
        self.responsable = responsable
        self.motivo_general = motivo_general
        self.observaciones = observaciones
        self.usu_id = usu_id
        self.suc_id = suc_id
        self.detalle = detalle  # lista de MermasDetDto

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "id_merma_cab": self.id_merma_cab,
            "cod_orden_prod_cab": self.cod_orden_prod_cab,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
            "responsable": self.responsable,
            "motivo_general": self.motivo_general,
            "observaciones": self.observaciones,
            "usu_id": self.usu_id,
            "suc_id": self.suc_id,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
