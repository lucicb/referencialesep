# deposito_dao.py
class DepositoDao:
    def __init__(self):
        # Configuración de la conexión, etc.
        pass

    def get_all_depositos(self):
        sql = """
        SELECT
            d.id_deposito,
            d.nombre_deposito
        FROM
            depositos d
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            depositos = cur.fetchall()
            return [{'id_deposito': d[0], 'nombre_deposito': d[1]} for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

