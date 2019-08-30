from flask_restful import Resource, reqparse
from billing import models_bill
from billing.services_bill import BillingService


class Billing(Resource):
    def post(self):

        try:
            billingService = BillingService();
            responseStr = billingService.runbilling();

            return {
                'message': 'Billing has been done.'.format(responseStr),
            }
        except:
            return {'message': 'Something went wrong'}, 500

