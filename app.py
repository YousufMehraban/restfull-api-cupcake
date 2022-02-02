"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template, jsonify
from models import db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

db.app = app
db.init_app(app)


@app.route('/')
def index():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def show_cupcakes():
    """show all cupcakes"""
    cupcakes = [ cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    """show a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """create a cupcake, save it in the database and respond with json"""
    flavor = request.json.get('flavor')
    size = request.json.get('size')
    rating = request.json.get('rating')
    image = request.json.get('image')

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """update a cupcake in the database and respond with json"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')

