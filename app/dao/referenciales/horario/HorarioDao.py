# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class HorarioDao:

    def getHorarios(self):

        horarioSQL = """
        SELECT id, descripcion
        FROM horarios
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(horarioSQL)
            horarios = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': horario[0], 'descripcion': horario[1]} for horario in horarios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los horarios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getHorarioById(self, id):

        horarioSQL = """
        SELECT id, descripcion
        FROM horarios WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(horarioSQL, (id,))
            horarioEncontrado = cur.fetchone() # Obtener una sola fila
            if horarioEncontrado:
                return {
                        "id": horarioEncontrado[0],
                        "descripcion": horarioEncontrado[1]
                    }  # Retornar los datos del horario
            else:
                return None # Retornar None si no se encuentra el horario
        except Exception as e:
            app.logger.error(f"Error al obtener horario: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarHorario(self, descripcion):

        insertHorarioSQL = """
        INSERT INTO horarios(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertHorarioSQL, (descripcion,))
            horario_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return horario_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar horario: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateHorario(self, id, descripcion):

        updateHorarioSQL = """
        UPDATE horarios
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateHorarioSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar horario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteHorario(self, id):

        deleteHorarioSQL = """
        DELETE FROM horarios
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteHorarioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar horario: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()