from flask import Blueprint, render_template, request
from app.dao.registrar_ventas.registrar_pedidos_clientes.pedidos_clientes_dao import PedidosClientesDao
from app.dao.referenciales.producto.ProductoDao import ProductoDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao
from app.conexion.Conexion import Conexion

pedmod = Blueprint('pedmod', __name__, template_folder='templates')

# DAOs
dao = PedidosClientesDao()
productoDao = ProductoDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()


# ================================
# LISTADO HTML
# ================================
@pedmod.route('/pedidos')
def pedidos_index():
    return render_template('pedidos-clientes.html')


# ================================
# FORM – NUEVO O EDITAR
# ================================
@pedmod.route('/pedidos/form', defaults={'id': None})
@pedmod.route('/pedidos/form/<int:id>')
def pedidos_form(id):

    # Productos
    productos = productoDao.get_productos()
    productos_dict = [p.to_dict() if hasattr(p, 'to_dict') else p for p in productos]

    # Sucursales
    sucursales = sucursalDao.get_sucursales()

    # Funcionarios
    funcionarios = loginDao.get_usuarios()  # retorna lista de diccionarios
    funcionarios_dict = [f for f in funcionarios]  # ya son dicts, no necesitamos to_dict()

    # Clientes desde la base usando tu conexión
    conn = Conexion().getConexion()
    clientes_dict = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT id_cliente, nombre, apellido, ci FROM clientes WHERE estado='activo' ORDER BY nombre")
        rows = cur.fetchall()
        for r in rows:
            clientes_dict.append({
                "id_cliente": r[0],
                "nombre": f"{r[1]} {r[2]}",
                "ci": r[3]
            })
        cur.close()
        conn.close()

    # Pedido si es edición
    pedido = dao.obtener_por_id(id) if id else None

    return render_template(
        'pedidos-clientes-form.html',
        productos=productos_dict,
        sucursales=sucursales,
        funcionarios=funcionarios_dict,
        clientes=clientes_dict,
        pedido=pedido
    )
