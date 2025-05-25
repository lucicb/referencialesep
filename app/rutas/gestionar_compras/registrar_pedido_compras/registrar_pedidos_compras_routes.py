from flask import Blueprint, render_template, jsonify
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.empleado.empleado_dao import EmpleadoDao
from app.dao.referenciales.producto.producto_dao import ProductoDao
from app.dao.referenciales.deposito.deposito_dao import DepositoDao  # Importar DepositoDao

# Crear el blueprint
pdcmod = Blueprint('pdcmod', __name__, template_folder='templates')

# Ruta al índice de pedidos
@pdcmod.route('/pedidos-index')
def pedidos_index():
    return render_template('pedidos-index.html')

# Ruta para mostrar el formulario de creación de pedidos
@pdcmod.route('/pedidos-agregar')
def pedidos_agregar():
    # Instanciar DAOs
    sdao = SucursalDao()
    empdao = EmpleadoDao()
    pdao = ProductoDao()

    # Obtener datos para los combos
    sucursales = sdao.get_sucursales()
    empleados = empdao.get_empleados()
    productos = pdao.get_productos()

    # Renderizar el formulario con los datos
    return render_template(
        'pedidos-agregar.html',
        sucursales=sucursales,
        empleados=empleados,
        productos=productos
    )
# En tu archivo de rutas (por ejemplo, deposito_routes.py o api_routes.py)
@pdcmod.route('/get_depositos', methods=['GET'])
def get_depositos():
    deposito_dao = DepositoDao()  # Accede a la base de datos y obtiene los depósitos
    depositos = deposito_dao.get_all_depositos()  # Método que obtiene todos los depósitos
    return jsonify({'depositos': depositos})  # Retorna los depósitos en formato JSON

        

