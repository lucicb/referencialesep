# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def get_depositos(self):
        sql = """
        SELECT
            d.id_deposito,
            d.nombre_deposito,
            d.id_sucursal
        FROM
            depositos d
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            depositos = cur.fetchall()
            return [{'id_deposito': d[0], 'descripcion': d[1], 'id_sucursal': d[2]} for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def get_deposito_by_id(self, id_deposito: int):
        sql = """
        SELECT
            d.id_deposito,
            d.nombre_deposito,
            d.id_sucursal
        FROM
            depositos d
        WHERE
            d.id_deposito = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_deposito,))
            deposito = cur.fetchone()
            if deposito:
                return {'id_deposito': deposito[0], 'nombre_deposito': deposito[1], 'id_sucursal': deposito[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener depósito: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def get_depositos_by_sucursal(self, id_sucursal: int):
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
            app.logger.error(f"Error al obtener depósitos por sucursal: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def guardarDeposito(self, nombre_deposito, id_sucursal):
        insertSQL = """
        INSERT INTO depositos(nombre_deposito, id_sucursal) 
        VALUES(%s, %s) RETURNING id_deposito
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertSQL, (nombre_deposito, id_sucursal))
            deposito_id = cur.fetchone()[0]
            con.commit()
            return deposito_id
        except Exception as e:
            app.logger.error(f"Error al insertar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateDeposito(self, id_deposito, nombre_deposito, id_sucursal):
        updateSQL = """
        UPDATE depositos 
        SET nombre_deposito = %s, id_sucursal = %s 
        WHERE id_deposito = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateSQL, (nombre_deposito, id_sucursal, id_deposito))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteDeposito(self, id_deposito):
        deleteSQL = """
        DELETE FROM depositos WHERE id_deposito = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteSQL, (id_deposito,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


