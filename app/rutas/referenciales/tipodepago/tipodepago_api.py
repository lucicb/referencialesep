from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tipodepago.TipodepagoDao import TipodepagoDao

tippapi = Blueprint('tippapi', __name__)

# Trae todos los tipos de pago
@tippapi.route('/tipodepago', methods=['GET'])
def getAllTipodepago():
    tippdao = TipodepagoDao()

    try:
        tipodepago = tippdao.getTipodepago()

        return jsonify({
            'success': True,
            'data': tipodepago,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los tipo de pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un tipo de pago por su ID
@tippapi.route('/tipodepago/<int:tipodepago_id>', methods=['GET'])
def getTipodepagoById(tipodepago_id):
    tippdao = TipodepagoDao()

    try:
        tipodepago = tippdao.getTipodepagoById(tipodepago_id)

        if tipodepago:
            return jsonify({
                'success': True,
                'data': tipodepago,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de pago con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener el tipo de pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo tipo de pago
@tippapi.route('/tipodepago', methods=['POST'])
def addTipodepago():
    data = request.get_json()
    tippdao = TipodepagoDao()

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
        tipodepago_id = tippdao.guardarTipodepago(descripcion)
        if tipodepago_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': tipodepago_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el tipo de pago. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar tipo de pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un tipo de pago existente
@tippapi.route('/tipodepago/<int:tipodepago_id>', methods=['PUT'])
def updateTipodepago(tipodepago_id):
    data = request.get_json()
    tippdao = TipodepagoDao()

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
        if tippdao.updateTipodepago(tipodepago_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': tipodepago_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de pago con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar el tipo de pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un tipo de pago
@tippapi.route('/tipodepago/<int:tipodepago_id>', methods=['DELETE'])
def deleteTipodepago(tipodepago_id):
    tippdao = TipodepagoDao()

    try:
        if tippdao.deleteTipodepago(tipodepago_id):
            return jsonify({
                'success': True,
                'mensaje': f'Tipo de pago con ID {tipodepago_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el tipo de pago con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar el tipo de pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500