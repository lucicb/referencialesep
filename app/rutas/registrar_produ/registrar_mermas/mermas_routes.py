from flask import Blueprint, render_template, request
from app.dao.registrar_produ.registrar_mermas.mermas_dao import MermasDao
from app.dao.referenciales.producto.ProductoDao import ProductoDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao
from app.dao.registrar_produ.registrar_orden_produ.orden_produ_dao import OrdenProduccionDao

mermod = Blueprint('mermod', __name__, template_folder='templates')

# DAOs
dao = MermasDao()              # DAO de mermas
productoDao = ProductoDao()     
sucursalDao = SucursalDao()
loginDao = LoginDao()
ordenDao = OrdenProduccionDao() # Para obtener info de la orden de producción asociada

# ================================
# LISTADO HTML
# ================================
@mermod.route('/mermas')
def mermas_index():
    return render_template('registrar-mermas.html')

# ================================
# FORM – NUEVO O EDITAR MERMA
# ================================
@mermod.route('/mermas/form', defaults={'id': None})
@mermod.route('/mermas/form/<int:id>')
def mermas_form(id):

    # Obtener órdenes de producción (para seleccionar a cuál pertenece la merma)
    ordenes = ordenDao.obtener_ordenes()

    # Obtener productos
    productos = productoDao.get_productos()
    productos_dict = [p.to_dict() for p in productos]

    # Obtener sucursales
    sucursales = sucursalDao.get_sucursales()

    # Obtener todos los usuarios/funcionarios activos
    funcionarios = loginDao.get_usuarios()
    funcionarios_dict = [f for f in funcionarios]

    # Obtener merma si se pasa un ID
    merma = dao.obtener_por_id(id) if id else None

    return render_template(
        'registrar-mermas-form.html',
        ordenes=ordenes,
        productos=productos_dict,
        sucursales=sucursales,
        funcionarios=funcionarios_dict,
        merma=merma
    )
