# registrar_mermas_dao.py
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MermasDao:

    # =========================
    # OBTENER TODAS LAS MERMAS
    # =========================
    def obtener_mermas(self):
        sql = """
        SELECT 
            mc.id_merma_cab,
            mc.cod_orden_prod_cab,
            mc.fecha_registro,
            mc.responsable,
            mc.motivo_general,
            mc.observaciones,
            mc.usu_id,
            mc.suc_id,
            u.usu_nick,
            s.descripcion AS sucursal
        FROM merma_cab mc
        LEFT JOIN usuarios u ON u.usu_id = mc.usu_id
        LEFT JOIN sucursales s ON s.id = mc.suc_id
        ORDER BY mc.id_merma_cab DESC
        """
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()
                    datos = []
                    for f in filas:
                        datos.append({
                            "id_merma_cab": f[0],
                            "cod_orden_prod_cab": f[1],
                            "fecha_registro": f[2],
                            "responsable": f[3],
                            "motivo_general": f[4],
                            "observaciones": f[5],
                            "usu_id": f[6],
                            "suc_id": f[7],
                            "usuario": {"usu_nick": f[8]},
                            "sucursal": f[9],
                            "detalle": []  # se completa más abajo
                        })
                    return datos
        except Exception as e:
            app.logger.error("Error al obtener mermas: " + str(e))
            return []

    # =========================
    # OBTENER MERMA POR ID
    # =========================
    def obtener_por_id(self, id_merma):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            id_merma_cab,
                            cod_orden_prod_cab,
                            fecha_registro,
                            responsable,
                            motivo_general,
                            observaciones,
                            usu_id,
                            suc_id
                        FROM merma_cab
                        WHERE id_merma_cab = %s
                    """, (id_merma,))
                    cab = cur.fetchone()
                    if not cab:
                        return None

                    merma = {
                        "id_merma_cab": cab[0],
                        "cod_orden_prod_cab": cab[1],
                        "fecha_registro": cab[2],
                        "responsable": cab[3],
                        "motivo_general": cab[4],
                        "observaciones": cab[5],
                        "usu_id": cab[6],
                        "suc_id": cab[7],
                        "detalle": []
                    }

                    # Obtener detalle
                    cur.execute("""
                        SELECT 
                            id_merma_det,
                            id_producto,
                            cantidad,
                            motivo,
                            costo_unitario,
                            costo_total
                        FROM merma_det
                        WHERE id_merma_cab = %s
                        ORDER BY id_merma_det
                    """, (id_merma,))
                    detalle = cur.fetchall()
                    for d in detalle:
                        merma["detalle"].append({
                            "id_merma_det": d[0],
                            "id_producto": d[1],
                            "cantidad": float(d[2]),
                            "motivo": d[3],
                            "costo_unitario": float(d[4]) if d[4] else 0,
                            "costo_total": float(d[5]) if d[5] else 0
                        })

                    return merma
        except Exception as e:
            app.logger.error("Error al obtener la merma por ID: " + str(e))
            return None

    # =========================
    # AGREGAR NUEVA MERMA
    # =========================
    def agregar(self, cab_dto):
        try:
            with Conexion().getConexion() as con:
                con.autocommit = False
                with con.cursor() as cur:
                    # Insertar cabecera
                    sql_cab = """
                    INSERT INTO merma_cab
                    (cod_orden_prod_cab, fecha_registro, responsable, motivo_general, observaciones, usu_id, suc_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_merma_cab
                    """
                    cur.execute(sql_cab, (
                        cab_dto.cod_orden_prod_cab,
                        cab_dto.fecha_registro,
                        cab_dto.responsable,
                        cab_dto.motivo_general,
                        cab_dto.observaciones,
                        cab_dto.usu_id,
                        cab_dto.suc_id
                    ))
                    id_cab = cur.fetchone()[0]

                    # Insertar detalle
                    sql_det = """
                    INSERT INTO merma_det
                    (id_merma_cab, id_producto, cantidad, motivo, costo_unitario)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    for det in cab_dto.detalle:
                        cur.execute(sql_det, (
                            id_cab,
                            det.id_producto,
                            det.cantidad,
                            det.motivo,
                            det.costo_unitario
                        ))

                    con.commit()
                    return True
        except Exception as e:
            app.logger.error(f"Error al registrar merma: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False
