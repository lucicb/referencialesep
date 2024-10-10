from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.profesional.ProfesionalDao import ProfesionalDao

profapi = Blueprint('profapi', __name__)

# Trae todos los profesionales
@profapi.route('/profesional', methods=['GET'])
def getAllProfesional():
    profdao = ProfesionalDao()

    try:
        profesional = profdao.getProfesional()

        return jsonify({
            'success': True,
            'data': profesional,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas profesional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un profesional por su ID
@profapi.route('/profesional/<int:profesional_id>', methods=['GET'])
def getProfesional(profesional_id):
    profdao = ProfesionalDao()

    try:
        profesional = profdao.getProfesionalById(profesional_id)

        if profesional:
            return jsonify({
                'success': True,
                'data': profesional,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la profesional con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener profesional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo profesional
@profapi.route('/profesional', methods=['POST'])
def addProfesional():
    data = request.get_json()
    profdao = ProfesionalDao()

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
        profesional_id = profdao.guardarProfesional(descripcion)
        if profesional_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': profesional_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar profesional. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar profesional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un profesional existente
@profapi.route('/profesional/<int:profesional_id>', methods=['PUT'])
def updateProfesional(profesional_id):
    data = request.get_json()
    profdao = ProfesionalDao()

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
        if profdao.updateProfesional(profesional_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': profesional_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró profesional con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar profesional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un profesional
@profapi.route('/profesional/<int:profesional_id>', methods=['DELETE'])
def deleteProfesional(profesional_id):
    profdao = ProfesionalDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if profdao.deleteProfesional(profesional_id):
            return jsonify({
                'success': True,
                'mensaje': f'Profesional con ID {profesional_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró profesional con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar profesional: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500