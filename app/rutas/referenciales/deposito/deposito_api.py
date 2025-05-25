# app/dao/referenciales/deposito/deposito_dao.py

from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:
    def __init__(self):
        # Aquí puedes configurar la conexión con la base de datos si es necesario.
        pass

    def get_depositos_por_sucursal(self, id_sucursal):
        sql = """
        SELECT
            d.id_deposito,
            d.nombre_deposito
        FROM
            depositos d
        WHERE
            d.id_sucursal = %s
        """
        # Usar el contexto 'with' para manejar la conexión y el cursor automáticamente
        try:
            conexion = Conexion()  # Asumimos que Conexion ya gestiona la conexión a la BD
            with conexion.getConexion() as con:  # Usamos 'with' para manejar la conexión
                with con.cursor() as cur:  # Usamos 'with' también para el cursor
                    cur.execute(sql, (id_sucursal,))
                    depositos = cur.fetchall()
                    
                    # Convertir el resultado en un diccionario
                    return [{'id_deposito': d[0], 'nombre_deposito': d[1]} for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener depósitos por sucursal {id_sucursal}: {str(e)}")
            return []  # Devolvemos una lista vacía en caso de error

