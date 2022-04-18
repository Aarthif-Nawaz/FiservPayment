from flask import Flask, request, jsonify, make_response
from Functions import createPayment
app = Flask(__name__)

@app.route('/getTransactionStatus', methods=['GET','POST'])
def getStatus():
    if request.method == "POST":
        try:
            total_amount = request.get_json(force=True)['total_amount'] if request.get_json(force=True)['total_amount'] else "1.00"
            address = request.get_json(force=True)['address'] if request.get_json(force=True)['address'] else ""
            phone_number = request.get_json(force=True)['phone'] if request.get_json(force=True)['phone'] else ""
            card_number = request.get_json(force=True)['card_number'] if request.get_json(force=True)['card_number'] else ""
            expiry_month =  request.get_json(force=True)['expiry_month'] if request.get_json(force=True)['expiry_month'] else ""
            expiry_year = request.get_json(force=True)['expiry_year'] if request.get_json(force=True)['expiry_year'] else ""
            cvv = request.get_json(force=True)['cvv'] if request.get_json(force=True)['cvv'] else ""
            postal = request.get_json(force=True)['postal'] if request.get_json(force=True)['postal'] else ""
            country = request.get_json(force=True)['country'] if request.get_json(force=True)['country'] else ""
            email = request.get_json(force=True)['email'] if request.get_json(force=True)['email'] else ""
            city = request.get_json(force=True)['city'] if request.get_json(force=True)['city'] else ""
            name = request.get_json(force=True)['name'] if request.get_json(force=True)['name'] else ""
        except Exception as e:
            return jsonify({'Error :  Please provide below data' : e}, 400)
        r = createPayment(amount=total_amount,address=address, phone_number=phone_number, card_number=card_number, expiry_month=expiry_month, expiry_year=expiry_year, security_code=cvv, postalCode=postal, country=country, email=email, city=city, name=name)
        return make_response(jsonify({'Transaction Status' : r}), 200)
    else:
        return jsonify({'Result', 'Please post data to recieve status'}, 302)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
