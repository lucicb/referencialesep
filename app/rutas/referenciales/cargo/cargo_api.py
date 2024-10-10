from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.cargo.CargoDao import CargoDao

carapi = Blueprint('carapi', __name__)

# Trae todos los cargos
@carapi.route('/cargo', methods=['GET'])
def getAllCargos():
    cardao = CargoDao()

    try:
        cargo = cardao.getCargo()

        return jsonify({
            'success': True,
            'data': cargo,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los cargos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un cargo por su ID
@carapi.route('/cargo/<int:cargo_id>', methods=['GET'])
def getCargoById(cargo_id):
    cardao = CargoDao()

    try:
        cargo = cardao.getCargoById(cargo_id)

        if cargo:
            return jsonify({
                'success': True,
                'data': cargo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo cargo
@carapi.route('/cargo', methods=['POST'])
def addCargo():
    data = request.get_json()
    cardao = CargoDao()

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
        cargo_id = cardao.guardarCargo(descripcion)
        if cargo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': cargo_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el cargo. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un cargo existente
@carapi.route('/cargo/<int:cargo_id>', methods=['PUT'])
def updateCargo(cargo_id):
    data = request.get_json()
    cardao = CargoDao()

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
        if cardao.updateCargo(cargo_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': cargo_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un cargo
@carapi.route('/cargo/<int:cargo_id>', methods=['DELETE'])
def deleteCargo(cargo_id):
    cardao = CargoDao()

    try:
        if cardao.deleteCargo(cargo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cargo con ID {cargo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500