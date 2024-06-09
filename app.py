from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ChawyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())
    text = db.Column(db.TEXT)


with app.app_context():
    db.create_all()


def sort_by_datetime(registers):
    return sorted(registers, key=lambda x: x.datetime, reverse=True)


@app.route('/')
def index():
    registers = ChawyLog.query.all()
    sorted_registers = sort_by_datetime(registers)
    return render_template('index.html', registers=sorted_registers)


log_messages = []


def add_log_message(text):
    log_messages.append(text)
    new_log = ChawyLog(text=text)
    db.session.add(new_log)
    db.session.commit()

# add_log_message("Test 1")


TOKEN = "tocket-poc"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = verify_token(request)
        return challenge
    elif request.method == 'POST':
        response = receive_messages(request)
        return response


def verify_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN:
        return challenge
    else:
        return jsonify({'error': 'Invalid Token'}), 401


def receive_messages(req):
    req = req.get_json()
    add_log_message(req)
    return jsonify({'message': 'EVENT_RECEIVED'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)