from flask import current_app as app
from app.conexion.Conexion import Conexion

class OrdenProduccionDao:

    def obtener_ordenes(self):
        sql = """
        SELECT 
            op.cod_orden_prod_cab,
            op.fecha_creacion,
            op.fecha_inicio,
            op.fecha_fin_estimada,
            op.fecha_fin_real,
            op.estado,
            p.nombre AS producto,
            s.descripcion AS sucursal,
            u.usu_id,
            u.usu_nick,
            u.usu_clave,
            u.usu_nro_intentos,
            u.fun_id,
            u.gru_id,
            u.usu_estado
        FROM orden_produccion_cab op
        LEFT JOIN productos p ON p.id_producto = op.id_producto
        LEFT JOIN sucursales s ON s.id = op.id_suc
        LEFT JOIN usuarios u ON u.usu_id = op.usu_id
        ORDER BY op.cod_orden_prod_cab DESC
        """
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()
                    datos = []

                    for f in filas:
                        datos.append({
                            "cod_orden_prod_cab": f[0],
                            "fecha_creacion": f[1],
                            "fecha_inicio": f[2],
                            "fecha_fin_estimada": f[3],
                            "fecha_fin_real": f[4],
                            "estado": f[5],
                            "producto": f[6],
                            "sucursal": f[7],
                            "usuario": {
                                "usu_id": f[8],
                                "usu_nick": f[9],
                                "usu_clave": f[10],
                                "usu_nro_intentos": f[11],
                                "fun_id": f[12],
                                "gru_id": f[13],
                                "usu_estado": f[14]
                            }
                        })
                    return datos
        except Exception as e:
            app.logger.error("Error al obtener órdenes de producción: " + str(e))
            return []

    def obtener_por_id(self, cod_orden):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            op.cod_orden_prod_cab,
                            op.fecha_creacion,
                            op.fecha_inicio,
                            op.fecha_fin_estimada,
                            op.fecha_fin_real,
                            op.estado,
                            op.id_producto,
                            op.id_suc,
                            u.usu_id,
                            u.usu_nick,
                            u.usu_clave,
                            u.usu_nro_intentos,
                            u.fun_id,
                            u.gru_id,
                            u.usu_estado
                        FROM orden_produccion_cab op
                        LEFT JOIN usuarios u ON u.usu_id = op.usu_id
                        WHERE op.cod_orden_prod_cab = %s
                    """, (cod_orden,))
                    cab = cur.fetchone()
                    if not cab:
                        return None

                    orden = {
                        "cod_orden_prod_cab": cab[0],
                        "fecha_creacion": cab[1],
                        "fecha_inicio": cab[2],
                        "fecha_fin_estimada": cab[3],
                        "fecha_fin_real": cab[4],
                        "estado": cab[5],
                        "id_producto": cab[6],
                        "id_sucursal": cab[7],
                        "usuario": {
                            "usu_id": cab[8],
                            "usu_nick": cab[9],
                            "usu_clave": cab[10],
                            "usu_nro_intentos": cab[11],
                            "fun_id": cab[12],
                            "gru_id": cab[13],
                            "usu_estado": cab[14]
                        },
                        "detalle": []
                    }

                    cur.execute("""
                        SELECT 
                            cod_orden_prod_det,
                            cantidad,
                            costo_unitario,
                            id_producto
                        FROM orden_produccion_det
                        WHERE cod_orden_prod_cab = %s
                        ORDER BY cod_orden_prod_det
                    """, (cod_orden,))
                    detalle = cur.fetchall()
                    for d in detalle:
                        orden["detalle"].append({
                            "cod_det": d[0],
                            "cantidad": float(d[1]),
                            "costo_unitario": float(d[2]),
                            "id_producto": d[3]
                        })

                    return orden
        except Exception as e:
            app.logger.error("Error al obtener la orden por ID: " + str(e))
            return None

    def agregar(self, cab_dto):
        try:
            with Conexion().getConexion() as con:
                con.autocommit = False
                with con.cursor() as cur:
                    # Insertar cabecera
                    sql_cab = """
                    INSERT INTO orden_produccion_cab
                    (fecha_inicio, fecha_fin_estimada, id_producto, id_suc, usu_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING cod_orden_prod_cab
                    """
                    cur.execute(sql_cab, (
                        cab_dto.fecha_inicio,
                        cab_dto.fecha_fin_estimada,
                        cab_dto.id_producto,
                        cab_dto.id_suc,
                        cab_dto.usu_id
                    ))
                    cod_cab = cur.fetchone()[0]

                    # Insertar detalles
                    sql_det = """
                    INSERT INTO orden_produccion_det
                    (cod_orden_prod_cab, cantidad, costo_unitario, id_producto)
                    VALUES (%s, %s, %s, %s)
                    """
                    for det in cab_dto.detalle:
                        cur.execute(sql_det, (
                            cod_cab,
                            det.cantidad,
                            det.costo_unitario,
                            det.id_producto
                        ))

                    con.commit()
                    return True
        except Exception as e:
            app.logger.error(f"Error al registrar orden: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False

    def cambiar_estado(self, cod_orden, nuevo_estado):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        UPDATE orden_produccion_cab
                        SET estado = %s
                        WHERE cod_orden_prod_cab = %s
                    """, (nuevo_estado, cod_orden))
                    con.commit()
                    return True
        except Exception as e:
            app.logger.error(f"Error al cambiar estado de la orden: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False
