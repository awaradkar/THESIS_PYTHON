from flask import Flask
from flask_restful import Api
from billing import resources_bill

app = Flask(__name__)
api = Api(app)

import __init__

api.add_resource(resources_dep.AllDeposits, '/deposits')
api.add_resource(resources_dep.Deposit, '/deposit')

api.add_resource(resources_wid.AllWithdrawals, '/withdrawals')
api.add_resource(resources_wid.Withdrawal, '/withdrawal')

db = __init__.db;