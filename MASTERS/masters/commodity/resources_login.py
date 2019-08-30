from flask import request, json, Response, Blueprint
from masters.commodity.models_comm import CommModel
import sys
import time

comm_api = Blueprint('login', __name__)


@comm_api.route('/', endpoint='getAll', methods=['GET'])
def get():
    return CommModel.return_all()


@comm_api.route('/', methods=['POST'])
def post():
    data = request.get_json()
    ###comm = CommModel.find_by_commodityname(data['commodityName'])
    ###if comm is not None:
    ###return {'message': 'Commodity {} already exists'.format(data['commodityName'])}

    new_comm = CommModel(
        commodityName=data['commodityName'],
        description=data['description'],
        uom=data['uom'],
        createdBy=data['createdBy']
    )
    try:
        new_comm.save()
        comm = CommModel.find_by_commodityname(data['commodityName'])
        return {
            'message': 'Commodity {} was created'.format(data),
        }
    except Exception as e:
        print(e)
        return {'message': 'Something went wrong'+e.__str__()}, 500


@comm_api.route('/<comm_id>', endpoint='getOne', methods=['GET'])
def get(comm_id):
    try:
        print(comm_id, file=sys.stdout);
        commodity = CommModel().find_by_commid(comm_id)
        return commodity;
    except Exception as e:
        print(e)
        return {'message': 'Something went wrong' + e.__str__()}, 500


@comm_api.route('/<comm_id>', methods=['DELETE'])
def delete(comm_id):
    try:
        return CommModel().delete_by_commid(comm_id)
    except:
        return {'message': 'Something went wrong'}, 500


@comm_api.route('/', methods=['PUT'])
def put():
    data = request.get_json()

    new_comm = CommModel(
        commodityId=data['commodityId'],
        commodityName=data['commodityName'],
        description=data['description'],
        uom=data['uom'],
        modifiedBy=data['modifiedBy']
    )
    try:
        new_comm.update_to_db()

        return {
            'message': 'Commodity {} was updated'.format(data),

        }
    except Exception as e:
        print(e)
        return {'message': 'Something went wrong' + e.__str__()}, 500
