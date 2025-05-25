from flask import current_app as app
from app.conexion.Conexion import Conexion

class EmpleadoDao:

    def get_empleados(self):
        """
        Devuelve una lista de empleados con su ID, nombre completo y teléfono.
        """
        emp_sql = """
        SELECT
            e.id_empleado,
            CONCAT(p.nombre, ' ', p.apellido) AS empleado,
            p.telefono
        FROM empleados e
        LEFT JOIN personas p ON e.id_persona = p.id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(emp_sql)
            empleados = cur.fetchall()
            return [
                {
                    'id_empleado': emp[0],
                    'empleado': emp[1],
                    'telefono': emp[2]
                }
                for emp in empleados
            ]

        except Exception as e:
            app.logger.error(f"Error al obtener empleados: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    # Las siguientes funciones están relacionadas a ciudades. Recomendado moverlas a CiudadDao.
    def getCiudadById(self, id):
        ciudadSQL = """
        SELECT id, descripcion
        FROM ciudades
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(ciudadSQL, (id,))
            ciudad = cur.fetchone()
            if ciudad:
                return {"id": ciudad[0], "descripcion": ciudad[1]}
            return None

        except Exception as e:
            app.logger.error(f"Error al obtener ciudad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCiudad(self, descripcion):
        insert_sql = """
        INSERT INTO ciudades (descripcion) VALUES (%s)
        RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insert_sql, (descripcion,))
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
        update_sql = """
        UPDATE ciudades
        SET descripcion = %s
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(update_sql, (descripcion, id))
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
        delete_sql = """
        DELETE FROM ciudades
        WHERE id = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(delete_sql, (id,))
            con.commit()
            return cur.rowcount > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar ciudad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
