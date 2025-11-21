from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime

from app.dao.registrar_produ.registrar_control_calidad.control_calidad_dao import ControlCalidadDao
from app.dao.registrar_produ.registrar_control_calidad.dto.control_calidad_cab_dto import ControlCalidadCabDto
from app.dao.registrar_produ.registrar_control_calidad.dto.control_calidad_det_dto import ControlCalidadDetDto

ccapi = Blueprint('ccapi', __name__)
dao = ControlCalidadDao()

# ===============================
# Obtener CSRF token
# ===============================
@ccapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200


# ===============================
# LISTAR TODOS
# ===============================
@ccapi.route('', methods=['GET'])
def listar():
    try:
        datos = dao.obtener_todos()
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# OBTENER POR ID
# ===============================
@ccapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        dato = dao.obtener_por_id(id)
        if dato:
            return jsonify(dato), 200
        else:
            return jsonify({"error": "Registro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# Validar y convertir fecha
# ===============================
def parse_fecha(fecha_str, campo):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
    except:
        raise ValueError(f"Formato inválido en {campo}. Use YYYY-MM-DD HH:MM")


# ===============================
# CREAR REGISTRO
# ===============================
@ccapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # =======================
        # VALIDAR CAMPOS
        # =======================
        required = ["cod_orden_prod_cab", "fecha_control", "responsable", "resultado", "estado", "usu_id"]
        for r in required:
            if r not in data or data[r] in ["", None]:
                return jsonify({"error": f"Falta campo obligatorio: {r}"}), 400

        # =======================
        # DETALLE
        # =======================
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            try:
                det = ControlCalidadDetDto(
                    valor_esperado=d["valor_esperado"],
                    valor_obtenido=d["valor_obtenido"],
                    resultado=d["resultado"],
                    observaciones=d.get("observaciones", "")
                )
                detalle.append(det)
            except Exception as ex:
                return jsonify({"error": f"Detalle inválido en fila {idx+1}: {ex}"}), 400

        # =======================
        # CABECERA
        # =======================
        fecha_control = data["fecha_control"]

        cab = ControlCalidadCabDto(
            cod_orden_prod_cab=int(data["cod_orden_prod_cab"]),
            fecha_control=fecha_control,
            responsable=data["responsable"],
            resultado=data["resultado"],
            observaciones=data.get("observaciones", ""),
            estado=data["estado"],
            usu_id=int(data["usu_id"]),
            detalle=detalle
        )

        ok = dao.agregar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# ACTUALIZAR REGISTRO
# ===============================
@ccapi.route('/<int:id>', methods=['PUT'])
def actualizar(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # Validar
        required = ["cod_orden_prod_cab", "fecha_control", "responsable", "resultado", "estado", "usu_id"]
        for r in required:
            if r not in data or data[r] in ["", None]:
                return jsonify({"error": f"Falta campo obligatorio: {r}"}), 400

        # Detalle
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            det = ControlCalidadDetDto(
                valor_esperado=d["valor_esperado"],
                valor_obtenido=d["valor_obtenido"],
                resultado=d["resultado"],
                observaciones=d.get("observaciones", ""),
                id_cali_det=d.get("id_cali_det")
            )
            detalle.append(det)

        cab = ControlCalidadCabDto(
            cod_orden_prod_cab=int(data["cod_orden_prod_cab"]),
            fecha_control=data["fecha_control"],
            responsable=data["responsable"],
            resultado=data["resultado"],
            observaciones=data.get("observaciones", ""),
            estado=data["estado"],
            usu_id=int(data["usu_id"]),
            detalle=detalle,
            id_cali_cab=id
        )

        ok = dao.actualizar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===============================
# ELIMINAR
# ===============================
@ccapi.route('/<int:id>', methods=['DELETE'])
def eliminar(id):
    try:
        ok = dao.eliminar(id)
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
