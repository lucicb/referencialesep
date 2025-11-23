class EtapaProduDetDto:
    """
    DTO para el detalle de la Etapa de Producción.
    """

    def __init__(
        self,
        etapa,
        descripcion,
        responsable,
        fecha_inicio,
        fecha_fin,
        estado,
        avance,
        id_etapa_cab=None,
        id_etapa_det=None
    ):
        self.id_etapa_det = id_etapa_det  # opcional, se asigna después de insertar en BD
        self.id_etapa_cab = id_etapa_cab  # FK a la cabecera
        self.etapa = etapa
        self.descripcion = descripcion
        self.responsable = responsable
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.avance = avance

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "id_etapa_det": self.id_etapa_det,
            "id_etapa_cab": self.id_etapa_cab,
            "etapa": self.etapa,
            "descripcion": self.descripcion,
            "responsable": self.responsable,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "estado": self.estado,
            "avance": self.avance
        }
