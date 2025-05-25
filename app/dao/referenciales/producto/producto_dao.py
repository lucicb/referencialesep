# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProductoDao:

    def get_productos(self):
        producto_sql = """
        SELECT
            id_producto,
            nombre,
            cantidad,
            precio_unitario
        FROM
            public.productos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(producto_sql)
            productos = cur.fetchall()
            return [
                {
                    'id_producto': item[0],
                    'nombre': item[1],
                    'cantidad': item[2],
                    'precio_unitario': item[3]
                }
                for item in productos
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los productos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_sucursal_depositos(self, id_sucursal: int):
        sucursal_sql = """
        SELECT
            sd.id_deposito,
            d.descripcion AS nombre_deposito
        FROM
            sucursal_depositos sd
        LEFT JOIN depositos d
            ON sd.id_deposito = d.id_deposito
        WHERE
            sd.id_sucursal = %s AND sd.estado = true
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sucursal_sql, (id_sucursal,))
            sucursales = cur.fetchall()
            return [
                {
                    'id_deposito': sucursal[0],
                    'nombre_deposito': sucursal[1]
                }
                for sucursal in sucursales
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener los depósitos de la sucursal: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
