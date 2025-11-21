from flask import current_app as app
from app.conexion.Conexion import Conexion


class ControlCalidadDao:

    # ===========================================================
    # OBTENER TODAS LAS CABECERAS DE CONTROL DE CALIDAD
    # ===========================================================
    def obtener_todos(self):
        sql = """
        SELECT 
            c.id_cali_cab,
            c.cod_orden_prod_cab,
            c.fecha_control,
            c.responsable,
            c.resultado,
            c.observaciones,
            c.estado,
            c.usu_id,

            u.usu_nick,
            u.usu_estado
        FROM control_calidad_cab c
        LEFT JOIN usuarios u ON u.usu_id = c.usu_id
        ORDER BY c.id_cali_cab DESC
        """

        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()

                    datos = []
                    for f in filas:
                        datos.append({
                            "id_cali_cab": f[0],
                            "cod_orden_prod_cab": f[1],
                            "fecha_control": f[2],
                            "responsable": f[3],
                            "resultado": f[4],
                            "observaciones": f[5],
                            "estado": f[6],
                            "usuario": {
                                "usu_id": f[7],
                                "usu_nick": f[8],
                                "usu_estado": f[9]
                            }
                        })

                    return datos

        except Exception as e:
            app.logger.error("Error al obtener controles de calidad: " + str(e))
            return []

    # ===========================================================
    # OBTENER UN CONTROL DE CALIDAD POR ID (CAB + DETALLE)
    # ===========================================================
    def obtener_por_id(self, id_cab):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:

                    # ---------- CABECERA ----------
                    cur.execute("""
                        SELECT 
                            c.id_cali_cab,
                            c.cod_orden_prod_cab,
                            c.fecha_control,
                            c.responsable,
                            c.resultado,
                            c.observaciones,
                            c.estado,
                            c.usu_id,

                            u.usu_nick,
                            u.usu_estado
                        FROM control_calidad_cab c
                        LEFT JOIN usuarios u ON u.usu_id = c.usu_id
                        WHERE c.id_cali_cab = %s
                    """, (id_cab,))

                    cab = cur.fetchone()
                    if not cab:
                        return None

                    control = {
                        "id_cali_cab": cab[0],
                        "cod_orden_prod_cab": cab[1],
                        "fecha_control": cab[2],
                        "responsable": cab[3],
                        "resultado": cab[4],
                        "observaciones": cab[5],
                        "estado": cab[6],
                        "usuario": {
                            "usu_id": cab[7],
                            "usu_nick": cab[8],
                            "usu_estado": cab[9]
                        },
                        "detalle": []
                    }

                    # ---------- DETALLE ----------
                    cur.execute("""
                        SELECT 
                            id_cali_det,
                            valor_esperado,
                            valor_obtenido,
                            resultado,
                            observaciones
                        FROM control_calidad_det
                        WHERE id_cali_cab = %s
                        ORDER BY id_cali_det
                    """, (id_cab,))

                    dets = cur.fetchall()
                    for d in dets:
                        control["detalle"].append({
                            "id_cali_det": d[0],
                            "valor_esperado": d[1],
                            "valor_obtenido": d[2],
                            "resultado": d[3],
                            "observaciones": d[4]
                        })

                    return control

        except Exception as e:
            app.logger.error("Error al obtener control de calidad por ID: " + str(e))
            return None

    # ===========================================================
    # AGREGAR CONTROL DE CALIDAD (CAB + DETALLE)
    # ===========================================================
    def agregar(self, cab_dto):
        try:
            with Conexion().getConexion() as con:
                con.autocommit = False
                with con.cursor() as cur:
                    
                    # Insertar CABECERA
                    sql_cab = """
                    INSERT INTO control_calidad_cab
                    (cod_orden_prod_cab, fecha_control, responsable, resultado, observaciones, estado, usu_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_cali_cab
                    """

                    cur.execute(sql_cab, (
                        cab_dto.cod_orden_prod_cab,
                        cab_dto.fecha_control,
                        cab_dto.responsable,
                        cab_dto.resultado,
                        cab_dto.observaciones,
                        cab_dto.estado,
                        cab_dto.usu_id
                    ))

                    id_cab = cur.fetchone()[0]

                    # Insertar DETALLE
                    sql_det = """
                    INSERT INTO control_calidad_det
                    (id_cali_cab, valor_esperado, valor_obtenido, resultado, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                    """

                    for det in cab_dto.detalle:
                        cur.execute(sql_det, (
                            id_cab,
                            det.valor_esperado,
                            det.valor_obtenido,
                            det.resultado,
                            det.observaciones
                        ))

                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al registrar control de calidad: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False

    # ===========================================================
    # CAMBIAR ESTADO
    # ===========================================================
    def cambiar_estado(self, id_cab, nuevo_estado):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        UPDATE control_calidad_cab
                        SET estado = %s
                        WHERE id_cali_cab = %s
                    """, (nuevo_estado, id_cab))
                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al cambiar estado del control de calidad: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False
