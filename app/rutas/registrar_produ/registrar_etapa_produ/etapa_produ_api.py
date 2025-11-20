from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.dao.registrar_produ.registrar_etapa_produ.etapa_produ_dao import EtapaProduDao
from app.dao.registrar_produ.registrar_etapa_produ.dto.etapa_produ_cab_dto import EtapaProduCabDto
from app.dao.registrar_produ.registrar_etapa_produ.dto.etapa_produ_det_dto import EtapaProduDetDto

epapi = Blueprint('epapi', __name__)
dao = EtapaProduDao()

# ===============================
# Endpoint para obtener CSRF token
# ===============================
@epapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200

# ============================================================
# LISTAR TODAS LAS ETAPAS
# ============================================================
@epapi.route('', methods=['GET'])
def listar():
    try:
        etapas = dao.obtener_etapas()
        return jsonify(etapas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# OBTENER UNA ETAPA POR ID
# ============================================================
@epapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        etapa = dao.obtener_por_id(id)
        if etapa:
            return jsonify(etapa), 200
        else:
            return jsonify({"error": "Etapa no encontrada"}), 404
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
# CREAR O ACTUALIZAR UNA ETAPA DE PRODUCCIÓN
# ============================================================
@epapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # Validar campos obligatorios de cabecera
        required_fields = ["cod_orden_prod_cab", "id_producto", "id_suc", "usu_id", "estado", "fecha", "detalle"]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                return jsonify({"error": f"Falta campo obligatorio: {field}"}), 400

        # -----------------------------
        # DETALLE
        # -----------------------------
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            try:
                etapa = d["etapa"]
                descripcion = d["descripcion"]
                responsable = d["responsable"]
                fecha_inicio = datetime.strptime(d["fecha_inicio"], "%Y-%m-%d") if d.get("fecha_inicio") else None
                fecha_fin = datetime.strptime(d["fecha_fin"], "%Y-%m-%d") if d.get("fecha_fin") else None
                estado = d["estado"]
                avance = d["avance"]

                detalle.append(EtapaProduDetDto(
                    etapa=etapa,
                    descripcion=descripcion,
                    responsable=responsable,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    estado=estado,
                    avance=avance
                ))
            except (ValueError, KeyError) as ex:
                return jsonify({"error": f"Detalle inválido en la fila {idx+1}: {str(ex)}"}), 400

        if not detalle:
            return jsonify({"error": "Debe agregar al menos un detalle válido"}), 400

        # -----------------------------
        # CABECERA con validación de fecha
        # -----------------------------
        try:
            fecha = parse_fecha(data["fecha"], "fecha")

            cab = EtapaProduCabDto(
                cod_orden_prod_cab=int(data["cod_orden_prod_cab"]),
                fecha=fecha,
                id_producto=int(data["id_producto"]),
                id_suc=int(data["id_suc"]),
                usu_id=int(data["usu_id"]),
                cantidad_planificada=float(data.get("cantidad_planificada", 0)),
                estado=data["estado"],
                observaciones=data.get("observaciones", ""),
                fecha_inicio=datetime.strptime(data.get("fecha_inicio"), "%Y-%m-%d") if data.get("fecha_inicio") else None,
                fecha_fin=datetime.strptime(data.get("fecha_fin"), "%Y-%m-%d") if data.get("fecha_fin") else None,
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
# ANULAR UNA ETAPA
# ============================================================
@epapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "ANULADO")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
