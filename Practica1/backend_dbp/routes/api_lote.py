from controllers.authenticate import token_required
from flask import Blueprint, jsonify, make_response, request
from controllers.loteControl import LoteControl
from controllers.utils.errors import Erros
from flask_expects_json import expects_json

api_lote = Blueprint('api_lote', __name__)

# API para Motivo
loteC = LoteControl()
# Validadores
schema = {
    "type": "object",
    'properties': {
        "nombrePr": {"type": "string"},
        "fechaPr": {"type": "string"},
        "fechaVen": {"type": "string"},
        "cantidadL": {"type": "integer"},
    },
    'required': ["nombrePr","fechaPr", "fechaVen", "cantidadL"]
}

@api_lote.route("/lote")
def listar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize() for i in loteC.listar()]}),
        200
    )
@api_lote.route("/lote/por_caducar")
def listar_PorCaducar():
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in loteC.listar_PorCaducar()]}),
        200
    )
@api_lote.route("/lote/vencidos")
def listar_vencidos():
    lote = loteC.listar_vencidos()
    return make_response(
        jsonify({"msg": "OK", "code": 200, "datos": [i.serialize for i in loteC.listar_vencidos()]}),
        200
    )
    
@api_lote.route("/lote/guardarLote", methods=['POST'])
@expects_json(schema)
@token_required
def guardar():
    data = request.get_json()
    id = loteC.guardar(data)

    if id >= 0:
        return make_response(
            jsonify({"msg": "OK", "code": 200, "datos": {"tag": "Datos Guardados"}}),
            200
        )
    else:
        return make_response(
            jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Erros.error[str(id)]}}), 
            400
        )
    
