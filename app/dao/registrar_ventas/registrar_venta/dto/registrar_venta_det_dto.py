# app/dao/registrar_ventas/registrar_venta/dto/registrar_venta_det_dto.py

class VentaDetDto:
    def __init__(
        self,
        id_venta_det=None,
        id_venta_cab=None,
        id_producto=None,
        cantidad=0.0,
        precio_unitario=0.0,
        descuento=0.0,
        observaciones='',
        **kwargs  # Esto ignora cualquier parámetro adicional como total_item, subtotal, etc.
    ):
        self.id_venta_det = id_venta_det        # ID de detalle, autogenerado
        self.id_venta_cab = id_venta_cab        # FK a cabecera de venta
        self.id_producto = id_producto          # Código o ID del producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.descuento = descuento
        self.subtotal = self.cantidad * self.precio_unitario
        self.total_item = self.subtotal - self.descuento
        self.observaciones = observaciones

    def to_dict(self):
        return {
            "id_venta_det": self.id_venta_det,
            "id_venta_cab": self.id_venta_cab,
            "id_producto": self.id_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal,
            "descuento": self.descuento,
            "total_item": self.total_item,
            "observaciones": self.observaciones
        }