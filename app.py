from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    flowers = Flowers.query.all()
    return render_template('index.html', flowers=flowers)


@app.route('/about_shop')
def about_shop():
    return render_template('about_shop.html')


@app.route('/buy/<int:id>')
def buy(id):
    flower = Flowers.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(flower.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        name_flower = request.form['name_flower']
        price = request.form['price']
        color = request.form['color']
        size_len = request.form['size_len']

        flower = Flowers(name_flower=name_flower, price=price, color=color, size_len=size_len)
        try:
            db.session.add(flower)
            db.session.commit()
            return redirect('/')

        except:
            return "При добавлении товара произошла ошибка"
    else:
        return render_template('create.html')


class Flowers(db.Model):
    __tablename__ = "flowers"
    id = db.Column(db.Integer, primary_key=True)
    name_flower = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Text, nullable=False)
    size_len = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Flowers %r' % self.id


if __name__ == '__main__':
    app.run(debug=True)
