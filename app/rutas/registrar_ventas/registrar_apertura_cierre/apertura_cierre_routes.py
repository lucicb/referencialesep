from flask import Blueprint, render_template, request
from datetime import datetime

from app.dao.registrar_ventas.registrar_apertura_cierre.apertura_cierre_dao import AperturaCierreDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao

apcmod = Blueprint('apcmod', __name__, template_folder='templates')

# DAOs
dao = AperturaCierreDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()


# ================================
# LISTADO HTML
# ================================
@apcmod.route('/apertura-cierre')
def apertura_cierre_index():
    # Obtener todas las aperturas de caja
    aperturas = dao.listar_aperturas()
    # Convertir cada apertura a diccionario con datos listos para la tabla
    aperturas_list = []
    for a in aperturas:
        aperturas_list.append({
            "id_caja_cab": a["id_caja_cab"],
            "sucursal": a["id_suc"],  # opcional: reemplazar con nombre si quieres
            "usu_id": a["usu_id"],    # opcional: reemplazar con nombre de usuario
            "fecha_apertura": a["fecha_apertura"].strftime("%d/%m/%Y %H:%M") if a["fecha_apertura"] else "-",
            "fecha_cierre": a["fecha_cierre"].strftime("%d/%m/%Y %H:%M") if a["fecha_cierre"] else None,
            "estado": a["estado"]
        })
    return render_template('apertura-cierre.html', aperturas=aperturas_list)


# ================================
# FORM – NUEVO O EDITAR
# ================================
@apcmod.route('/apertura-cierre/form', defaults={'id': None})
@apcmod.route('/apertura-cierre/form/<int:id>')
def apertura_cierre_form(id):
    # ===============================
    # SUCURSALES
    # ===============================
    sucursales = sucursalDao.get_sucursales()
    sucursales_dict = [s for s in sucursales]

    # ===============================
    # FUNCIONARIOS
    # ===============================
    funcionarios = loginDao.get_usuarios()
    funcionarios_dict = [f for f in funcionarios]

    # ===============================
    # APERTURA/CIERRE SI ES EDICIÓN
    # ===============================
    apertura = dao.obtener_por_id(id) if id else None
    # Indicar si es apertura o cierre
    es_cierre = apertura and apertura["estado"] == "ABIERTO"

    return render_template(
        'apertura-cierre-form.html',
        sucursales=sucursales_dict,
        funcionarios=funcionarios_dict,
        apertura=apertura,
        es_cierre=es_cierre
    )
