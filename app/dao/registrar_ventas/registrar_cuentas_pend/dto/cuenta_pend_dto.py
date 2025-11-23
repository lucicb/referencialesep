class CuentaPendDto:
    def __init__(
        self,
        id_cuenta_pend=None,
        id_cliente=None,
        id_venta_cab=None,
        monto_original=0,
        monto_pagado=0,
        fecha_vencimiento=None,
        estado='pendiente',
        observaciones=''
    ):
        self.id_cuenta_pend = id_cuenta_pend
        self.id_cliente = id_cliente
        self.id_venta_cab = id_venta_cab
        self.monto_original = monto_original
        self.monto_pagado = monto_pagado
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.observaciones = observaciones
