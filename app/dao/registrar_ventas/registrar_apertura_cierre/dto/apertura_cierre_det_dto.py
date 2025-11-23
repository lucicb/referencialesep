class AperturaCierreDetDto:
    """
    DTO para los movimientos de caja (detalle).
    Representa ingresos o egresos realizados durante la apertura/cierre de caja.
    """

    def __init__(
        self,
        tipo,               # ingreso / egreso
        concepto,
        monto,
        fecha_mov=None,
        usu_id=None,
        id_caja_mov=None,   # asignado por la BD
        id_caja_cab=None    # relación con la cabecera
    ):
        self.id_caja_mov = id_caja_mov
        self.id_caja_cab = id_caja_cab

        self.tipo = tipo
        self.concepto = concepto
        self.monto = monto
        self.fecha_mov = fecha_mov
        self.usu_id = usu_id

    def to_dict(self):
        """
        Devuelve una representación tipo diccionario.
        Ideal para enviarlo como JSON.
        """
        return {
            "id_caja_mov": self.id_caja_mov,
            "id_caja_cab": self.id_caja_cab,

            "tipo": self.tipo,
            "concepto": self.concepto,
            "monto": float(self.monto) if self.monto is not None else None,

            "fecha_mov": self.fecha_mov.isoformat() if self.fecha_mov else None,
            "usu_id": self.usu_id
        }
