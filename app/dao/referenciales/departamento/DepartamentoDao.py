# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepartamentoDao:

    def getDepartamentos(self):

        departamentoSQL = """
        SELECT id, descripcion
        FROM departamentos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(departamentoSQL)
            departamentos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': departamento[0], 'descripcion': departamento[1]} for departamento in departamentos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los departamentos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDepartamentoById(self, id):

        departamentoSQL = """
        SELECT id, descripcion
        FROM departamentos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(departamentoSQL, (id,))
            departamentoEncontrado = cur.fetchone()  # Obtener una sola fila
            if departamentoEncontrado:
                return {
                    "id": departamentoEncontrado[0],
                    "descripcion": departamentoEncontrado[1]
                }  # Retornar los datos del departamento
            else:
                return None  # Retornar None si no se encuentra el departamento
        except Exception as e:
            app.logger.error(f"Error al obtener departamento: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDepartamento(self, descripcion):

        insertDepartamentoSQL = """
        INSERT INTO departamentos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDepartamentoSQL, (descripcion,))
            departamento_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return departamento_id

        # Si algo fallo entra aquí
        except Exception as e:
            app.logger.error(f"Error al insertar departamento: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va a ejecutar
        finally:
            cur.close()
            con.close()

    def updateDepartamento(self, id, descripcion):

        updateDepartamentoSQL = """
        UPDATE departamentos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDepartamentoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar departamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDepartamento(self, id):

        deleteDepartamentoSQL = """
        DELETE FROM departamentos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDepartamentoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar departamento: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()