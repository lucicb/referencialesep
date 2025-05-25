from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ciudad.CiudadDao import CiudadDao
import traceback

ciuapi = Blueprint('ciuapi', __name__, url_prefix='/api/v1/ciudad')

# Trae todas las ciudades
@ciuapi.route('', methods=['GET'])
def getCiudades():
    ciudao = CiudadDao()
    try:
        ciudades = ciudao.getCiudades()
        return jsonify({
            'success': True,
            'data': ciudades,
            'error': None
        }), 200

    except Exception as e:
        error_msg = f"Error al obtener todas las ciudades: {str(e)}\n{traceback.format_exc()}"
        app.logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.',
            'debug': str(e)  # Opcional: quitar en producción
        }), 500

# Trae una ciudad específica por ID
@ciuapi.route('/<int:ciudad_id>', methods=['GET'])
def getCiudad(ciudad_id):
    ciudao = CiudadDao()

    try:
        ciudad = ciudao.getCiudadById(ciudad_id)
        if ciudad:
            return jsonify({
                'success': True,
                'data': ciudad,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ciudad con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener ciudad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ciudad
@ciuapi.route('', methods=['POST'])
def addCiudad():
    data = request.get_json()
    ciudao = CiudadDao()

    # Validar que el JSON tenga los campos necesarios
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        ciudad_id = ciudao.guardarCiudad(descripcion)
        if ciudad_id:
            return jsonify({
                'success': True,
                'data': {'id': ciudad_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la ciudad. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar ciudad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una ciudad existente
@ciuapi.route('/<int:ciudad_id>', methods=['PUT'])
def updateCiudad(ciudad_id):
    data = request.get_json()
    ciudao = CiudadDao()

    # Validar que el JSON tenga los campos necesarios
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion']

    try:
        if ciudao.updateCiudad(ciudad_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': ciudad_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ciudad con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar ciudad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una ciudad existente
@ciuapi.route('/<int:ciudad_id>', methods=['DELETE'])
def deleteCiudad(ciudad_id):
    ciudao = CiudadDao()

    try:
        if ciudao.deleteCiudad(ciudad_id):
            return jsonify({
                'success': True,
                'mensaje': f'Ciudad con ID {ciudad_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la ciudad con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar ciudad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
