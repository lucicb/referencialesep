from app.conexion.Conexion import Conexion
from app.dao.registrar_ventas.registrar_apertura_cierre.dto.apertura_cierre_cab_dto import AperturaCierreCabDto
from app.dao.registrar_ventas.registrar_apertura_cierre.dto.apertura_cierre_det_dto import AperturaCierreDetDto

class AperturaCierreDao:

    def __init__(self):
        self.con = Conexion().getConexion()

    # ==============================
    # LISTAR TODAS LAS APERTURAS
    # ==============================
    def listar_aperturas(self):
        cur = self.con.cursor()

        cur.execute("""
            SELECT 
                id_caja_cab, id_suc, usu_id, 
                fecha_apertura, monto_inicial,
                fecha_cierre, monto_final, monto_teorico, diferencia,
                estado, observaciones
            FROM caja_cab
            ORDER BY fecha_apertura DESC
        """)

        filas = cur.fetchall()
        aperturas = []

        for f in filas:
            aperturas.append(
                AperturaCierreCabDto(
                    id_caja_cab = f[0],
                    id_suc = f[1],
                    usu_id = f[2],
                    fecha_apertura = f[3],
                    monto_inicial = f[4],
                    fecha_cierre = f[5],
                    monto_final = f[6],
                    monto_teorico = f[7],
                    diferencia = f[8],
                    estado = f[9],
                    observaciones = f[10]
                )
            )

        return aperturas

    # ==============================
    # OBTENER APERTURA POR ID
    # ==============================
    def obtener_por_id(self, id_caja_cab):
        cur = self.con.cursor()

        cur.execute("""
            SELECT 
                id_caja_cab, id_suc, usu_id, 
                fecha_apertura, monto_inicial,
                fecha_cierre, monto_final, monto_teorico, diferencia,
                estado, observaciones
            FROM caja_cab
            WHERE id_caja_cab = %s
        """, (id_caja_cab, ))

        f = cur.fetchone()

        if not f:
            return None

        return AperturaCierreCabDto(
            id_caja_cab = f[0],
            id_suc = f[1],
            usu_id = f[2],
            fecha_apertura = f[3],
            monto_inicial = f[4],
            fecha_cierre = f[5],
            monto_final = f[6],
            monto_teorico = f[7],
            diferencia = f[8],
            estado = f[9],
            observaciones = f[10]
        )

    # ==============================
    # CREAR APERTURA DE CAJA
    # ==============================
    def crear_apertura(self, dto: AperturaCierreCabDto):
        cur = self.con.cursor()

        cur.execute("""
            INSERT INTO caja_cab (
                id_suc, usu_id, fecha_apertura,
                monto_inicial, estado, observaciones
            )
            VALUES (%s, %s, NOW(), %s, %s, %s)
            RETURNING id_caja_cab
        """, (
            dto.id_suc,
            dto.usu_id,
            dto.monto_inicial,
            dto.estado,
            dto.observaciones
        ))

        id_generado = cur.fetchone()[0]
        self.con.commit()
        return id_generado

    # ==============================
    # CERRAR CAJA
    # ==============================
    def cerrar_caja(self, dto: AperturaCierreCabDto):
        cur = self.con.cursor()

        cur.execute("""
            UPDATE caja_cab
            SET fecha_cierre = NOW(),
                monto_final = %s,
                monto_teorico = %s,
                diferencia = %s,
                estado = %s,
                observaciones = %s
            WHERE id_caja_cab = %s
        """, (
            dto.monto_final,
            dto.monto_teorico,
            dto.diferencia,
            dto.estado,
            dto.observaciones,
            dto.id_caja_cab
        ))

        self.con.commit()

    # ==============================
    # LISTAR MOVIMIENTOS DE UNA CAJA
    # ==============================
    def listar_movimientos(self, id_caja_cab):
        cur = self.con.cursor()

        cur.execute("""
            SELECT 
                id_caja_mov, id_caja_cab, tipo,
                concepto, monto, fecha_mov, usu_id
            FROM caja_mov
            WHERE id_caja_cab = %s
            ORDER BY fecha_mov ASC
        """, (id_caja_cab, ))

        filas = cur.fetchall()
        movimientos = []

        for f in filas:
            movimientos.append(
                AperturaCierreDetDto(
                    id_caja_mov = f[0],
                    id_caja_cab = f[1],
                    tipo = f[2],
                    concepto = f[3],
                    monto = f[4],
                    fecha_mov = f[5],
                    usu_id = f[6]
                )
            )

        return movimientos

    # ==============================
    # INSERTAR MOVIMIENTO (DETALLE)
    # ==============================
    def agregar_movimiento(self, dto: AperturaCierreDetDto):
        cur = self.con.cursor()

        cur.execute("""
            INSERT INTO caja_mov (
                id_caja_cab, tipo, concepto,
                monto, fecha_mov, usu_id
            )
            VALUES (%s, %s, %s, %s, NOW(), %s)
            RETURNING id_caja_mov
        """, (
            dto.id_caja_cab,
            dto.tipo,
            dto.concepto,
            dto.monto,
            dto.usu_id
        ))

        id_generado = cur.fetchone()[0]
        self.con.commit()
        return id_generado
