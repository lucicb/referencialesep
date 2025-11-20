# producto_dao.py
from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.referenciales.producto.producto_dto import ProductoDto

class ProductoDao:

    # ================================
    # Obtener todos los productos
    # ================================
    def get_productos(self):
        sql = """
        SELECT 
            id_producto,
            nombre,
            COALESCE(cantidad,0) AS cantidad,
            COALESCE(precio_unitario,0) AS precio_unitario
        FROM public.productos
        ORDER BY nombre
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            filas = cur.fetchall()
            productos = []
            for f in filas:
                productos.append(ProductoDto(
                    id_producto=f[0],
                    nombre=f[1],
                    cantidad=float(f[2]),
                    precio_unitario=float(f[3])
                ))
            return productos
        except Exception as e:
            app.logger.error(f"Error al obtener productos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ================================
    # Obtener producto por ID
    # ================================
    def get_producto_by_id(self, id_producto):
        sql = """
        SELECT 
            id_producto,
            nombre,
            COALESCE(cantidad,0) AS cantidad,
            COALESCE(precio_unitario,0) AS precio_unitario
        FROM public.productos
        WHERE id_producto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_producto,))
            f = cur.fetchone()
            if f:
                return ProductoDto(
                    id_producto=f[0],
                    nombre=f[1],
                    cantidad=float(f[2]),
                    precio_unitario=float(f[3])
                )
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener producto por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
