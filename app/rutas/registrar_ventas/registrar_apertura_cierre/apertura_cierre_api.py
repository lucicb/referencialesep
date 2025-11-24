from flask import Blueprint, jsonify, request
from datetime import datetime

from app.dao.registrar_ventas.registrar_apertura_cierre.apertura_cierre_dao import AperturaCierreDao
from app.dao.registrar_ventas.registrar_apertura_cierre.dto.apertura_cierre_cab_dto import AperturaCierreCabDto

apcapi = Blueprint('apcapi', __name__, url_prefix='/api/v1/apertura-cierre')
dao = AperturaCierreDao()


# ===============================
# CSRF TOKEN
# ===============================
@apcapi.route('/csrf-token', methods=['GET'])
def csrf_token():
    token = "1234567890"
    return jsonify({"csrf_token": token}), 200


# ============================================================
# LISTAR TODAS LAS APERTURAS DE CAJA
# ============================================================
@apcapi.route('', methods=['GET'])
def listar():
    try:
        aperturas = dao.listar_aperturas()
        return jsonify({
            "success": True,
            "aperturas": [a.to_dict() for a in aperturas]
        }), 200
    except Exception as e:
        print(f"Error listando aperturas: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# OBTENER UNA APERTURA POR ID
# ============================================================
@apcapi.route('/<int:id>', methods=['GET'])
def obtener(id):
    try:
        apertura = dao.obtener_por_id(id)
        if apertura:
            return jsonify({"success": True, "apertura": apertura.to_dict()}), 200
        else:
            return jsonify({"success": False, "error": "Apertura no encontrada"}), 404
    except Exception as e:
        print(f"Error obteniendo apertura: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# CREAR APERTURA DE CAJA
# ============================================================
@apcapi.route('', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        print("Datos recibidos para apertura:", data)
        
        if not data:
            return jsonify({"success": False, "error": "No se recibió data"}), 400

        # Validar campos obligatorios
        if not data.get('id_suc') or not data.get('usu_id') or not data.get('monto'):
            return jsonify({"success": False, "error": "Faltan campos obligatorios"}), 400

        # Crear DTO
        cab = AperturaCierreCabDto(
            id_suc=int(data['id_suc']),
            usu_id=data['usu_id'],
            monto_inicial=float(data['monto']),
            observaciones=data.get('observaciones', '')
        )

        # Guardar en BD
        id_generado = dao.crear_apertura(cab)
        
        print(f"✅ Apertura creada con ID: {id_generado}")
        return jsonify({"success": True, "id_caja_cab": id_generado}), 201

    except Exception as e:
        print(f"❌ Error creando apertura: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# CERRAR CAJA
# ============================================================
@apcapi.route('/cerrar/<int:id>', methods=['PUT'])
def cerrar(id):
    try:
        data = request.get_json()
        print(f"Cerrando caja {id} con datos:", data)
        
        if not data or not data.get('monto'):
            return jsonify({"success": False, "error": "Falta monto final"}), 400

        monto_final = float(data['monto'])
        
        # Cerrar caja
        dao.cerrar_caja(id, monto_final)
        
        print(f"✅ Caja {id} cerrada correctamente")
        return jsonify({"success": True}), 200
        
    except Exception as e:
        print(f"❌ Error cerrando caja: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500