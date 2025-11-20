from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.dao.registrar_produ.registrar_orden_produ.orden_produ_dao import OrdenProduccionDao
from app.dao.registrar_produ.registrar_orden_produ.dto.orden_produccion_cab_dto import OrdenProduccionCabDto
from app.dao.registrar_produ.registrar_orden_produ.dto.orden_produccion_det_dto import OrdenProduccionDetDto

opapi = Blueprint('opapi', __name__)
dao = OrdenProduccionDao()

# ===============================
# Endpoint para obtener CSRF token
# ===============================
@opapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200

# ============================================================
# LISTAR TODAS LAS ÓRDENES
# ============================================================
@opapi.route('', methods=['GET'])
def listar():
    try:
        ordenes = dao.obtener_ordenes()
        return jsonify(ordenes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# OBTENER UNA ORDEN POR ID
# ============================================================
@opapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        orden = dao.obtener_por_id(id)
        if orden:
            return jsonify(orden), 200
        else:
            return jsonify({"error": "Orden no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Función auxiliar para parsear fechas
# ============================================================
def parse_fecha(fecha_str, campo):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Formato de fecha inválido en {campo}, se espera YYYY-MM-DD")

# ============================================================
# CREAR O ACTUALIZAR UNA ORDEN DE PRODUCCIÓN
# ============================================================
@opapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # Validar campos obligatorios
        required_fields = ["id_producto", "id_suc", "usu_id", "detalle", "fecha_inicio", "fecha_fin_estimada"]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                return jsonify({"error": f"Falta campo obligatorio: {field}"}), 400

        # -----------------------------
        # DETALLE
        # -----------------------------
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            try:
                id_producto = int(d["id_producto"])
                cantidad = float(d["cantidad"])
                costo_unitario = float(d["costo_unitario"])
                detalle.append(OrdenProduccionDetDto(
                    id_producto=id_producto,
                    cantidad=cantidad,
                    costo_unitario=costo_unitario
                ))
            except (ValueError, KeyError) as ex:
                return jsonify({"error": f"Detalle inválido en la fila {idx+1}: {str(ex)}"}), 400

        if not detalle:
            return jsonify({"error": "Debe agregar al menos un detalle válido"}), 400

        # -----------------------------
        # CABECERA con validación de fechas
        # -----------------------------
        try:
            fecha_inicio = parse_fecha(data["fecha_inicio"], "fecha_inicio")
            fecha_fin_estimada = parse_fecha(data["fecha_fin_estimada"], "fecha_fin_estimada")

            cab = OrdenProduccionCabDto(
                fecha_inicio=fecha_inicio,
                fecha_fin_estimada=fecha_fin_estimada,
                id_producto=int(data["id_producto"]),
                id_suc=int(data["id_suc"]),
                usu_id=int(data["usu_id"]),
                detalle=detalle
            )
        except ValueError as ex:
            return jsonify({"error": f"Error en la cabecera: {str(ex)}"}), 400

        # Guardar en BD
        ok = dao.agregar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# ANULAR UNA ORDEN
# ============================================================
@opapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "ANULADO")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
