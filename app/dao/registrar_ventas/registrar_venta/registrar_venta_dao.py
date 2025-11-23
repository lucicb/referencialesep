from app.conexion.Conexion import Conexion
from app.dao.registrar_ventas.registrar_venta.dto.registrar_venta_cab_dto import VentaCabDto
from app.dao.registrar_ventas.registrar_venta.dto.registrar_venta_det_dto import VentaDetDto
from datetime import datetime

class RegistrarVentaDao:

    def __init__(self):
        self.con = Conexion().getConexion()

    # ==============================
    # LISTAR TODAS LAS VENTAS
    # ==============================
    def listar_cabecera(self):
        cur = self.con.cursor()
        cur.execute("""
            SELECT 
                id_venta_cab, id_cliente, id_suc, usu_id,
                fecha_venta, nro_factura, tipo_venta,
                total, estado, observaciones, id_cuenta_pend
            FROM venta_cab
            ORDER BY fecha_venta DESC
        """)
        filas = cur.fetchall()
        ventas = []

        for f in filas:
            ventas.append(
                VentaCabDto(
                    id_venta_cab=f[0],
                    id_cliente=f[1],
                    id_suc=f[2],
                    usu_id=f[3],
                    fecha_venta=f[4],
                    nro_factura=f[5],
                    tipo_venta=f[6],
                    total=f[7],
                    estado=f[8],
                    observaciones=f[9],
                    id_cuenta_pend=f[10]
                )
            )

        return ventas

    # ==============================
    # OBTENER CABECERA POR ID
    # ==============================
    def obtener_venta_cab(self, id_venta_cab):
        cur = self.con.cursor()
        cur.execute("""
            SELECT 
                id_venta_cab, id_cliente, id_suc, usu_id,
                fecha_venta, nro_factura, tipo_venta,
                total, estado, observaciones, id_cuenta_pend
            FROM venta_cab
            WHERE id_venta_cab = %s
        """, (id_venta_cab,))
        f = cur.fetchone()
        if not f:
            return None

        return VentaCabDto(
            id_venta_cab=f[0],
            id_cliente=f[1],
            id_suc=f[2],
            usu_id=f[3],
            fecha_venta=f[4],
            nro_factura=f[5],
            tipo_venta=f[6],
            total=f[7],
            estado=f[8],
            observaciones=f[9],
            id_cuenta_pend=f[10]
        )

    # ==============================
    # OBTENER DETALLE POR CABECERA
    # ==============================
    def obtener_detalle(self, id_venta_cab):
        cur = self.con.cursor()
        cur.execute("""
            SELECT 
                id_venta_det, id_venta_cab, id_producto, cantidad, 
                precio_unitario, subtotal, descuento, total_item, observaciones
            FROM venta_det
            WHERE id_venta_cab = %s
            ORDER BY id_venta_det ASC
        """, (id_venta_cab,))
        filas = cur.fetchall()
        detalle = []

        for f in filas:
            detalle.append(
                VentaDetDto(
                    id_venta_det=f[0],
                    id_venta_cab=f[1],
                    id_producto=f[2],
                    cantidad=f[3],
                    precio_unitario=f[4],
                    subtotal=f[5],
                    descuento=f[6],
                    total_item=f[7],
                    observaciones=f[8]
                )
            )

        return detalle

    # ==============================
    # CREAR NUEVA VENTA
    # ==============================
    def crear_venta(self, venta_cab_dto: VentaCabDto, detalles: list):
        """
        Crea la cabecera y el detalle de la venta.
        Si es tipo crédito, genera automáticamente la cuenta pendiente.
        """
        cur = self.con.cursor()

        # ------------------------------
        # INSERTAR CABECERA
        # ------------------------------
        cur.execute("""
            INSERT INTO venta_cab (
                id_cliente, id_suc, usu_id, fecha_venta, nro_factura, tipo_venta,
                total, estado, observaciones
            ) VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s)
            RETURNING id_venta_cab
        """, (
            venta_cab_dto.id_cliente,
            venta_cab_dto.id_suc,
            venta_cab_dto.usu_id,
            venta_cab_dto.nro_factura,
            venta_cab_dto.tipo_venta,
            venta_cab_dto.total,
            venta_cab_dto.estado,
            venta_cab_dto.observaciones
        ))

        id_venta_cab = cur.fetchone()[0]

        # ------------------------------
        # INSERTAR DETALLES
        # ------------------------------
        total_venta = 0
        for det in detalles:
            subtotal = det.cantidad * det.precio_unitario
            total_item = subtotal - (det.descuento or 0)
            total_venta += total_item

            cur.execute("""
                INSERT INTO venta_det (
                    id_venta_cab, id_producto, cantidad, precio_unitario, descuento, total_item, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_venta_det
            """, (
                id_venta_cab,
                det.id_producto,
                det.cantidad,
                det.precio_unitario,
                det.descuento,
                total_item,
                det.observaciones
            ))
            det.id_venta_det = cur.fetchone()[0]

        # ------------------------------
        # ACTUALIZAR TOTAL EN CABECERA
        # ------------------------------
        cur.execute("""
            UPDATE venta_cab
            SET total = %s
            WHERE id_venta_cab = %s
        """, (total_venta, id_venta_cab))

        # ------------------------------
        # CREAR CUENTA PENDIENTE SI ES CRÉDITO
        # ------------------------------
        if venta_cab_dto.tipo_venta.lower() == 'credito':
            cur.execute("""
                INSERT INTO cuenta_pend (
                    id_cliente, id_venta_cab, fecha_registro, monto_original, monto_pagado, fecha_vencimiento, estado, observaciones
                ) VALUES (%s, %s, NOW(), %s, 0, %s, 'pendiente', %s)
                RETURNING id_cuenta_pend
            """, (
                venta_cab_dto.id_cliente,
                id_venta_cab,
                total_venta,
                venta_cab_dto.fecha_vencimiento,
                venta_cab_dto.observaciones
            ))
            id_cuenta_pend = cur.fetchone()[0]
            # asociar el id de cuenta pendiente a la venta
            cur.execute("""
                UPDATE venta_cab
                SET id_cuenta_pend = %s
                WHERE id_venta_cab = %s
            """, (id_cuenta_pend, id_venta_cab))

        self.con.commit()
        return id_venta_cab
