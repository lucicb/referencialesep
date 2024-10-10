# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipodepagoDao:

    def getTipodepago(self):

        tipodepagoSQL = """
        SELECT id, descripcion
        FROM tipodepago
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipodepagoSQL)
            tipodepago = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': tipodepago[0], 'descripcion': tipodepago[1]} for tipodepago in tipodepago]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipo de pago: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipodepagoById(self, id):

        tipodepagoSQL = """
        SELECT id, descripcion
        FROM tipodepago WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipodepagoSQL, (id,))
            tipodepagoEncontrada = cur.fetchone() # Obtener una sola fila
            if tipodepagoEncontrada:
                return {
                        "id": tipodepagoEncontrada[0],
                        "descripcion": tipodepagoEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener tipodepago: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipodepago(self, descripcion):

        insertTipodepagoSQL = """
        INSERT INTO tipodepago(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertTipodepagoSQL, (descripcion,))
            tipodepago_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return tipodepago_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar tipodepago: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateTipodepago(self, id, descripcion):

        updateTipodepagoSQL = """
        UPDATE tipodepago
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipodepagoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tipodepago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipodepago(self, id):

        updateTipodepagoSQL = """
        DELETE FROM tipodepago
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipodepagoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tipodepago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()