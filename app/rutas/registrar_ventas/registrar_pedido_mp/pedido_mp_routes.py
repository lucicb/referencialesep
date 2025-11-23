from flask import Blueprint, render_template
from app.dao.registrar_produ.registrar_pedido_mp.pedido_mp_dao import PedidoMateriaPrimaDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao
from app.conexion.Conexion import Conexion

pmpmod = Blueprint('pmpmod', __name__, template_folder='templates')

# DAOs
pedidoDao = PedidoMateriaPrimaDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()

# ================================
# LISTADO HTML
# ================================
@pmpmod.route('/pedido-mp')
def pedido_mp_index():
    return render_template('pedido-mp.html')

# ================================
# FORM – NUEVO O EDITAR
# ================================
@pmpmod.route('/pedido-mp/form', defaults={'id': None})
@pmpmod.route('/pedido-mp/form/<int:id>')
def pedido_mp_form(id):

    # Obtener materias primas directamente desde la tabla
    materias_primas = []
    try:
        with Conexion().getConexion() as con:
            with con.cursor() as cur:
                cur.execute("SELECT id_materia_prima, descripcion FROM materia_prima ORDER BY descripcion")
                filas = cur.fetchall()
                for f in filas:
                    materias_primas.append({
                        "id_materia_prima": f[0],
                        "descripcion": f[1]
                    })
    except Exception as e:
        print(f"Error al obtener materias primas: {e}")

    # Obtener sucursales
    sucursales = sucursalDao.get_sucursales()

    # Obtener todos los usuarios/funcionarios activos
    funcionarios = loginDao.get_usuarios()
    
    # Obtener pedido si se pasa un ID
    pedido = pedidoDao.obtener_por_id(id) if id else None

    return render_template(
        'pedido-mp-form.html',
        materias_primas=materias_primas,
        sucursales=sucursales,
        funcionarios=funcionarios,
        pedido=pedido
    )
