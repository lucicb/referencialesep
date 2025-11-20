# orden_produccion_det_dto.py

class OrdenProduccionDetDto:
    """
    DTO para el detalle de la orden de producción.
    """

    def __init__(self, id_producto, cantidad, costo_unitario, cod_orden_prod_det=None):
        self.cod_orden_prod_det = cod_orden_prod_det  # opcional, se asigna después de insertar en BD
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.costo_unitario = costo_unitario

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "cod_orden_prod_det": self.cod_orden_prod_det,
            "id_producto": self.id_producto,
            "cantidad": float(self.cantidad),
            "costo_unitario": float(self.costo_unitario)
        }
