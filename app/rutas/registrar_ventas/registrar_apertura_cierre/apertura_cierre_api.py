from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf
from datetime import datetime

from app.dao.registrar_ventas.registrar_apertura_cierre.apertura_cierre_dao import AperturaCierreDao
from app.dao.registrar_ventas.registrar_apertura_cierre.dto.apertura_cierre_cab_dto import AperturaCierreCabDto
from app.dao.registrar_ventas.registrar_apertura_cierre.dto.apertura_cierre_det_dto import AperturaCierreDetDto

apcapi = Blueprint('apcapi', __name__)
dao = AperturaCierreDao()


# ===============================
# CSRF TOKEN
# ===============================
@apcapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token}), 200


# ============================================================
# LISTAR TODAS LAS APERTURAS DE CAJA
# ============================================================
@apcapi.route('', methods=['GET'])
def listar():
    try:
        aperturas = dao.obtener_aperturas()
        return jsonify(aperturas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# OBTENER UNA APERTURA POR ID
# ============================================================
@apcapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        apertura = dao.obtener_por_id(id)
        if apertura:
            return jsonify(apertura), 200
        else:
            return jsonify({"error": "Apertura no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# FUNCION AUXILIAR: PARSEAR FECHA Y FECHA-HORA
# ============================================================
def parse_fecha_hora(fecha_str, campo):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValueError(f"Formato inválido en {campo}, se espera YYYY-MM-DDTHH:MM")


# ============================================================
# CREAR O ACTUALIZAR APERTURA/CERRAR CAJA
# ============================================================
@apcapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibió data"}), 400

        # -----------------------------
        # CAMPOS OBLIGATORIOS
        # -----------------------------
        required_fields = ["id_suc", "usu_id", "fecha_apertura", "monto_inicial", "detalle"]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                return jsonify({"error": f"Falta campo obligatorio: {field}"}), 400

        # -----------------------------
        # PARSE DETALLE
        # -----------------------------
        detalle = []
        for idx, d in enumerate(data.get("detalle", [])):
            try:
                tipo = d["tipo"]
                concepto = d["concepto"]
                monto = float(d["monto"])
                fecha_mov = parse_fecha_hora(d["fecha_mov"], "fecha_mov")
                usu_id_mov = d.get("usu_id", None)

                det = AperturaCierreDetDto(
                    tipo=tipo,
                    concepto=concepto,
                    monto=monto,
                    fecha_mov=fecha_mov,
                    usu_id=usu_id_mov
                )
                detalle.append(det)

            except Exception as ex:
                return jsonify({"error": f"Detalle inválido en la fila {idx+1}: {str(ex)}"}), 400

        if not detalle:
            return jsonify({"error": "Debe agregar al menos un movimiento válido"}), 400

        # -----------------------------
        # PARSE CABECERA
        # -----------------------------
        try:
            fecha_apertura = parse_fecha_hora(data["fecha_apertura"], "fecha_apertura")
            fecha_cierre = parse_fecha_hora(data["fecha_cierre"], "fecha_cierre") if data.get("fecha_cierre") else None
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400

        cab = AperturaCierreCabDto(
            id_caja_cab=data.get("id_caja_cab"),
            id_suc=int(data["id_suc"]),
            usu_id=data["usu_id"],
            fecha_apertura=fecha_apertura,
            monto_inicial=float(data["monto_inicial"]),
            fecha_cierre=fecha_cierre,
            monto_final=float(data.get("monto_final", 0)) if fecha_cierre else None,
            monto_teorico=float(data.get("monto_teorico", 0)),
            diferencia=float(data.get("diferencia", 0)),
            estado=data.get("estado", "abierta"),
            observaciones=data.get("observaciones", ""),
            detalle=detalle
        )

        # -----------------------------
        # GUARDAR EN BD
        # -----------------------------
        ok = dao.guardar(cab)
        return jsonify({"success": ok}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# CERRAR CAJA (CAMBIAR ESTADO)
# ============================================================
@apcapi.route('/<int:id>/cerrar', methods=['PUT'])
def cerrar(id):
    try:
        ok = dao.cambiar_estado(id, "cerrada")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ANULAR CAJA
# ============================================================
@apcapi.route('/<int:id>/anular', methods=['PUT'])
def anular(id):
    try:
        ok = dao.cambiar_estado(id, "anulada")
        return jsonify({"success": ok}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
