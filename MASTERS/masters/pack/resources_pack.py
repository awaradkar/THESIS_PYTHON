from flask_restful import Resource, reqparse
from masters.pack import models_pack


parser = reqparse.RequestParser()
parser.add_argument('packId')
parser.add_argument('packType',help='This field cannot be blank',required = True)
parser.add_argument('packDeduction')
parser.add_argument('createdDate')
parser.add_argument('modifiedDate')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')


class Pack(Resource):
    def post(self):
        data = parser.parse_args()

        new_pack = models_pack.PackModel(
            packType=data['packType'],
            packDeduction=data['packDeduction'],
            createdBy=data['createdBy']
        )
        try:
            new_pack.save_to_db()

            return {
                'message': 'Pack {} was created'.format(data),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        data = parser.parse_args()

        try:
            return models_pack.PackModel.find_by_packid(data['packId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        data = parser.parse_args()

        try:
            return models_pack.PackModel.delete_by_packid(data['packId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def put(self):
        data = parser.parse_args()

        new_pack = models_pack.PackModel(
            packId=data['packId'],
            packType=data['packType'],
            packDeduction=data['packDeduction'],
            modifiedBy=data['modifiedBy']
        )
        try:
            new_pack.update_to_db()

            return {
                'message': 'Pack {} was updated'.format(data),

            }
        except:
            return {'message': 'Something went wrong'}, 500


class AllPacks(Resource):
    def get(self):
        return models_pack.PackModel.return_all()
