from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

def compute_beta(data):
    try:
        stocks = data['tickers']
        # running sum
        cum_sum = 0
        for i in range(len(stocks)):
            temp = yf.Ticker(stocks[i])
            if(temp.info['symbol'] == 'SPY'):
                cum_sum += 1 # SPY has no beta
            elif(temp.info['beta'] == None):
                cum_sum += 0 # No beta = 0
            else:
                cum_sum += temp.info['beta']
        # calculate the average beta of your portfolio
        return cum_sum / len(stocks)
    # make sure the request is valid
    except KeyError:
        print("invalid format for data")
        return 0.0
    except ValueError:
        print("could not find stock")
        return 0.0

@app.route('/tickers', methods = ['POST'])
def tickers():
    tickers = json.loads(request.data)
    beta = compute_beta(tickers)
    print(beta)
    return jsonify(beta=beta)

@app.route('/')
def hello_world():
    return 'Finance API'

if __name__ == "__main__":
    app.run(host="10.0.0.27")
