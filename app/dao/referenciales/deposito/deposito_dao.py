# app/dao/referenciales/deposito/deposito_dao.py

from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:
    def __init__(self):
        # Configurar conexión a la base de datos
        pass

    def get_all_depositos(self):
        sql = """
        SELECT id_deposito, nombre_deposito
        FROM depositos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            depositos = cur.fetchall()
            return [{'id_deposito': d[0], 'nombre_deposito': d[1]} for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener los depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


