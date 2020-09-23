import json
import os

from enum import Enum
from typing import List, Optional

from flask import Flask, request, abort, jsonify, render_template
from pydantic import BaseModel, ValidationError


app = Flask(__name__)
orders_fname = 'orders.json'


# Models

class Size(str, Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


class Topping(str, Enum):
    PEPPERONI = 'pepperoni'
    MUSRHOOM = 'mushroom'
    ONION = 'onion'


class Order(BaseModel):
    pizza_size: Size
    toppings: Optional[List[Topping]] = []


# Routes

@app.route('/')
def doc():
    return render_template('index.html')


@app.route('/orders', methods=['GET', 'POST'])
def list_orders():
    if not os.path.exists(orders_fname):
        orders = []
    else:
        with open(orders_fname) as orders_file:
            orders = json.load(orders_file)

    if request.method == 'POST':
        try:
            order = Order(**request.get_json(force=True)).dict()
        except ValidationError as e:
            return e.json(), 400
        order['id'] = len(orders) + 1
        orders.append(order)
        with open(orders_fname, 'w') as orders_file:
            json.dump(orders, orders_file)
        return order

    return jsonify(orders)


@app.route('/price', methods=['POST'])
def price():
    try:
        order = Order(**request.json)
    except ValidationError as e:
        abort(400, {'errors': e.json()})
    return 42


@app.route('/toppings')
def toppings():
    return jsonify([t.value for t in Topping])
