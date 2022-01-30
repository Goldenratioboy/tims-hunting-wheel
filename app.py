from flask import Flask, request
from db_conn import get_rows
import json

app = Flask(__name__)

## takes in a 2d array and writes rows as a csv file
def dictionary_to_csv_string(input):
    result = ''

    for row in input:
        for item in row:
            result += str(item) + '; '
        result = result[:-2]
        result += '<br/>'

    return result

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
    return dictionary_to_csv_string(return_value)


if __name__ == '__main__':
    app.run(debug=True)

