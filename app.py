from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():

    product_name = request.form['product_name']
    price = float(request.form['price'])
    rating = float(request.form['rating'])
    reviews = int(request.form['reviews'])

    data = pd.read_csv('products.csv')

    results = data[data['Product'].str.contains(product_name, case=False, na=False)]

    if len(results) == 0:
        return render_template(
            'result.html',
            products=[],
            status="No Data Found",
            risk=0,
            color="gray",
            lowest_price=None,
            highest_rating=None,
            most_reviews=None,
            best_choice=None
        )

    risk = 0

    avg_price = results['Price'].mean()

    if price < avg_price * 0.5:
        risk += 50

    if rating > 4.8 and reviews < 10:
        risk += 20

    if risk < 30:
        status = "Likely Genuine"
        color = "#2ecc71"
    elif risk < 60:
        status = "Possibly Fake"
        color = "#f39c12"
    else:
        status = "High Risk"
        color = "#e74c3c"

    lowest_price = results.loc[results['Price'].idxmin()]
    highest_rating = results.loc[results['Rating'].idxmax()]
    most_reviews = results.loc[results['Reviews'].idxmax()]
    best_choice = results.sort_values(by=['Rating', 'Reviews'], ascending=False).iloc[0]

    return render_template(
        'result.html',
        products=results.to_dict(orient="records"),
        status=status,
        risk=risk,
        color=color,
        lowest_price=lowest_price,
        highest_rating=highest_rating,
        most_reviews=most_reviews,
        best_choice=best_choice
    )

if __name__ == '__main__':
    app.run(debug=True)