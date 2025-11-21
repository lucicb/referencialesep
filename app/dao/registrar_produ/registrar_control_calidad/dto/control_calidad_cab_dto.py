class ControlCalidadCabDto:
    """
    DTO para la cabecera de Control de Calidad.
    Contiene los datos principales del control y su lista de detalles.
    """

    def __init__(
        self,
        cod_orden_prod_cab,
        fecha_control,
        responsable,
        resultado,
        observaciones,
        estado,
        usu_id,
        detalle,
        id_cali_cab=None
    ):
        # ID que genera la BD (opcional)
        self.id_cali_cab = id_cali_cab

        # Campos de la tabla control_calidad_cab
        self.cod_orden_prod_cab = cod_orden_prod_cab
        self.fecha_control = fecha_control
        self.responsable = responsable
        self.resultado = resultado
        self.observaciones = observaciones
        self.estado = estado
        self.usu_id = usu_id

        # Lista de objetos ControlCalidadDetDto
        self.detalle = detalle

    def to_dict(self):
        """
        Convierte el DTO a diccionario (útil para jsonify o debug).
        """
        return {
            "id_cali_cab": self.id_cali_cab,
            "cod_orden_prod_cab": self.cod_orden_prod_cab,
            "fecha_control": self.fecha_control.isoformat() if self.fecha_control else None,
            "responsable": self.responsable,
            "resultado": self.resultado,
            "observaciones": self.observaciones,
            "estado": self.estado,
            "usu_id": self.usu_id,
            "detalle": [d.to_dict() for d in self.detalle] if self.detalle else []
        }
