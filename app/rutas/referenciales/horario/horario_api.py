from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.horario.HorarioDao import HorarioDao

horaapi = Blueprint('horaapi', __name__)

# Trae todos los horarios
@horaapi.route('/horarios', methods=['GET'])
def getHorarios():
    horadao = HorarioDao()

    try:
        horarios = horadao.getHorarios()

        return jsonify({
            'success': True,
            'data': horarios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los horarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horaapi.route('/horarios/<int:horario_id>', methods=['GET'])
def getHorario(horario_id):
    horadao = HorarioDao()

    try:
        horario = horadao.getHorarioById(horario_id)

        if horario:
            return jsonify({
                'success': True,
                'data': horario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el horario con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo horario
@horaapi.route('/horarios', methods=['POST'])
def addHorario():
    data = request.get_json()
    horadao = HorarioDao()

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
        horario_id = horadao.guardarHorario(descripcion)
        if horario_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': horario_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el horario. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horaapi.route('/horarios/<int:horario_id>', methods=['PUT'])
def updateHorario(horario_id):
    data = request.get_json()
    horadao = HorarioDao()

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
        if horadao.updateHorario(horario_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': horario_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el horario con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horaapi.route('/horarios/<int:horario_id>', methods=['DELETE'])
def deleteHorario(horario_id):
    horadao = HorarioDao()

    try:
        # Usar el retorno de eliminarHorario para determinar el éxito
        if horadao.deleteHorario(horario_id):
            return jsonify({
                'success': True,
                'mensaje': f'Horario con ID {horario_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el horario con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500