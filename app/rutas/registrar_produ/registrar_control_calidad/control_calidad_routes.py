from flask import Blueprint, render_template
from app.dao.registrar_produ.registrar_control_calidad.control_calidad_dao import ControlCalidadDao
from app.dao.registrar_produ.registrar_orden_produ.orden_produ_dao import OrdenProduccionDao
from app.dao.referenciales.usuario.login_dao import LoginDao

ccmod = Blueprint('ccmod', __name__, template_folder='templates')

# DAOs
ccDao = ControlCalidadDao()
ordenDao = OrdenProduccionDao()
loginDao = LoginDao()


# ================================
# LISTADO HTML
# ================================
@ccmod.route('/control-calidad')
def control_calidad_index():
    """
    Muestra la grilla con todos los controles de calidad.
    """
    return render_template('control-calidad.html')


# ================================
# FORM HTML - NUEVO O EDITAR
# ================================
@ccmod.route('/control-calidad/form', defaults={'id': None})
@ccmod.route('/control-calidad/form/<int:id>')
def control_calidad_form(id):
    """
    Muestra el formulario para cargar o editar un control de calidad.
    """

    # =======================
    # 1. Ordenes de Producción
    # =======================
    ordenes = ordenDao.obtener_ordenes()  # lista de diccionarios
    # No convertimos porque este método ya retorna JSON friendly

    # =======================
    # 2. Usuarios / Funcionarios
    # =======================
    funcionarios = loginDao.get_usuarios()
    funcionarios_dict = [f for f in funcionarios]  # ya es dict

    # =======================
    # 3. Obtener el registro si se está en edición
    # =======================
    control = ccDao.obtener_por_id(id) if id else None

    return render_template(
        'control-calidad-form.html',
        ordenes=ordenes,
        funcionarios=funcionarios_dict,
        control=control
    )
