from flask import current_app as app
from app.conexion.Conexion import Conexion


class PedidosClientesDao:

    # ============================================================
    # LISTAR TODOS LOS PEDIDOS
    # ============================================================
    def obtener_pedidos(self):
        sql = """
        SELECT 
            cab.id_pedido_cab,
            cab.fecha_pedido,
            cab.fecha_entrega,
            cab.estado,
            cab.total,
            cli.nombre AS cliente,
            s.descripcion AS sucursal,
            u.usu_nick AS usuario
        FROM pedido_cliente_cab cab
        LEFT JOIN clientes cli ON cli.id_cliente = cab.id_cliente
        LEFT JOIN sucursales s ON s.id = cab.id_suc
        LEFT JOIN usuarios u ON u.usu_id = cab.usu_id
        ORDER BY cab.id_pedido_cab DESC
        """

        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:
                    cur.execute(sql)
                    filas = cur.fetchall()

                    datos = []

                    for f in filas:
                        datos.append({
                            "id_pedido_cab": f[0],
                            "fecha_pedido": f[1],
                            "fecha_entrega": f[2],
                            "estado": f[3],
                            "total": float(f[4]) if f[4] else 0,
                            "cliente": f[5],
                            "sucursal": f[6],
                            "usuario": f[7]
                        })

                    return datos

        except Exception as e:
            app.logger.error("Error al obtener pedidos de clientes: " + str(e))
            return []

    # ============================================================
    # OBTENER PEDIDO POR ID
    # ============================================================
    def obtener_por_id(self, id_pedido):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:

                    # -------- CABECERA ----------
                    cur.execute("""
                        SELECT 
                            cab.id_pedido_cab,
                            cab.id_cliente,
                            cab.fecha_pedido,
                            cab.fecha_entrega,
                            cab.estado,
                            cab.total,
                            cab.observaciones,
                            cab.usu_id,
                            cab.id_suc
                        FROM pedido_cliente_cab cab
                        WHERE cab.id_pedido_cab = %s
                    """, (id_pedido,))

                    cab = cur.fetchone()
                    if not cab:
                        return None

                    pedido = {
                        "id_pedido_cab": cab[0],
                        "id_cliente": cab[1],
                        "fecha_pedido": cab[2],
                        "fecha_entrega": cab[3],
                        "estado": cab[4],
                        "total": float(cab[5]) if cab[5] else 0,
                        "observaciones": cab[6],
                        "usu_id": cab[7],
                        "id_suc": cab[8],
                        "detalle": []
                    }

                    # -------- DETALLE ----------
                    cur.execute("""
                        SELECT 
                            id_pedido_det,
                            id_producto,
                            cantidad,
                            precio_unitario,
                            subtotal,
                            observaciones
                        FROM pedido_cliente_det
                        WHERE id_pedido_cab = %s
                        ORDER BY id_pedido_det
                    """, (id_pedido,))

                    det_rows = cur.fetchall()

                    for d in det_rows:
                        pedido["detalle"].append({
                            "id_pedido_det": d[0],
                            "id_producto": d[1],
                            "cantidad": float(d[2]),
                            "precio_unitario": float(d[3]),
                            "subtotal": float(d[4]),
                            "observaciones": d[5]
                        })

                    return pedido

        except Exception as e:
            app.logger.error("Error al obtener pedido por ID: " + str(e))
            return None

    # ============================================================
    # AGREGAR NUEVO PEDIDO
    # ============================================================
    def agregar(self, cab_dto):
        try:
            with Conexion().getConexion() as con:
                con.autocommit = False
                with con.cursor() as cur:

                    # Insertar cabecera
                    sql_cab = """
                    INSERT INTO pedido_cliente_cab
                    (id_cliente, fecha_pedido, fecha_entrega, estado, total, observaciones, usu_id, id_suc)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_pedido_cab
                    """

                    cur.execute(sql_cab, (
                        cab_dto.id_cliente,
                        cab_dto.fecha_pedido,
                        cab_dto.fecha_entrega,
                        cab_dto.estado,
                        cab_dto.total,
                        cab_dto.observaciones,
                        cab_dto.usu_id,
                        cab_dto.id_suc
                    ))

                    id_cab = cur.fetchone()[0]

                    # Insertar detalle
                    sql_det = """
                    INSERT INTO pedido_cliente_det
                    (id_pedido_cab, id_producto, cantidad, precio_unitario, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                    """

                    for det in cab_dto.detalle:
                        cur.execute(sql_det, (
                            id_cab,
                            det.id_producto,
                            det.cantidad,
                            det.precio_unitario,
                            det.observaciones
                        ))

                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al registrar pedido del cliente: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False

    # ============================================================
    # CAMBIAR ESTADO
    # ============================================================
    def cambiar_estado(self, id_pedido, nuevo_estado):
        try:
            with Conexion().getConexion() as con:
                with con.cursor() as cur:

                    cur.execute("""
                        UPDATE pedido_cliente_cab
                        SET estado = %s
                        WHERE id_pedido_cab = %s
                    """, (nuevo_estado, id_pedido))

                    con.commit()
                    return True

        except Exception as e:
            app.logger.error(f"Error al cambiar estado del pedido: {e}", exc_info=True)
            try:
                con.rollback()
            except:
                pass
            return False
