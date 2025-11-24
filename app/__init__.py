from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

app = Flask(__name__)
csrf.init_app(app)
# Inicializar secret key
app.secret_key = b'_5#y2L"F6Q7z\n\xec]'

# Establecer duración de sesión, 15 minutos
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# Importar módulo de seguridad
from app.rutas.seguridad.login_routes import logmod
app.register_blueprint(logmod)

# Importar las rutas de referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod  # ciudad
from app.rutas.referenciales.paises.pais_routes import paimod   # pais
from app.rutas.referenciales.nacionalidad.nacionalidad_routes import naciomod  # nacionalidad
from app.rutas.referenciales.estado_civil.estado_civil_routes import estacivmod  # estado civil
# from app.rutas.referenciales.sexo.sexo_routes import sexmod  # sexo (comentado, si no lo usas)
from app.rutas.referenciales.persona.persona_routes import persmod  # persona
from app.rutas.referenciales.dia.dia_routes import diamod  # dia
from app.rutas.referenciales.turno.turno_routes import turmod  # turno
from app.rutas.referenciales.horario.horario_routes import horamod  # horario
# from app.rutas.referenciales.sucursal.sucursal_routes import sucurmod  # sucursal (comentado, si no lo usas)
from app.rutas.referenciales.profesional.profesional_routes import profmod  # profesional
# from app.rutas.referenciales.tipodepago.tipodepago_routes import tippmod  # tipodepago (comentado, si no lo usas)
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_routes import tipcmod  # tipodeconsulta
from app.rutas.referenciales.cargo.cargo_routes import carmod  # cargo
from app.rutas.referenciales.departamento.departamento_routes import depmod  # departamento
from app.rutas.referenciales.deposito.deposito_routes import depomod

# Importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes import pdcmod

# Registrar las rutas de referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')  # ciudad
app.register_blueprint(paimod, url_prefix=f'{modulo0}/paises')  # pais
app.register_blueprint(naciomod, url_prefix=f'{modulo0}/nacionalidad')  # nacionalidad
app.register_blueprint(estacivmod, url_prefix=f'{modulo0}/estadocivil')  # estado civil
# app.register_blueprint(sexmod, url_prefix=f'{modulo0}/sexo')  # sexo (comentado)
app.register_blueprint(persmod, url_prefix=f'{modulo0}/persona')  # persona
app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia')  # dia
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')  # turno
app.register_blueprint(horamod, url_prefix=f'{modulo0}/horario')  # horario
# app.register_blueprint(sucurmod, url_prefix=f'{modulo0}/sucursal')  # sucursal (comentado)
app.register_blueprint(profmod, url_prefix=f'{modulo0}/profesional')  # profesional
# app.register_blueprint(tippmod, url_prefix=f'{modulo0}/tipodepago')  # tipodepago (comentado)
app.register_blueprint(tipcmod, url_prefix=f'{modulo0}/tipodeconsulta')  # tipodeconsulta
app.register_blueprint(carmod, url_prefix=f'{modulo0}/cargo')  # cargo
app.register_blueprint(depmod, url_prefix=f'{modulo0}/departamento')  # departamento
app.register_blueprint(depomod, url_prefix=f'{modulo0}/deposito')  # deposito

# Registrar las rutas de gestionar compras
#modulo1 = '/gestionar-compras'
#app.register_blueprint(pdcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')  # registrar pedidos compras

# Registrar las APIs
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.paises.pais_api import paisapi
from app.rutas.referenciales.nacionalidad.nacionalidad_api import nacioapi
from app.rutas.referenciales.estado_civil.estado_civil_api import estacivapi
# from app.rutas.referenciales.sexo.sexo_api import sexapi  # sexo (comentado)
from app.rutas.referenciales.persona.persona_api import persapi
from app.rutas.referenciales.dia.dia_api import diaapi
from app.rutas.referenciales.turno.turno_api import turnoapi
from app.rutas.referenciales.horario.horario_api import horaapi
# from app.rutas.referenciales.sucursal.sucursal_api import sucurapi  # sucursal (comentado)
from app.rutas.referenciales.profesional.profesional_api import profapi
# from app.rutas.referenciales.tipodepago.tipodepago_api import tippapi  # tipodepago (comentado)
from app.rutas.referenciales.tipodeconsulta.tipodeconsulta_api import tipcapi
from app.rutas.referenciales.cargo.cargo_api import carapi
from app.rutas.referenciales.departamento.departamento_api import depapi
from app.rutas.referenciales.deposito.deposito_api import depoapi
from app.rutas.referenciales.sucursal.sucursal_api import sucapi
#from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi

# Registrar las APIs v1
version1 = '/api/v1'
api_v1 = '/api/v1'

app.register_blueprint(ciuapi, url_prefix=f'{version1}/ciudad')  # ciudad
app.register_blueprint(paisapi, url_prefix=f'{version1}/paises')  # pais
app.register_blueprint(nacioapi, url_prefix=f'{version1}/nacionalidad')  # nacionalidad
app.register_blueprint(estacivapi, url_prefix=f'{version1}/estadocivil')  # estado civil
# app.register_blueprint(sexapi, url_prefix=f'{version1}/sexo')  # sexo (comentado)
app.register_blueprint(persapi, url_prefix=f'{version1}/persona')  # persona
app.register_blueprint(diaapi, url_prefix=f'{version1}/dia')  # dia
app.register_blueprint(turnoapi, url_prefix=f'{version1}/turno')  # turno
app.register_blueprint(horaapi, url_prefix=f'{version1}/horario')  # horario
# app.register_blueprint(sucurapi, url_prefix=f'{version1}/sucursal')  # sucursal (comentado)
app.register_blueprint(profapi, url_prefix=f'{version1}/profesional')  # profesional
# app.register_blueprint(tippapi, url_prefix=f'{version1}/tipodepago')  # tipodepago (comentado)
app.register_blueprint(tipcapi, url_prefix=f'{version1}/tipodeconsulta')  # tipodeconsulta
app.register_blueprint(carapi, url_prefix=f'{version1}/cargo')  # cargo
app.register_blueprint(depapi, url_prefix=f'{version1}/departamento')  # departamento
app.register_blueprint(depoapi, url_prefix=f'{version1}/deposito')

# Gestionar compras API
#apiversion1 = '/api/v1'
#app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-pedido-compras')  # registrar pedidos compras
app.register_blueprint(sucapi, url_prefix=f'{version1}/sucursal')  # sucursal

 # ================================
# Gestionar Compras - Rutas
# ================================
modulo_compras = '/gestionar-compras'

from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedidos_compras_routes import pdcmod
from app.rutas.gestionar_compras.registrar_solicitud_compras.registrar_solicitud_compras_routes import solmod
from app.rutas.gestionar_compras.registrar_presupuesto.registrar_presupuesto_routes import presumod
from app.rutas.gestionar_compras.registrar_recepcion_compras.recepcion_mercaderia_routes import rm_mod

app.register_blueprint(pdcmod, url_prefix=f'{modulo_compras}/registrar-pedido-compras')
app.register_blueprint(solmod, url_prefix=f'{modulo_compras}/registrar-solicitud-compras')
app.register_blueprint(presumod, url_prefix=f'{modulo_compras}/registrar-presupuesto')
app.register_blueprint(rm_mod, url_prefix=f'{modulo_compras}/registrar-recepcion-compras')

# ================================
# Gestionar Compras - APIs
# ================================
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api import pdcapi
from app.rutas.gestionar_compras.registrar_solicitud_compras.registrar_solicitud_compras_api import scapi
from app.rutas.gestionar_compras.registrar_presupuesto.registrar_presupuesto_api import presuapi
from app.rutas.gestionar_compras.registrar_recepcion_compras.recepcion_mercaderia_api import rm_api

app.register_blueprint(pdcapi, url_prefix=f'{api_v1}{modulo_compras}/registrar-pedido-compras')
app.register_blueprint(scapi, url_prefix=f'{api_v1}{modulo_compras}/registrar-solicitud-compras')
app.register_blueprint(presuapi, url_prefix=f'{api_v1}{modulo_compras}/registrar-presupuesto')
# Exento CSRF porque recibe JSON desde AJAX
app.register_blueprint(rm_api, url_prefix=f'{api_v1}{modulo_compras}/recepcion-mercaderias')
csrf.exempt(pdcapi)
csrf.exempt(scapi)
csrf.exempt(presuapi)
csrf.exempt(rm_api)


# ================================
# Orden de Producción - Rutas y APIs
# ================================
from app.rutas.registrar_produ.registrar_orden_produ.orden_produccion_routes import opmod
from app.rutas.registrar_produ.registrar_orden_produ.orden_produccion_api import opapi


modulo_produccion = '/produccion'

# Rutas HTML
app.register_blueprint(opmod, url_prefix='/produccion/registrar-orden')

# APIs
app.register_blueprint(opapi, url_prefix=f'{api_v1}/orden-produccion')

# Exentos CSRF
csrf.exempt(opmod)
csrf.exempt(opapi)


# ================================
# Control de Calidad - Rutas y APIs
# ================================
from app.rutas.registrar_produ.registrar_control_calidad.control_calidad_routes import ccmod
from app.rutas.registrar_produ.registrar_control_calidad.control_calidad_api import ccapi

# Rutas HTML
app.register_blueprint(ccmod, url_prefix='/produccion/registrar-control-calidad')

# APIs
app.register_blueprint(ccapi, url_prefix=f'{api_v1}/control-calidad')

# Exentos CSRF
csrf.exempt(ccmod)
csrf.exempt(ccapi)

# ================================
# Registro de Mermas - Rutas y APIs
# ================================
from app.rutas.registrar_produ.registrar_mermas.mermas_routes import mermod
from app.rutas.registrar_produ.registrar_mermas.mermas_api import merapi

# Rutas HTML
app.register_blueprint(mermod, url_prefix='/produccion/registrar-mermas')

# APIs
app.register_blueprint(merapi, url_prefix=f'{api_v1}/mermas')

# Exentos CSRF
csrf.exempt(mermod)
csrf.exempt(merapi)





# ================================
# Etapa de Producción - Rutas y APIs
# ================================
from app.rutas.registrar_produ.registrar_etapa_produ.etapa_produ_routes import epmod
from app.rutas.registrar_produ.registrar_etapa_produ.etapa_produ_api import epapi

modulo_etapa = '/produccion'

# Rutas HTML
app.register_blueprint(epmod, url_prefix='/produccion/registrar-etapa')

# APIs
app.register_blueprint(epapi, url_prefix=f'{api_v1}/etapa-produccion')

# Exentos CSRF
csrf.exempt(epmod)
csrf.exempt(epapi)




# ================================
# Pedido de Materia Prima - Rutas y APIs
# ================================
from app.rutas.registrar_produ.registrar_pedido_mp.pedido_mp_routes import pmpmod
from app.rutas.registrar_produ.registrar_pedido_mp.pedido_mp_api import pmpapi

modulo_produccion = '/produccion'

# Rutas HTML
app.register_blueprint(pmpmod, url_prefix='/produccion/pedido-mp')

# APIs
app.register_blueprint(pmpapi, url_prefix=f'{api_v1}/pedido-mp')

# Exentos CSRF
csrf.exempt(pmpmod)
csrf.exempt(pmpapi)



# ================================
# Cierre - Rutas y APIs
# ================================
from app.rutas.referenciales.apertura.apertura_routes import apermod
from app.rutas.referenciales.apertura.apertura_api import aperapi

app.register_blueprint(apermod, url_prefix=f'{modulo0}/apertura')  
app.register_blueprint(aperapi, url_prefix=f'{api_v1}')



from app.rutas.referenciales.cierre.cierre_routes import cierremod
from app.rutas.referenciales.cierre.cierre_api import cierreapi

app.register_blueprint(cierreapi, url_prefix=api_v1)
app.register_blueprint(cierremod, url_prefix=f'{modulo0}/cierre')

# ================================
# pedidos clientes - Rutas y APIs
# ================================
from app.rutas.registrar_ventas.registrar_pedidos_clientes.pedidos_clientes_routes import pedmod
from app.rutas.registrar_ventas.registrar_pedidos_clientes.pedidos_clientes_api import pedapi

# Registrar Blueprints
app.register_blueprint(pedmod, url_prefix='/ventas/pedidos-clientes')
app.register_blueprint(pedapi)
# Exentos CSRF
csrf.exempt(pedmod)
csrf.exempt(pedapi)

# ================================
# apertura y cierre de caja - Rutas y APIs
# ================================
from app.rutas.registrar_ventas.registrar_apertura_cierre.apertura_cierre_routes import apcmod
from app.rutas.registrar_ventas.registrar_apertura_cierre.apertura_cierre_api import apcapi

app.register_blueprint(apcmod, url_prefix='/ventas/apertura-cierre')  # <-- Agregar url_prefix vacío o sin prefijo
app.register_blueprint(apcapi)  # Este ya tiene url_prefix en su definición

csrf.exempt(apcmod)
csrf.exempt(apcapi)

# ================================
# registrar venta - Rutas y APIs
# ================================
from app.rutas.registrar_ventas.registrar_venta.registrar_venta_routes import venta_mod
from app.rutas.registrar_ventas.registrar_venta.registrar_venta_api import venta_api

# Registrar Blueprints
app.register_blueprint(venta_mod, url_prefix='/ventas/registrar-venta')
app.register_blueprint(venta_api)  # <-- SIN url_prefix porque ya lo tiene definido internamente

# Exentos CSRF
csrf.exempt(venta_mod)
csrf.exempt(venta_api)





csrf.exempt(logmod)
csrf.exempt(ciumod)
csrf.exempt(paimod)
csrf.exempt(naciomod)
csrf.exempt(estacivmod)
csrf.exempt(persmod)
csrf.exempt(diamod)
csrf.exempt(turmod)
csrf.exempt(horamod)
csrf.exempt(profmod)
csrf.exempt(tipcmod)
csrf.exempt(carmod)
csrf.exempt(depmod)
csrf.exempt(depomod)
csrf.exempt(pdcmod)
csrf.exempt(solmod)
csrf.exempt(presumod)
csrf.exempt(rm_mod)
csrf.exempt(cierremod)

if __name__ == '__main__':
    app.run(debug=True)




