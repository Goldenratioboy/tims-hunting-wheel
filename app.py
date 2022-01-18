from flask import Flask, request
from db_conn import get_rows
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Health Check"

# Get Odds Main endpoint
@app.route("/get-odds")
def get_odds():
    args = request.args
    if args.get('weapon') is None:
        return 'Invalid input'
    if args.get('species') is None:
        return 'Invalid input'
    if args.get('resident') is None:
        return 'Invalid input'
    if args.get('points') is None:
        return 'Invalid input'
    print(args.get('weapon'), args.get('species'), args.get('resident'), args.get('points'))
    return_value = get_rows(args.get('weapon'), args.get('species'), args.get('resident'), args.get('points'))
    return json.dumps(return_value)


if __name__ == '__main__':
    app.run(debug=True)