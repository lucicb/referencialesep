from flask import Blueprint, render_template
from app.dao.registrar_produ.registrar_etapa_produ.etapa_produ_dao import EtapaProduDao
from app.dao.registrar_produ.registrar_orden_produ.orden_produ_dao import OrdenProduccionDao
from app.dao.referenciales.producto.ProductoDao import ProductoDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao

epmod = Blueprint('epmod', __name__, template_folder='templates')

# DAOs
dao = EtapaProduDao()
ordenDao = OrdenProduccionDao()  # <-- NECESARIO PARA LISTAR ORDENES PRODU
productoDao = ProductoDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()  # Para traer funcionarios

# ================================
# LISTADO HTML
# ================================
@epmod.route('/etapa')
def etapa_produccion_index():
    return render_template('etapa-produ.html')

# ================================
# FORM – NUEVO O EDITAR
# ================================
@epmod.route('/etapa/form', defaults={'id': None})
@epmod.route('/etapa/form/<int:id>')
def etapa_produccion_form(id):

    # Obtener productos
    productos = productoDao.get_productos()
    productos_dict = [p.to_dict() for p in productos]

    # Obtener sucursales
    sucursales = sucursalDao.get_sucursales()

    # Obtener funcionarios
    funcionarios = loginDao.get_usuarios()
    funcionarios_dict = [f for f in funcionarios]

    # Obtener etapa si existe
    etapa = dao.obtener_por_id(id) if id else None

    # 🔥 **ESTO FALTABA**: lista de órdenes para cargar en el formulario
    ordenes_produccion = ordenDao.obtener_ordenes()

    return render_template(
        'etapa-produ-form.html',
        productos=productos_dict,
        sucursales=sucursales,
        funcionarios=funcionarios_dict,
        etapa=etapa,
        ordenes_produccion=ordenes_produccion  # <-- AGREGADO
    )
