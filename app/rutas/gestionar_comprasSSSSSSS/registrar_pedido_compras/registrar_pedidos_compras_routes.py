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
    depodao = DepositoDao()

    # Obtener datos para los combos
    sucursales = sdao.get_sucursales()
    empleados = empdao.get_empleados()
    productos = pdao.get_productos()
    depositos = depodao.get_depositos()

    # Renderizar el formulario con los datos
    return render_template(
        'pedidos-agregar.html',
        sucursales=sucursales,
        empleados=empleados,
        productos=productos,
        depositos=depositos
    )
 

        

