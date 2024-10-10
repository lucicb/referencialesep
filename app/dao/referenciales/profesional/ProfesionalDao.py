# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProfesionalDao:

    def getProfesional(self):

        profesionalSQL = """
        SELECT id, descripcion
        FROM profesional
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(profesionalSQL)
            profesional = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': profesional[0], 'descripcion': profesional[1]} for profesional in profesional]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los profesionales: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProfesionalById(self, id):

        profesionalSQL = """
        SELECT id, descripcion
        FROM profesional WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(profesionalSQL, (id,))
            profesionalEncontrada = cur.fetchone() # Obtener una sola fila
            if profesionalEncontrada:
                return {
                        "id": profesionalEncontrada[0],
                        "descripcion": profesionalEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener profesional: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProfesional(self, descripcion):

        insertProfesionalSQL = """
        INSERT INTO profesional(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertProfesionalSQL, (descripcion,))
            profesional_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return profesional_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar profesional: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateProfesional(self, id, descripcion):

        updateProfesionalSQL = """
        UPDATE profesional
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProfesionalSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar profesional: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProfesional(self, id):

        updateProfesionalSQL = """
        DELETE FROM profesional
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProfesionalSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar profesional: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()