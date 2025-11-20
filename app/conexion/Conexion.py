import psycopg2

class Conexion:
    """Clase para gestionar la conexión a la base de datos PostgreSQL."""

    def __init__(self):
        try:
            # Parámetros de conexión a la base de datos
            dbname = "miBd"         # <-- Asegúrate que este nombre exista en PostgreSQL
            user = "postgres"       # <-- Usuario de tu base
            password = "1"          # <-- Contraseña del usuario (verifica que sea correcta)
            host = "localhost"      # <-- Dirección del servidor de PostgreSQL
            port = 5432             # <-- Puerto (5432 por defecto en PostgreSQL)

            # Establecer conexión
            self.con = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )

        except psycopg2.OperationalError as e:
            print(" Error de conexión a la base de datos:")
            print(str(e))
            self.con = None  # Opcional: establecer como None para evitar errores posteriores

    def getConexion(self):
        """Devuelve la conexión activa a la base de datos."""
        return self.con
