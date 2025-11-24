from flask import Blueprint, render_template
from datetime import datetime
import os

from app.dao.registrar_ventas.registrar_apertura_cierre.apertura_cierre_dao import AperturaCierreDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao

# Obtener la ruta absoluta de la carpeta templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

apcmod = Blueprint('apcmod', __name__, template_folder=template_dir)

# DAOs
dao = AperturaCierreDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()


# ================================
# LISTADO HTML
# ================================
@apcmod.route('')
def apertura_cierre_index():
    try:
        aperturas = dao.listar_aperturas()
        aperturas_list = [a.to_dict() for a in aperturas]
        
        return render_template('apertura-cierre.html', aperturas=aperturas_list)
    except Exception as e:
        print(f"Error en apertura_cierre_index: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500


# ================================
# FORM – NUEVO O EDITAR
# ================================
@apcmod.route('/form', defaults={'id': None})
@apcmod.route('/form/<int:id>')
def apertura_cierre_form(id):
    try:
        # Sucursales
        sucursales = sucursalDao.get_sucursales()
        sucursales_dict = [s for s in sucursales]

        # Funcionarios
        funcionarios = loginDao.get_usuarios()
        funcionarios_dict = [f for f in funcionarios]

        # Apertura/Cierre si es edición
        apertura = None
        if id:
            apertura_dto = dao.obtener_por_id(id)
            apertura = apertura_dto.to_dict() if apertura_dto else None

        # Fecha actual
        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Próximo ID (para mostrar)
        proximo_id = "AUTO"

        print(f"Template folder: {template_dir}")
        print(f"Buscando: apertura-cierre-form.html")

        return render_template(
            'apertura-cierre-form.html',
            sucursales=sucursales_dict,
            funcionarios=funcionarios_dict,
            apertura=apertura,
            fecha_hoy=fecha_hoy,
            proximo_id=proximo_id
        )
    except Exception as e:
        print(f"Error en apertura_cierre_form: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500