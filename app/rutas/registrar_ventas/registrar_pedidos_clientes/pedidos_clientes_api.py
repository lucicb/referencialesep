from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime

from app.dao.registrar_ventas.registrar_pedidos_clientes.pedidos_clientes_dao import PedidosClientesDao
from app.dao.registrar_ventas.registrar_pedidos_clientes.dto.pedidos_clientes_cab_dto import PedidosClientesCabDto
from app.dao.registrar_ventas.registrar_pedidos_clientes.dto.pedidos_clientes_det_dto import PedidosClientesDetDto

pedapi = Blueprint('pedapi', __name__, url_prefix='/api/v1/pedidos-clientes')
dao = PedidosClientesDao()

# ============================================================
# CSRF TOKEN
# ============================================================
@pedapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200


# ============================================================
# LISTAR TODOS LOS PEDIDOS
# ============================================================
@pedapi.route('', methods=['GET'])
def listar():
    try:
        pedidos = dao.obtener_pedidos()
        return jsonify(pedidos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# OBTENER PEDIDO POR ID
# ============================================================
@pedapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        pedido = dao.obtener_por_id(id)
        if pedido:
            return jsonify(pedido), 200
        return jsonify({"error": "Pedido no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# PARSE DE FECHAS
# ============================================================
def parse_fecha(fecha_str, campo):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Formato de fecha inválido en {campo}, se espera YYYY-MM-DD")


# ============================================================
# CREAR (O FUTURO ACTUALIZAR) PEDIDO CLIENTE
# ============================================================
@pedapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # ------------------------
        # Validar campos cabecera
        # ------------------------
        required_fields = ["id_cliente", "id_suc", "usu_id",
                           "fecha_pedido", "fecha_entrega", "detalle"]

        for f in required_fields:
            if f not in data or data[f] in ["", None]:
                return jsonify({"error": f"Falta campo obligatorio: {f}"}), 400

        # ------------------------
        # Parse DETALLE
        # ------------------------
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            try:
                det = PedidosClientesDetDto(
                    id_producto=str(d["id_producto"]),
                    cantidad=float(d["cantidad"]),
                    precio_unitario=float(d["precio_unitario"]),
                    observaciones=d.get("observaciones")
                )
                detalle.append(det)
            except Exception as ex:
                return jsonify({"error": f"Detalle inválido en fila {idx+1}: {str(ex)}"}), 400

        if not detalle:
            return jsonify({"error": "Debe agregar al menos un detalle válido"}), 400

        # ------------------------
        # Parse CABECERA
        # ------------------------
        try:
            fecha_pedido = parse_fecha(data["fecha_pedido"], "fecha_pedido")
            fecha_entrega = parse_fecha(data["fecha_entrega"], "fecha_entrega")

            cab = PedidosClientesCabDto(
                id_cliente=int(data["id_cliente"]),
                fecha_pedido=fecha_pedido,
                fecha_entrega=fecha_entrega,
                estado=data.get("estado", "PENDIENTE"),
                total=float(data.get("total", 0)),
                observaciones=data.get("observaciones"),
                usu_id=str(data["usu_id"]),
                id_suc=int(data["id_suc"]),
                detalle=detalle
            )
        except Exception as ex:
            return jsonify({"error": f"Error en cabecera: {str(ex)}"}), 400

        # ------------------------
        # GUARDAR EN BD
        # ------------------------
        ok = dao.agregar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ANULAR PEDIDO
# ============================================================
@pedapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "ANULADO")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
