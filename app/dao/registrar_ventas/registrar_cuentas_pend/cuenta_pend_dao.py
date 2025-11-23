from app.conexion.Conexion import Conexion

class CuentaPendDao:

    def __init__(self):
        self.con = Conexion().getConexion()

    # Crear cuenta pendiente
    def crear_cuenta(self, dto):
        cur = self.con.cursor()

        cur.execute("""
            INSERT INTO cuenta_pend (
                id_cliente, id_venta_cab, fecha_registro,
                monto_original, monto_pagado, fecha_vencimiento,
                estado, observaciones
            )
            VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s)
            RETURNING id_cuenta_pend
        """, (
            dto.id_cliente,
            dto.id_venta_cab,
            dto.monto_original,
            dto.monto_pagado,
            dto.fecha_vencimiento,
            dto.estado,
            dto.observaciones
        ))

        id_generado = cur.fetchone()[0]
        self.con.commit()
        return id_generado
