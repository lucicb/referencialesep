# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipodeconsultaDao:

    def getTipodeconsulta(self):

        tipodeconsultaSQL = """
        SELECT id, descripcion
        FROM tipodeconsulta
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipodeconsultaSQL)
            tipodeconsulta = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': tipodeconsulta[0], 'descripcion': tipodeconsulta[1]} for tipodeconsulta in tipodeconsulta]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los tipos de consultas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTipodeconsultaById(self, id):

        tipodeconsultaSQL = """
        SELECT id, descripcion
        FROM tipodeconsulta WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tipodeconsultaSQL, (id,))
            tipodeconsultaEncontrada = cur.fetchone() # Obtener una sola fila
            if tipodeconsultaEncontrada:
                return {
                        "id": tipodeconsultaEncontrada[0],
                        "descripcion": tipodeconsultaEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener tipodeconsulta: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTipodeconsulta(self, descripcion):

        insertTipodeconsultaSQL = """
        INSERT INTO tipodeconsulta(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertTipodeconsultaSQL, (descripcion,))
            tipodeconsulta_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return tipodeconsulta_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar tipodeconsulta: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateTipodeconsulta(self, id, descripcion):

        updateTipodeconsultaSQL = """
        UPDATE tipodeconsulta
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipodeconsultaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tipodeconsulta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTipodeconsulta(self, id):

        updateTipodeconsultaSQL = """
        DELETE FROM tipodeconsulta
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTipodeconsultaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tipodeconsulta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()