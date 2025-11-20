# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class LoginDao:

    def buscarUsuario(self, usu_nick: str):
        buscar_usuario_sql = """
        SELECT
            u.usu_id,
            TRIM(u.usu_nick) AS nick,
            u.usu_clave,
            u.usu_nro_intentos,
            u.fun_id,
            u.gru_id,
            u.usu_estado,
            CONCAT(p.nombre, ' ', p.apellido) AS nombre_persona,
            g.gru_des AS grupo
        FROM usuarios u
        LEFT JOIN personas p ON p.id = u.fun_id
        LEFT JOIN grupos g ON g.gru_id = u.gru_id
        WHERE u.usu_nick = %s AND u.usu_estado IS TRUE
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(buscar_usuario_sql, (usu_nick,))
            usuario_encontrado = cur.fetchone()
            if usuario_encontrado:
                return {
                    "usu_id": usuario_encontrado[0],
                    "usu_nick": usuario_encontrado[1],
                    "usu_clave": usuario_encontrado[2],
                    "usu_nro_intentos": usuario_encontrado[3],
                    "fun_id": usuario_encontrado[4],
                    "gru_id": usuario_encontrado[5],
                    "usu_estado": usuario_encontrado[6],
                    "nombre_persona": usuario_encontrado[7],
                    "grupo": usuario_encontrado[8]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener usuario: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # =============================================================
    # NUEVO MÉTODO PARA LISTAR TODOS LOS FUNCIONARIOS ACTIVOS
    # =============================================================
    def get_usuarios(self):
        sql = """
        SELECT
            u.usu_id,
            TRIM(u.usu_nick) AS usu_nick,
            u.fun_id,
            CONCAT(p.nombre, ' ', p.apellido) AS nombre_persona
        FROM usuarios u
        LEFT JOIN personas p ON p.id = u.fun_id
        WHERE u.usu_estado IS TRUE
        ORDER BY nombre_persona
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            filas = cur.fetchall()
            return [
                {
                    "usu_id": f[0],
                    "usu_nick": f[1],
                    "fun_id": f[2],
                    "nombre_persona": f[3]
                } for f in filas
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener funcionarios: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
