import json
import flask
from flask import request
from rent_reckoner.reckoner import RentReckoner
from rent_reckoner.provider.google_sheet_provider import GoogleDataProvider
from rent_reckoner.provider.trello_provider import TrelloDataProvider
from rent_reckoner.provider.splitwise_provider import SplitwiseDataProvider

app = flask.Flask(__name__)

GOOGLE_DATA_PROVIDER = GoogleDataProvider()
TRELLO_DATA_PROVIDER = TrelloDataProvider()
SPLITWISE_DATA_PROVIDER = SplitwiseDataProvider()
DATA_PROVIDERS = [GOOGLE_DATA_PROVIDER, TRELLO_DATA_PROVIDER, SPLITWISE_DATA_PROVIDER]
data_providet_id = 2
RENT_RECKONER = RentReckoner(DATA_PROVIDERS[data_providet_id])

def create_response(data):
    resp = flask.Response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/habitations/<int:habitant_id>/bills_to_ui")
def get_bills_to_ui(habitant_id):
    bills_to_ui = RENT_RECKONER.get_bills_to_ui(habitant_id)
    bills_to_ui = json.dumps(bills_to_ui, default=lambda o: o.__dict__)
    return create_response(bills_to_ui)

@app.route("/habitations/<int:habitant_id>/residents_to_ui")
def get_residents_to_ui(habitant_id):
    residents_to_ui = RENT_RECKONER.get_residents_to_ui(habitant_id)
    residents_to_ui = json.dumps(residents_to_ui, default=lambda o: o.__dict__)
    return create_response(residents_to_ui)

@app.route("/habitations/<int:habitant_id>/bills")
def get_bills(habitant_id):
    bills = DATA_PROVIDERS[data_providet_id].get_bills(habitant_id)
    bills = json.dumps(bills)
    return create_response(bills)

@app.route("/habitations/<int:habitant_id>/residents")
def get_residents(habitant_id):
    residents = DATA_PROVIDERS[data_providet_id].get_residents(habitant_id)
    residents = json.dumps(residents)
    return create_response(residents)

@app.route("/habitations/<int:habitant_id>/update_depts")
def update_depts(habitant_id):
    RENT_RECKONER.update_debts(habitant_id)
    return "updated"

@app.route("/habitations/<int:habitant_id>/residents", methods=['POST'])
def add_resident(habitant_id):
    resident = request.get_json()

    DATA_PROVIDERS[data_providet_id].add_resident(habitant_id, resident['start'], resident['end'], resident['name'])
    return create_response(resident)

@app.route("/habitations/<int:habitant_id>/bills", methods=['POST'])
def add_bill(habitant_id):
    bill = request.get_json()

    DATA_PROVIDERS[data_providet_id].add_bill(habitant_id, bill['start'], bill['end'], bill['type'], bill['amount'], bill['paid_by'])
    return create_response(bill)

@app.route("/habitations/<int:habitant_id>/merge/<int:source_id>/<int:target_id>", methods=['GET'])
def merge(habitant_id, source_id, target_id):
    DATA_PROVIDERS[source_id].merge(habitant_id, DATA_PROVIDERS[target_id])
    return 'merged'

@app.route("/splitwise", methods=['GET'])
def splitwise():
    return '<a href="' + SPLITWISE_DATA_PROVIDER.get_auth_url() + '">Splitwise</a>'

@app.route("/splitwise/auth", methods=['GET'])
def splitwise_auth():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")
    SPLITWISE_DATA_PROVIDER.auth(oauth_token, oauth_verifier)
    return 'authed'

if __name__ == "__main__":
    app.run(debug=True)
