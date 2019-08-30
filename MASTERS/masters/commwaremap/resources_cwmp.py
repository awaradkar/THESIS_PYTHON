from flask import request, json, Response, Blueprint
from masters.commwaremap.models_cwmp import WareCommMapModel


parser = reqparse.RequestParser()
parser.add_argument('wareCommId')
parser.add_argument('warehouseCode',help='This field cannot be blank',required = True)
parser.add_argument('commodityCode')
parser.add_argument('createdDate')
parser.add_argument('modifiedDate')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')


class WareCommMap(Resource):
    def post(self):
        data = parser.parse_args()

        new_commwaremap = models_cwmp.WareCommMapModel(
            warehouseCode=data['warehouseCode'],
            commodityCode=data['commodityCode'],
            createdBy=data['createdBy']
        )
        try:
            new_commwaremap.save_to_db()

            return {
                'message': 'WareCommMap {} was created'.format(data),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        data = parser.parse_args()

        try:
            return models_cwmp.WareCommMapModel.find_by_warecommid(data['wareCommId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        data = parser.parse_args()

        try:
            return models_cwmp.WareCommMapModel.delete_by_warecommid(data['wareCommId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def put(self):
        data = parser.parse_args()

        new_pack = models_cwmp.WareCommMapModel(
            wareCommId=data['wareCommId'],
            warehouseCode=data['warehouseCode'],
            commodityCode=data['commodityCode'],
            modifiedBy=data['modifiedBy']
        )
        try:
            new_pack.update_to_db()

            return {
                'message': 'WareCommMap {} was updated'.format(data),

            }
        except:
            return {'message': 'Something went wrong'}, 500





class AllWareCommMaps(Resource):
    def get(self):
        return models_cwmp.WareCommMapModel.return_all()
