from flask_restful import Resource, reqparse
from wareDep.deposit import models_dep


parser = reqparse.RequestParser()
parser.add_argument('depositId')
parser.add_argument('txnId')
parser.add_argument('clientId')
parser.add_argument('clientName')
parser.add_argument('warehouseCode')
parser.add_argument('warehouseName')
parser.add_argument('commodityCode')
parser.add_argument('commodityName')
parser.add_argument('uomCode')
parser.add_argument('packType')
parser.add_argument('noOfBags')
parser.add_argument('quantity')
parser.add_argument('netQuantity')
parser.add_argument('currenyQty')
parser.add_argument('currentPacks')
parser.add_argument('depositDate')
parser.add_argument('createdDate')
parser.add_argument('modifiedDate')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')

class Deposit(Resource):
    def post(self):
        data = parser.parse_args()

        new_dep = models_dep.DepositModel(
            clientId=data['clientId'],
            clientName=data['clientName'],
            warehouseCode=data['warehouseCode'],
            warehouseName=data['warehouseName'],
            commodityCode=data['commodityCode'],
            commodityName=data['commodityName'],
            uomCode=data['uomCode'],
            packType=data['packType'],
            noOfBags=data['noOfBags'],
            quantity=data['quantity'],
            netQuantity=data['netQuantity'],
            currenyQty=data['currenyQty'],
            currentPacks=data['currentPacks'],
            depositDate=data['depositDate'],
            createdBy=data['createdBy']
        )
        try:
            new_dep.save_to_db()

            return {
                'message': 'Deposit {} was created'.format(data),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        data = parser.parse_args()

        try:
            return models_dep.DepositModel.find_by_depid(data['depositId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        data = parser.parse_args()

        try:
            return models_dep.DepositModel.delete_by_depid(data['depositId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def put(self):
        data = parser.parse_args()

        new_dep = models_dep.DepositModel(
            depositId=data['depositId'],
            txnId=data['txnId'],
            clientId=data['clientId'],
            clientName=data['clientName'],
            warehouseCode=data['warehouseCode'],
            warehouseName=data['warehouseName'],
            commodityCode=data['commodityCode'],
            commodityName=data['commodityName'],
            uomCode=data['uomCode'],
            packType=data['packType'],
            noOfBags=data['noOfBags'],
            quantity=data['quantity'],
            netQuantity=data['netQuantity'],
            currenyQty=data['currenyQty'],
            currentPacks=data['currentPacks'],
            depositDate=data['depositDate'],
            modifiedBy=data['modifiedBy']
        )
        try:
            new_dep.update_to_db()

            return {
                'message': 'Deposit {} was updated'.format(data),

            }
        except:
            return {'message': 'Something went wrong'}, 500


class AllDeposits(Resource):
    def get(self):
        return models_dep.DepositModel.return_all()
