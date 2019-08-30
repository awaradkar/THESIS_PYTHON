from flask_restful import Resource, reqparse
from masters.organization import models_org


parser = reqparse.RequestParser()
parser.add_argument('organizationId')
parser.add_argument('organizationName',help='This field cannot be blank',required = True)
parser.add_argument('organizationAddress')
parser.add_argument('organizationLocation')
parser.add_argument('organizationCity')
parser.add_argument('organizationZipCode')
parser.add_argument('organizationState')
parser.add_argument('organizationDate')
parser.add_argument('createdDate')
parser.add_argument('modifiedDate')
parser.add_argument('createdBy')
parser.add_argument('modifiedBy')


class Organization(Resource):
    def post(self):
        data = parser.parse_args()

        new_org = models_org.OrgModel(
            organizationName=data['organizationName'],
            organizationAddress=data['organizationAddress'],
            organizationLocation=data['organizationAddress'],
            organizationCity=data['organizationCity'],
            organizationZipCode=data['organizationZipCode'],
            organizationState=data['organizationState'],
            organizationDate=data['organizationDate'],
            createdBy=data['createdBy']
        )
        try:
            new_org.save_to_db()

            return {
                'message': 'Organization {} was created'.format(data),
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        data = parser.parse_args()

        try:
            return models_org.OrgModel.find_by_orgid(data['organizationId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        data = parser.parse_args()

        try:
            return models_org.OrgModel.delete_by_orgid(data['organizationId'])
        except:
            return {'message': 'Something went wrong'}, 500

    def put(self):
        data = parser.parse_args()

        new_org = models_org.OrgModel(
            organizationId=data['organizationId'],
            organizationName=data['organizationName'],
            organizationAddress=data['organizationAddress'],
            organizationLocation=data['organizationAddress'],
            organizationCity=data['organizationCity'],
            organizationZipCode=data['organizationZipCode'],
            organizationState=data['organizationState'],
            organizationDate=data['organizationDate'],
            modifiedBy=data['modifiedBy']
        )
        try:
            new_org.update_to_db()

            return {
                'message': 'Organization {} was updated'.format(data),

            }
        except:
            return {'message': 'Something went wrong'}, 500





class AllOrganizations(Resource):
    def get(self):
        return models_org.OrgModel.return_all()
