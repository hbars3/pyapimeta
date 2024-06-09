from flask import Flask, render_template
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

    prueba1 = ChawyLog(text='Mensaje de prueba 1')
    prueba2 = ChawyLog(text='Mensaje de prueba 2')
    db.session.add(prueba1)
    db.session.add(prueba2)
    db.session.commit()


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)