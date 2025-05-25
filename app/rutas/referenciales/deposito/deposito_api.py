from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.deposito.deposito_dao import DepositoDao

# Crear Blueprint para el API de Depósitos
depoapi = Blueprint('depoapi', __name__)

# Obtener todos los depósitos
@depoapi.route('/depositos', methods=['GET'])
def get_depositos():
    dao = DepositoDao()

    try:
        depositos = dao.get_depositos()
        return jsonify({
            'success': True,
            'data': depositos,
            'error': False
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener los depósitos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador'
        }), 500

# Obtener un depósito por su ID
@depoapi.route('/depositos/<int:id_deposito>', methods=['GET'])
def get_deposito(id_deposito):
    dao = DepositoDao()

    try:
        deposito = dao.get_deposito_by_id(id_deposito)
        if deposito:
            return jsonify({
                'success': True,
                'data': deposito,
                'error': False
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Depósito no encontrado'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener el depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador'
        }), 500

# Agregar un nuevo depósito
@depoapi.route('/depositos', methods=['POST'])
def add_deposito():
    data = request.get_json()

    # Verificar que los parámetros necesarios estén presentes
    if not data or 'nombre_deposito' not in data or 'id_sucursal' not in data:
        return jsonify({
            'success': False,
            'error': 'Faltan parámetros: nombre_deposito o id_sucursal'
        }), 400

    nombre_deposito = data['nombre_deposito']
    id_sucursal = data['id_sucursal']

    dao = DepositoDao()

    try:
        deposito_id = dao.guardarDeposito(nombre_deposito, id_sucursal)
        if deposito_id:
            return jsonify({
                'success': True,
                'data': {'id_deposito': deposito_id, 'nombre_deposito': nombre_deposito, 'id_sucursal': id_sucursal},
                'error': False
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el depósito'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar el depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador'
        }), 500

# Actualizar un depósito
@depoapi.route('/depositos/<int:id_deposito>', methods=['PUT'])
def update_deposito(id_deposito):
    data = request.get_json()

    # Verificar que los parámetros necesarios estén presentes
    if not data or 'nombre_deposito' not in data or 'id_sucursal' not in data:
        return jsonify({
            'success': False,
            'error': 'Faltan parámetros: nombre_deposito o id_sucursal'
        }), 400

    nombre_deposito = data['nombre_deposito']
    id_sucursal = data['id_sucursal']

    dao = DepositoDao()

    try:
        updated = dao.updateDeposito(id_deposito, nombre_deposito, id_sucursal)
        if updated:
            return jsonify({
                'success': True,
                'data': {'id_deposito': id_deposito, 'nombre_deposito': nombre_deposito, 'id_sucursal': id_sucursal},
                'error': False
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el depósito'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al actualizar el depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador'
        }), 500

# Eliminar un depósito
@depoapi.route('/depositos/<int:id_deposito>', methods=['DELETE'])
def delete_deposito(id_deposito):
    dao = DepositoDao()

    try:
        deleted = dao.deleteDeposito(id_deposito)
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Depósito eliminado exitosamente',
                'error': False
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el depósito'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al eliminar el depósito: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador'
        }), 500




