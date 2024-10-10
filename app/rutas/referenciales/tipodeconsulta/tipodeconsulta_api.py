from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tipodeconsulta.TipodeconsultaDao import TipodeconsultaDao

tipcapi = Blueprint('tipcapi', __name__)

# Trae todos los tipos de consulta
@tipcapi.route('/tipodeconsulta', methods=['GET'])
def getAllTipodeconsulta():
    tipcdao = TipodeconsultaDao()

    try:
        tipodeconsulta = tipcdao.getTipodeconsulta()

        return jsonify({
            'success': True,
            'data': tipodeconsulta,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipos de consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un tipo de consulta por su ID
@tipcapi.route('/tipodeconsulta/<int:tipodeconsulta_id>', methods=['GET'])
def getTipodeconsultaById(tipodeconsulta_id):
    tipcdao = TipodeconsultaDao()

    try:
        tipodeconsulta = tipcdao.getTipodeconsultaById(tipodeconsulta_id)

        if tipodeconsulta:
            return jsonify({
                'success': True,
                'data': tipodeconsulta,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de consulta con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener tipo de consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo tipo de consulta
@tipcapi.route('/tipodeconsulta', methods=['POST'])
def addTipodeconsulta():
    data = request.get_json()
    tipcdao = TipodeconsultaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        tipodeconsulta_id = tipcdao.guardarTipodeconsulta(descripcion)
        if tipodeconsulta_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': tipodeconsulta_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el tipo de consulta. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un tipo de consulta existente
@tipcapi.route('/tipodeconsulta/<int:tipodeconsulta_id>', methods=['PUT'])
def updateTipodeconsulta(tipodeconsulta_id):
    data = request.get_json()
    tipcdao = TipodeconsultaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if tipcdao.updateTipodeconsulta(tipodeconsulta_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': tipodeconsulta_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de consulta con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un tipo de consulta
@tipcapi.route('/tipodeconsulta/<int:tipodeconsulta_id>', methods=['DELETE'])
def deleteTipodeconsulta(tipodeconsulta_id):
    tipcdao = TipodeconsultaDao()

    try:
        if tipcdao.deleteTipodeconsulta(tipodeconsulta_id):
            return jsonify({
                'success': True,
                'mensaje': f'Tipo de consulta con ID {tipodeconsulta_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de consulta con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500