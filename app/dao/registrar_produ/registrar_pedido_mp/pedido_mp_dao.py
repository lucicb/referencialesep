from flask import current_app as app
from app.conexion.Conexion import Conexion

class PedidoMateriaPrimaDao:

    # ============================================
    #  OBTENER TODOS LOS PEDIDOS (LISTADO)
    # ============================================
    def obtener_pedidos(self):
        sql = """
        SELECT 
            pmp.cod_pedido_mp,
            pmp.fecha_creacion,
            pmp.estado,
            s.descripcion AS sucursal,
            u.usu_nick AS usuario,
            pmp.observaciones,
            pmp.prioridad
        FROM pedido_mp_cab pmp
        LEFT JOIN sucursales s ON s.id = pmp.id_suc
        LEFT JOIN usuarios u ON u.usu_id = pmp.usu_id
        ORDER BY pmp.cod_pedido_mp DESC
        """
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()
                    datos = []
                    for f in filas:
                        datos.append({
                            "cod_pedido_mp": f[0],
                            "fecha_creacion": f[1],
                            "estado": f[2],
                            "sucursal": f[3],
                            "usuario": f[4],
                            "observaciones": f[5],
                            "prioridad": f[6]
                        })
                    return datos
        except Exception as e:
            app.logger.error("Error al obtener pedidos MP: " + str(e))
            return []

    # ============================================
    #  OBTENER CAB + DETALLE POR ID
    # ============================================
    def obtener_por_id(self, cod_pedido):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    # CABECERA
                    cur.execute("""
                        SELECT 
                            pmp.cod_pedido_mp,
                            pmp.fecha_creacion,
                            pmp.estado,
                            pmp.id_suc,
                            pmp.observaciones,
                            pmp.prioridad,
                            u.usu_id,
                            u.usu_nick
                        FROM pedido_mp_cab pmp
                        LEFT JOIN usuarios u ON u.usu_id = pmp.usu_id
                        WHERE pmp.cod_pedido_mp = %s
                    """, (cod_pedido,))
                    cab = cur.fetchone()
                    if not cab:
                        return None
                    pedido = {
                        "cod_pedido_mp": cab[0],
                        "fecha_creacion": cab[1],
                        "estado": cab[2],
                        "id_suc": cab[3],
                        "observaciones": cab[4],
                        "prioridad": cab[5],
                        "usuario": {"usu_id": cab[6], "usu_nick": cab[7]},
                        "detalle": []
                    }
                    # DETALLE
                    cur.execute("""
                        SELECT 
                            d.id_detalle,
                            d.id_materia_prima,
                            mp.descripcion,
                            d.cantidad,
                            d.estado_item,
                            d.cantidad_aprobada
                        FROM pedido_mp_det d
                        LEFT JOIN materia_prima mp 
                               ON mp.id_materia_prima = d.id_materia_prima
                        WHERE d.cod_pedido_mp = %s
                        ORDER BY d.id_detalle
                    """, (cod_pedido,))
                    detalle = cur.fetchall()
                    for d in detalle:
                        pedido["detalle"].append({
                            "id_detalle": d[0],
                            "id_materia_prima": d[1],
                            "materia_prima": d[2],
                            "cantidad": float(d[3]),
                            "estado_item": d[4],
                            "cantidad_aprobada": float(d[5]) if d[5] else None
                        })
                    return pedido
        except Exception as e:
            app.logger.error("Error al obtener pedido MP por ID: " + str(e))
            return None

    # ============================================
    # INSERTAR CABECERA + DETALLE
    # ============================================
    def agregar(self, cab_dto):
        """
        Inserta un nuevo pedido de materia prima con su detalle.
        cab_dto: instancia de PedidoMpCabDto con lista de PedidoMpDetDto
        Retorna True si se guarda correctamente, False si hay error.
        """
        con = None
        try:
            con = Conexion().getConexion()
            con.autocommit = False
            with con.cursor() as cur:
                # INSERT CABECERA
                sql_cab = """
                INSERT INTO pedido_mp_cab
                (usu_id, id_suc, observaciones, prioridad, fecha_pedido, fecha_entrega_estimada)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING cod_pedido_mp
                """
                cur.execute(sql_cab, (
                    cab_dto.usu_id,
                    cab_dto.id_suc,
                    cab_dto.observaciones,
                    cab_dto.prioridad,
                    cab_dto.fecha_pedido,
                    cab_dto.fecha_entrega_estimada
                ))
                cod_cab_row = cur.fetchone()
                if not cod_cab_row:
                    raise Exception("No se obtuvo el código de cabecera insertada")
                cod_cab = cod_cab_row[0]

                # INSERT DETALLE
                sql_det = """
                INSERT INTO pedido_mp_det
                (cod_pedido_mp, id_materia_prima, cantidad, costo_unitario, estado_item)
                VALUES (%s, %s, %s, %s, %s)
                """
                for det in cab_dto.detalle:
                    cur.execute(sql_det, (
                        cod_cab,
                        det.id_materia_prima,
                        det.cantidad,
                        det.costo_unitario,
                        'PENDIENTE'
                    ))
                # CONFIRMAR
                con.commit()
                return True
        except Exception as e:
            app.logger.error(f"Error al registrar pedido MP: {e}", exc_info=True)
            if con:
                try:
                    con.rollback()
                except:
                    pass
            return False

    # ============================================
    # CAMBIAR ESTADO DEL PEDIDO
    # ============================================
    def cambiar_estado(self, cod_pedido, nuevo_estado):
        con = None
        try:
            con = Conexion().getConexion()
            with con.cursor() as cur:
                cur.execute("""
                    UPDATE pedido_mp_cab
                    SET estado = %s
                    WHERE cod_pedido_mp = %s
                """, (nuevo_estado, cod_pedido))
                con.commit()
                return True
        except Exception as e:
            app.logger.error(f"Error al cambiar estado del pedido MP: {e}", exc_info=True)
            if con:
                try:
                    con.rollback()
                except:
                    pass
            return False
