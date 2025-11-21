from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.dao.registrar_produ.registrar_mermas.mermas_dao import MermasDao
from app.dao.registrar_produ.registrar_mermas.dto.mermas_cab_dto import MermasCabDto
from app.dao.registrar_produ.registrar_mermas.dto.mermas_det_dto import MermasDetDto

merapi = Blueprint('merapi', __name__)
dao = MermasDao()

# ===============================
# Endpoint para obtener CSRF token
# ===============================
@merapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200

# ============================================================
# LISTAR TODAS LAS MERMAS
# ============================================================
@merapi.route('', methods=['GET'])
def listar():
    try:
        mermas = dao.obtener_mermas()
        return jsonify(mermas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# OBTENER UNA MERMA POR ID
# ============================================================
@merapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        merma = dao.obtener_por_id(id)
        if merma:
            return jsonify(merma), 200
        else:
            return jsonify({"error": "Merma no encontrada"}), 404
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
# CREAR O ACTUALIZAR MERMA
# ============================================================
@merapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # Validar campos obligatorios
        required_fields = ["cod_orden_prod_cab", "suc_id", "usu_id", "detalle", "fecha_registro", "responsable"]
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
                costo_unitario = float(d.get("costo_unitario", 0))
                motivo = d.get("motivo", "")
                detalle.append(MermasDetDto(
                    id_producto=id_producto,
                    cantidad=cantidad,
                    costo_unitario=costo_unitario,
                    motivo=motivo
                ))
            except (ValueError, KeyError) as ex:
                return jsonify({"error": f"Detalle inválido en la fila {idx+1}: {str(ex)}"}), 400

        if not detalle:
            return jsonify({"error": "Debe agregar al menos un detalle válido"}), 400

        # -----------------------------
        # CABECERA con validación de fecha
        # -----------------------------
        try:
            fecha_registro = parse_fecha(data["fecha_registro"], "fecha_registro")
            cab = MermasCabDto(
                cod_orden_prod_cab=int(data["cod_orden_prod_cab"]),
                suc_id=int(data["suc_id"]),
                usu_id=int(data["usu_id"]),
                fecha_registro=fecha_registro,
                responsable=data["responsable"],
                motivo_general=data.get("motivo_general", ""),
                observaciones=data.get("observaciones", ""),
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
# ANULAR UNA MERMA
# ============================================================
@merapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "ANULADO")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
