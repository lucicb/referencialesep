from flask import Blueprint, render_template, request
from app.dao.registrar_produ.registrar_orden_produ.orden_produ_dao import OrdenProduccionDao
from app.dao.referenciales.producto.ProductoDao import ProductoDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao

opmod = Blueprint('opmod', __name__, template_folder='templates')

# DAOs
dao = OrdenProduccionDao()
productoDao = ProductoDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()  # <-- LoginDao para traer funcionarios

# ================================
# LISTADO HTML
# ================================
@opmod.route('/orden')
def orden_produccion_index():
    return render_template('orden-produccion.html')

# ================================
# FORM – NUEVO O EDITAR
# ================================
@opmod.route('/orden/form', defaults={'id': None})
@opmod.route('/orden/form/<int:id>')
def orden_produccion_form(id):

    # Obtener productos
    productos = productoDao.get_productos()
    productos_dict = [p.to_dict() for p in productos]

    # Obtener sucursales
    sucursales = sucursalDao.get_sucursales()

    # Obtener todos los usuarios/funcionarios activos
    # Aquí suponemos que existe un método que traiga todos los usuarios
    # Si LoginDao no tiene, podemos crear uno: get_usuarios()
    funcionarios = loginDao.get_usuarios()  # <-- Método que retorna lista de diccionarios
    funcionarios_dict = [f for f in funcionarios]  # Ya vienen como diccionarios

    # Obtener orden si se pasa un ID
    orden = dao.obtener_por_id(id) if id else None

    return render_template(
        'orden-produccion-form.html',
        productos=productos_dict,
        sucursales=sucursales,
        funcionarios=funcionarios_dict,  # enviamos todos los funcionarios
        orden=orden
    )
