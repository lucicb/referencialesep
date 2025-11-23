# app/dao/registrar_ventas/registrar_venta/dto/registrar_venta_cab_dto.py

from datetime import datetime

class VentaCabDto:
    def __init__(
        self,
        id_venta_cab=None,
        id_cliente=None,
        id_suc=None,
        usu_id=None,
        fecha_venta=None,
        nro_factura=None,
        tipo_venta=None,
        total=0.0,
        estado='pendiente',
        observaciones='',
        id_cuenta_pend=None  # FK a cuenta pendiente si aplica
    ):
        self.id_venta_cab = id_venta_cab      # ID generado automáticamente
        self.id_cliente = id_cliente          # FK cliente
        self.id_suc = id_suc                  # FK sucursal
        self.usu_id = usu_id                  # Usuario que registra
        self.fecha_venta = fecha_venta or datetime.now()
        self.nro_factura = nro_factura
        self.tipo_venta = tipo_venta          # contado / crédito
        self.total = total                    # Total calculado de la venta
        self.estado = estado                  # procesado / anulado / pendiente
        self.observaciones = observaciones
        self.id_cuenta_pend = id_cuenta_pend  # FK cuenta pendiente si aplica

    def to_dict(self):
        return {
            "id_venta_cab": self.id_venta_cab,
            "id_cliente": self.id_cliente,
            "id_suc": self.id_suc,
            "usu_id": self.usu_id,
            "fecha_venta": self.fecha_venta,
            "nro_factura": self.nro_factura,
            "tipo_venta": self.tipo_venta,
            "total": self.total,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "id_cuenta_pend": self.id_cuenta_pend
        }
