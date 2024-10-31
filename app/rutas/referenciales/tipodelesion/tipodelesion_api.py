from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tipodelesion.TipodelesionDao import TipodelesionDao

tiplapi = Blueprint('tiplapi', __name__)

# Trae todas las ciudades
@tiplapi.route('/tipodelesion', methods=['GET'])
def getTipodelesion():
    tipldao = TipodelesionDao()

    try:
        tipodelesion = tipldao.getTipodelesion()

        return jsonify({
            'success': True,
            'data': tipodelesion,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipo de lesiones: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tiplapi.route('/tipodelesion/<int:tipodelesion_id>', methods=['GET'])
def getTipodelesion(tipodelesion_id):
    tipldao = TipodelesionDao()

    try:
        tipodelesion = tipldao.getTipodelesionById(tipodelesion_id)

        if tipodelesion:
            return jsonify({
                'success': True,
                'data': tipodelesion,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de lesion con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener tipo de lesion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ciudad
@tiplapi.route('/tipodelesion', methods=['POST'])
def addTipodelesion():
    data = request.get_json()
    tipldao = TipodelesionDao()

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
        tipodelesion_id = tipldao.guardarTipodelesion(descripcion)
        if tipodelesion_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': tipodelesion_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el tipo de lesion. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de lesion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tiplapi.route('/tipodelesion/<int:tipodelesion_id>', methods=['PUT'])
def updateTipodelesion(tipodelesion_id):
    data = request.get_json()
    tipldao = TipodelesionDao()

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
        if tipldao.updateTipodelesion(tipodelesion_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': tipodelesion_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de lesion con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tipo de lesion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tiplapi.route('/tipodelesion/<int:ciudad_id>', methods=['DELETE'])
def deleteTipodelesion(tipodelesion_id):
    tipldao = TipodelesionDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if tipldao.deleteTipodelesion(tipodelesion_id):
            return jsonify({
                'success': True,
                'mensaje': f'Tipo de lesion con ID {tipodelesion_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de lesion con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar tipo de lesion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500