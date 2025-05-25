# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class SucursalDao:

    def get_sucursales(self):
        sql = """
        SELECT
            s.id,
            s.descripcion AS nombre_sucursal
        FROM
            sucursales s
        WHERE EXISTS (
            SELECT 1 FROM depositos d WHERE d.id_sucursal = s.id
        )
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            sucursales = cur.fetchall()
            return [{'id': s[0], 'descripcion': s[1]} for s in sucursales]
        except Exception as e:
            app.logger.error(f"Error al obtener sucursales: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_depositos_por_sucursal(self, id_sucursal: int):
        sql = """
        SELECT
            d.id_deposito,
            d.nombre_deposito
        FROM
            depositos d
        WHERE
            d.id_sucursal = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_sucursal,))
            depositos = cur.fetchall()
            return [{'id_deposito': d[0], 'nombre_deposito': d[1]} for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # Métodos de ciudades (opcional, si realmente los usás desde esta clase)
    def getCiudadById(self, id):
        ciudadSQL = """
        SELECT id, descripcion FROM ciudades WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ciudadSQL, (id,))
            ciudad = cur.fetchone()
            return {"id": ciudad[0], "descripcion": ciudad[1]} if ciudad else None
        except Exception as e:
            app.logger.error(f"Error al obtener ciudad: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarCiudad(self, descripcion):
        insertSQL = """
        INSERT INTO ciudades(descripcion) VALUES(%s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertSQL, (descripcion,))
            ciudad_id = cur.fetchone()[0]
            con.commit()
            return ciudad_id
        except Exception as e:
            app.logger.error(f"Error al insertar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCiudad(self, id, descripcion):
        updateSQL = """
        UPDATE ciudades SET descripcion=%s WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateSQL, (descripcion, id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCiudad(self, id):
        deleteSQL = """
        DELETE FROM ciudades WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteSQL, (id,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar ciudad: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
