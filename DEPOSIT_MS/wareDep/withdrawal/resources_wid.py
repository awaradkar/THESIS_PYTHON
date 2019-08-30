from flask_restful import Resource, reqparse
from wareDep.withdrawal import models_wid


parser = reqparse.RequestParser()
parser.add_argument('withdrawalId')
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
parser.add_argument('withDrawalNoOfBags')
parser.add_argument('withdrawalQuantity')
parser.add_argument('withdrawalDate')
parser.add_argument('createdDate')
parser.add_argument('modifiedDate')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')


class Withdrawal(Resource):
    def post(self):
        data = parser.parse_args()

        new_withdrawal = models_wid.WithdrawalModel(
            depositId=data['depositId'],
            clientId=data['clientId'],
            clientName=data['clientName'],
            warehouseCode=data['warehouseCode'],
            warehouseName=data['warehouseName'],
            commodityCode=data['commodityCode'],
            commodityName=data['commodityName'],
            uomCode=data['uomCode'],
            packType=data['packType'],
            withDrawalNoOfBags=data['withDrawalNoOfBags'],
            withdrawalQuantity=data['withdrawalQuantity'],
            withdrawalDate=data['depositDate'],
            createdBy=data['createdBy']
        )
        try:
            new_withdrawal.save_to_db()

            return {
                'message': 'Withdrawal {} was created'.format(data),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        data = parser.parse_args()

        try:
            return models_wid.WithdrawalModel.find_by_withdrawalid(data['withdrawalId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        data = parser.parse_args()

        try:
            return models_wid.WithdrawalModel.delete_by_withdrawalid(data['withdrawalId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def put(self):
        data = parser.parse_args()

        new_withdrawal = models_wid.WithdrawalModel(
            txnId=data['txnId'],
            withdrawalId=data['withdrawalId'],
            depositId=data['depositId'],
            clientId=data['clientId'],
            clientName=data['clientName'],
            warehouseCode=data['warehouseCode'],
            warehouseName=data['warehouseName'],
            commodityCode=data['commodityCode'],
            commodityName=data['commodityName'],
            uomCode=data['uomCode'],
            packType=data['packType'],
            withDrawalNoOfBags=data['withDrawalNoOfBags'],
            withdrawalQuantity=data['withdrawalQuantity'],
            withdrawalDate=data['depositDate'],
            modifiedBy=data['modifiedBy']
        )
        try:
            new_withdrawal.update_to_db()

            return {
                'message': 'Withdrawal {} was updated'.format(data),

            }
        except:
            return {'message': 'Something went wrong'}, 500





class AllWithdrawals(Resource):
    def get(self):
        return models_wid.WithdrawalModel.return_all()
