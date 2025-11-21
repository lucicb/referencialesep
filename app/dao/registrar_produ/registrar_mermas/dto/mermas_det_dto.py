# mermas_det_dto.py

class MermasDetDto:
    """
    DTO para el detalle de Mermas.
    """

    def __init__(self, id_producto, cantidad, motivo, costo_unitario, id_merma_det=None):
        self.id_merma_det = id_merma_det  # opcional, se asigna después de insertar en BD
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.motivo = motivo
        self.costo_unitario = costo_unitario

    def to_dict(self):
        """
        Retorna la representación como diccionario, útil para jsonify.
        """
        return {
            "id_merma_det": self.id_merma_det,
            "id_producto": self.id_producto,
            "cantidad": float(self.cantidad),
            "motivo": self.motivo,
            "costo_unitario": float(self.costo_unitario),
            "costo_total": float(self.cantidad) * float(self.costo_unitario)  # calculado
        }
