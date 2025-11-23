from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.dao.registrar_produ.registrar_pedido_mp.pedido_mp_dao import PedidoMateriaPrimaDao
from app.dao.registrar_produ.registrar_pedido_mp.dto.pedido_mp_cab_dto import PedidoMpCabDto
from app.dao.registrar_produ.registrar_pedido_mp.dto.pedido_mp_det_dto import PedidoMpDetDto

pmpapi = Blueprint('pmpapi', __name__)
dao = PedidoMateriaPrimaDao()


# ===============================
# Endpoint para obtener CSRF token
# ===============================
@pmpapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200


# ===============================
# Función auxiliar para parsear fechas
# ===============================
def parse_fecha(fecha_str, campo):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):  # primero DD/MM/YYYY, luego YYYY-MM-DD
        try:
            return datetime.strptime(fecha_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido para {campo}. Se esperaba DD/MM/YYYY o YYYY-MM-DD, recibida: {fecha_str}")

# ============================================================
# CREAR UN NUEVO PEDIDO DE MATERIA PRIMA
# ============================================================
@pmpapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # ---------------------------------------------
        # Validar campos obligatorios del formulario
        # ---------------------------------------------
        required_fields = [
            "id_suc",
            "usu_id",
            "fecha_pedido",
            "fecha_entrega_estimada",
            "prioridad",
            "detalle"
        ]

        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                return jsonify({"error": f"Falta campo obligatorio: {field}"}), 400

        # ---------------------------------------------
        # Procesar DETALLE
        # ---------------------------------------------
        detalle = []
        for idx, d in enumerate(data["detalle"]):

            try:
                id_materia_prima = int(d["id_materia_prima"])
                cantidad = int(d["cantidad"])  # ahora es entero
                costo_unitario = int(d["costo_unitario"])  # entero también

                detalle.append(PedidoMpDetDto(
                    id_materia_prima=id_materia_prima,
                    cantidad=cantidad,
                    costo_unitario=costo_unitario
                ))

            except Exception as ex:
                return jsonify({
                    "error": f"Detalle inválido en fila {idx+1}: {str(ex)}"
                }), 400

        if not detalle:
            return jsonify({"error": "Debe incluir al menos un item en el detalle"}), 400

        # ---------------------------------------------
        # CABECERA
        # ---------------------------------------------
        fecha_pedido = parse_fecha(data["fecha_pedido"], "fecha_pedido")
        fecha_entrega_estimada = parse_fecha(data["fecha_entrega_estimada"], "fecha_entrega_estimada")

        cab = PedidoMpCabDto(
            id_suc=int(data["id_suc"]),
            usu_id=int(data["usu_id"]),
            fecha_pedido=fecha_pedido,
            fecha_entrega_estimada=fecha_entrega_estimada,
            prioridad=data["prioridad"],
            observaciones=data.get("observaciones", ""),
            detalle=detalle
        )

        # Guardar en la BD
        ok = dao.agregar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# LISTAR
# ============================================================
@pmpapi.route('', methods=['GET'])
def listar():
    try:
        pedidos = dao.obtener_pedidos()
        return jsonify(pedidos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# OBTENER UN PEDIDO
# ============================================================
@pmpapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        pedido = dao.obtener_por_id(id)
        if pedido:
            return jsonify(pedido), 200
        return jsonify({"error": "Pedido no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ANULAR UN PEDIDO
# ============================================================
@pmpapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "ANULADO")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
