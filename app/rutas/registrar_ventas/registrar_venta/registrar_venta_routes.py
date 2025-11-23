from flask import Blueprint, render_template
from datetime import datetime

# DAOs
from app.dao.registrar_ventas.registrar_venta.registrar_venta_dao import RegistrarVentaDao
from app.dao.referenciales.producto.ProductoDao import ProductoDao
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.usuario.login_dao import LoginDao
from app.conexion.Conexion import Conexion

venta_mod = Blueprint('venta_mod', __name__, template_folder='templates')

# Instancias DAO
ventaDao = RegistrarVentaDao()
sucursalDao = SucursalDao()
loginDao = LoginDao()
productoDao = ProductoDao()


# ===================================
#   LISTADO DE VENTAS
# ===================================
@venta_mod.route('/ventas')
def ventas_index():
    conn = Conexion().getConexion()
    ventas = ventaDao.listar_cabecera()
    
    # Obtener nombres de clientes y sucursales
    ventas_completas = []
    for v in ventas:
        venta_dict = v.to_dict()
        
        # Obtener nombre del cliente
        cur = conn.cursor()
        cur.execute("SELECT nombre, apellido FROM clientes WHERE id_cliente = %s", (v.id_cliente,))
        cliente = cur.fetchone()
        venta_dict['cliente_nombre'] = f"{cliente[0]} {cliente[1]}" if cliente else "N/A"
        
        # Obtener nombre de la sucursal
        cur.execute("SELECT descripcion FROM sucursales WHERE id = %s", (v.id_suc,))
        sucursal = cur.fetchone()
        venta_dict['sucursal_descripcion'] = sucursal[0] if sucursal else "N/A"
        
        ventas_completas.append(venta_dict)
        cur.close()
    
    conn.close()
    
    return render_template(
        'registrar-venta.html',
        ventas=ventas_completas
    )


# ===================================
#   FORM NUEVO / EDITAR
# ===================================
@venta_mod.route('/ventas/form', defaults={'id': None})
@venta_mod.route('/ventas/form/<int:id>')
def ventas_form(id):

    # ============================
    # Clientes (consulta directa)
    # ============================
    conn = Conexion().getConexion()
    clientes_dict = []

    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id_cliente, nombre, apellido, ci
            FROM clientes
            WHERE estado = 'activo'
            ORDER BY nombre
        """)
        rows = cur.fetchall()
        for r in rows:
            clientes_dict.append({
                "id_cliente": r[0],
                "nombre": f"{r[1]} {r[2]}",
                "ci": r[3]
            })
        cur.close()
        conn.close()

    # ============================
    # Sucursales
    # ============================
    sucursales = sucursalDao.get_sucursales()
    sucursales_dict = [s for s in sucursales]

    # ============================
    # Usuarios
    # ============================
    usuarios = loginDao.get_usuarios()
    usuarios_dict = [u for u in usuarios]

    # ============================
    # Productos
    # ============================
    productos = productoDao.get_productos()
    productos_dict = [p.to_dict() if hasattr(p, "to_dict") else p for p in productos]

    # ============================
    # Venta si es EDICIÓN
    # ============================
    venta = ventaDao.obtener_venta_cab(id) if id else None

    # Detalle (solo si existe)
    detalle = []
    if venta:
        detalle_items = ventaDao.obtener_detalle(id)
        detalle = [d.to_dict() for d in detalle_items]

    return render_template(
        'registrar-venta-form.html',
        clientes=clientes_dict,
        sucursales=sucursales_dict,
        usuarios=usuarios_dict,
        productos=productos_dict,
        venta=venta,
        detalle=detalle,
        fecha_hoy=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
