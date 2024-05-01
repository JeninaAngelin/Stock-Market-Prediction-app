from flask import Flask, render_template, request
from utils.helpers import preprocess_input, predict_closing_price

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        datetime_str = request.form['datetime']
        stock_name = request.form['stock_name']
        stock_name = request.form['stock_name'].upper()  # Convert to uppercase
        valid_stocks = ['XPEV', 'TSLA', 'F', 'NIO']

        if stock_name not in valid_stocks:
            error_message = f"Invalid stock name: {stock_name}. Please enter one of the following: XPEV, TSLA, F, NIO."
            return render_template('results.html', error_message=error_message)
        predicted_price = predict_closing_price(datetime_str, stock_name)
        return render_template('results.html', stock_name=stock_name, datetime_str=datetime_str, predicted_price=predicted_price)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
