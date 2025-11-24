class AperturaCierreCabDto:
    """
    DTO para la cabecera de Apertura y Cierre de Caja.
    Contiene los datos principales de la apertura/cierre.
    """

    def __init__(
        self,
        id_suc,
        usu_id,
        fecha_apertura=None,
        monto_inicial=None,
        fecha_cierre=None,
        monto_final=None,
        monto_teorico=None,
        diferencia=None,
        estado=None,
        observaciones=None,
        id_caja_cab=None,
        detalle=None
    ):
        self.id_caja_cab = id_caja_cab
        self.id_suc = id_suc
        self.usu_id = usu_id

        self.fecha_apertura = fecha_apertura
        self.monto_inicial = monto_inicial

        self.fecha_cierre = fecha_cierre
        self.monto_final = monto_final
        self.monto_teorico = monto_teorico
        self.diferencia = diferencia

        self.estado = estado
        self.observaciones = observaciones

        self.detalle = detalle if detalle else []

    def to_dict(self):
        """
        Devuelve una representación tipo diccionario.
        Ideal para enviarlo como JSON.
        """
        return {
            "id_caja_cab": self.id_caja_cab,
            "id_suc": self.id_suc,
            "usu_id": self.usu_id,

            "fecha_apertura": self.fecha_apertura.strftime("%Y-%m-%d %H:%M") if self.fecha_apertura else None,
            "monto_inicial": float(self.monto_inicial) if self.monto_inicial is not None else None,

            "fecha_cierre": self.fecha_cierre.strftime("%Y-%m-%d %H:%M") if self.fecha_cierre else None,
            "monto_final": float(self.monto_final) if self.monto_final is not None else None,
            "monto_teorico": float(self.monto_teorico) if self.monto_teorico is not None else None,
            "diferencia": float(self.diferencia) if self.diferencia is not None else None,

            "estado": self.estado,
            "observaciones": self.observaciones,

            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }