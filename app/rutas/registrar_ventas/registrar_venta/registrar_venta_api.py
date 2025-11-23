from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from app.dao.registrar_ventas.registrar_venta.registrar_venta_dao import RegistrarVentaDao
from app.dao.registrar_ventas.registrar_venta.dto.registrar_venta_cab_dto import VentaCabDto
from app.dao.registrar_ventas.registrar_venta.dto.registrar_venta_det_dto import VentaDetDto

venta_api = Blueprint('venta_api', __name__, url_prefix='/api/v1/venta')

# DAO
ventaDao = RegistrarVentaDao()


@venta_api.route('/csrf-token')
def csrf_token():
    token = "1234567890"
    return jsonify({"csrf_token": token})


@venta_api.route('', methods=['POST'])
def crear_venta():
    try:
        data = request.get_json()
        
        print("=" * 50)
        print("DATOS RECIBIDOS:")
        print(data)
        print("=" * 50)

        # Validar datos recibidos
        if not data:
            return jsonify({"success": False, "error": "No se recibieron datos"}), 400

        # Crear cabecera
        venta_cab = VentaCabDto(
            id_cliente=data.get('id_cliente'),
            id_suc=data.get('id_suc'),
            usu_id=data.get('usu_id'),
            fecha_venta=datetime.now(),
            nro_factura=data.get('nro_factura'),
            tipo_venta=data.get('tipo_venta'),
            total=0,  # Se calcula en el DAO
            estado=data.get('estado', 'PROCESADO'),
            observaciones=data.get('observaciones', '')
        )

        # Crear detalle
        detalle = []
        for item in data.get('detalle', []):
            det = VentaDetDto(
                id_producto=item.get('id_producto'),
                cantidad=float(item.get('cantidad', 0)),
                precio_unitario=float(item.get('precio_unitario', 0)),
                descuento=float(item.get('descuento', 0)),
                observaciones=item.get('observaciones', '')
            )
            detalle.append(det)

        print(f"Cabecera: cliente={venta_cab.id_cliente}, tipo={venta_cab.tipo_venta}")
        print(f"Detalle: {len(detalle)} items")

        # Usar el método crear_venta que ya existe en el DAO
        id_venta_cab = ventaDao.crear_venta(venta_cab, detalle)

        print(f"✅ Venta creada exitosamente con ID: {id_venta_cab}")

        return jsonify({"success": True, "id_venta_cab": id_venta_cab}), 201

    except Exception as e:
        print("=" * 50)
        print("❌ ERROR:")
        print(str(e))
        print("=" * 50)
        
        import traceback
        traceback.print_exc()
        
        return jsonify({"success": False, "error": str(e)}), 500


@venta_api.route('/<int:id>', methods=['GET'])
def obtener_venta(id):
    try:
        venta = ventaDao.obtener_venta_cab(id)
        if not venta:
            return jsonify({"success": False, "error": "Venta no encontrada"}), 404
        
        detalle = ventaDao.obtener_detalle(id)
        
        return jsonify({
            "success": True,
            "venta": venta.to_dict(),
            "detalle": [d.to_dict() for d in detalle]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@venta_api.route('', methods=['GET'])
def listar_ventas():
    try:
        ventas = ventaDao.listar_cabecera()
        return jsonify({
            "success": True,
            "ventas": [v.to_dict() for v in ventas]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500