from flask import current_app as app
from app.conexion.Conexion import Conexion

class SucursalDao:

    def getSucursales(self):

        sucursalSQL = """
        SELECT id, descripcion
        FROM sucursales
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sucursalSQL)
            sucursales = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': sucursal[0], 'descripcion': sucursal[1]} for sucursal in sucursales]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las sucursales: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getSucursalById(self, id):

        sucursalSQL = """
        SELECT id, descripcion
        FROM sucursales WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sucursalSQL, (id,))
            sucursalEncontrada = cur.fetchone()  # Obtener una sola fila
            if sucursalEncontrada:
                return {
                        "id": sucursalEncontrada[0],
                        "descripcion": sucursalEncontrada[1]
                    }  # Retornar los datos de la sucursal
            else:
                return None  # Retornar None si no se encuentra la sucursal
        except Exception as e:
            app.logger.error(f"Error al obtener sucursal: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarSucursal(self, descripcion):

        insertSucursalSQL = """
        INSERT INTO sucursales(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertSucursalSQL, (descripcion,))
            sucursal_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return sucursal_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar sucursal: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateSucursal(self, id, descripcion):

        updateSucursalSQL = """
        UPDATE sucursales
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSucursalSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar sucursal: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteSucursal(self, id):

        deleteSucursalSQL = """
        DELETE FROM sucursales
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSucursalSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar sucursal: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()