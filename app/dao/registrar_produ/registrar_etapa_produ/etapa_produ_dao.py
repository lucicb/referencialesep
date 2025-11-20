from flask import current_app as app
from app.conexion.Conexion import Conexion


class EtapaProduDao:

    # ============================================================
    #  OBTENER TODAS LAS ETAPAS (CAB + JOIN A PRODUCTO, SUCURSAL)
    # ============================================================
    def obtener_etapas(self):
        sql = """
        SELECT 
            cab.id_etapa_cab,
            cab.cod_orden_prod_cab,
            cab.fecha,
            cab.id_producto,
            p.nombre AS producto_nombre,
            cab.cantidad_planificada,
            cab.estado,
            cab.observaciones,
            cab.fecha_inicio,
            cab.fecha_fin,
            cab.usu_id,
            cab.id_suc,
            s.descripcion AS sucursal_desc
        FROM etapa_produ_cab cab
        LEFT JOIN productos p ON p.id_producto = cab.id_producto
        LEFT JOIN sucursales s ON s.id = cab.id_suc
        ORDER BY cab.id_etapa_cab DESC
        """
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()

                    datos = []
                    for f in filas:
                        datos.append({
                            "id_etapa_cab": f[0],
                            "cod_orden_prod_cab": f[1],
                            "fecha": f[2],
                            "id_producto": f[3],
                            "producto": f[4],
                            "cantidad_planificada": float(f[5]),
                            "estado": f[6],
                            "observaciones": f[7],
                            "fecha_inicio": f[8],
                            "fecha_fin": f[9],
                            "usu_id": f[10],
                            "id_suc": f[11],
                            "sucursal": f[12]
                        })

                    return datos
        except Exception as e:
            app.logger.error("Error al obtener etapas: " + str(e))
            return []

    # ============================================================
    #        OBTENER CABECERA + DETALLE POR ID
    # ============================================================
    def obtener_por_id(self, id_etapa_cab):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:

                    # CABECERA
                    sql_cab = """
                        SELECT 
                            cab.id_etapa_cab,
                            cab.cod_orden_prod_cab,
                            cab.fecha,
                            cab.id_producto,
                            p.nombre,
                            cab.cantidad_planificada,
                            cab.estado,
                            cab.observaciones,
                            cab.fecha_inicio,
                            cab.fecha_fin,
                            cab.usu_id,
                            cab.id_suc,
                            s.descripcion
                        FROM etapa_produ_cab cab
                        LEFT JOIN productos p ON p.id_producto = cab.id_producto
                        LEFT JOIN sucursales s ON s.id = cab.id_suc
                        WHERE cab.id_etapa_cab = %s
                    """
                    cur.execute(sql_cab, (id_etapa_cab,))
                    cab = cur.fetchone()

                    if not cab:
                        return None

                    etapa = {
                        "id_etapa_cab": cab[0],
                        "cod_orden_prod_cab": cab[1],
                        "fecha": cab[2],
                        "id_producto": cab[3],
                        "producto": cab[4],
                        "cantidad_planificada": float(cab[5]),
                        "estado": cab[6],
                        "observaciones": cab[7],
                        "fecha_inicio": cab[8],
                        "fecha_fin": cab[9],
                        "usu_id": cab[10],
                        "id_suc": cab[11],
                        "sucursal": cab[12],
                        "detalle": []
                    }

                    # DETALLE
                    sql_det = """
                        SELECT 
                            det.id_etapa_det,
                            det.etapa,
                            det.descripcion,
                            det.responsable,
                            det.fecha_inicio,
                            det.fecha_fin,
                            det.estado,
                            det.avance
                        FROM etapa_produ_det det
                        WHERE det.id_etapa_cab = %s
                        ORDER BY det.id_etapa_det
                    """
                    cur.execute(sql_det, (id_etapa_cab,))
                    detalle = cur.fetchall()

                    for d in detalle:
                        etapa["detalle"].append({
                            "id_etapa_det": d[0],
                            "etapa": d[1],
                            "descripcion": d[2],
                            "responsable": d[3],
                            "fecha_inicio": d[4],
                            "fecha_fin": d[5],
                            "estado": d[6],
                            "avance": d[7]
                        })

                    return etapa

        except Exception as e:
            app.logger.error("Error al obtener etapa por ID: " + str(e))
            return None

    # ============================================================
    #                 INSERTAR CAB + DETALLE
    # ============================================================
    def agregar(self, cab_dto):
        try:
            with Conexion().getConexion() as con:
                con.autocommit = False

                with con.cursor() as cur:

                    # INSERTAR CABECERA
                    sql_cab = """
                        INSERT INTO etapa_produ_cab
                        (cod_orden_prod_cab, fecha, id_producto, cantidad_planificada, estado,
                         observaciones, fecha_inicio, fecha_fin, usu_id, id_suc)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id_etapa_cab
                    """
                    cur.execute(sql_cab, (
                        cab_dto.cod_orden_prod_cab,
                        cab_dto.fecha,
                        cab_dto.id_producto,
                        cab_dto.cantidad_planificada,
                        cab_dto.estado,
                        cab_dto.observaciones,
                        cab_dto.fecha_inicio,
                        cab_dto.fecha_fin,
                        cab_dto.usu_id,
                        cab_dto.id_suc
                    ))

                    id_cab = cur.fetchone()[0]

                    # INSERTAR DETALLE
                    sql_det = """
                        INSERT INTO etapa_produ_det
                        (id_etapa_cab, etapa, descripcion, responsable, fecha_inicio, fecha_fin, estado, avance)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """

                    for det in cab_dto.detalle:
                        cur.execute(sql_det, (
                            id_cab,
                            det.etapa,
                            det.descripcion,
                            det.responsable,
                            det.fecha_inicio,
                            det.fecha_fin,
                            det.estado,
                            det.avance
                        ))

                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al agregar etapa producción: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False

    # ============================================================
    #                  CAMBIAR ESTADO CABECERA
    # ============================================================
    def cambiar_estado(self, id_etapa_cab, nuevo_estado):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        UPDATE etapa_produ_cab
                        SET estado = %s
                        WHERE id_etapa_cab = %s
                    """, (nuevo_estado, id_etapa_cab))

                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al cambiar estado: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False
