from flask import Flask, jsonify, request

import manager

app = Flask(__name__)

def _find(id):
    matching = [a for a in manager.alarms if a.id == id]
    if len(matching) == 0 or len(matching) > 1:
        raise IndexError()

    return matching[0]


def _read(id):
    return jsonify(_find(id).serialize())


def _update(id):
    a = _find(id)
    a.hour = request.form['hour']
    a.minute = request.form['minute']
    manager.save()
    return jsonify(id)


def _delete(id):
    manager.alarms = [a for a in manager.alarms if a.id != id]
    manager.save()
    return jsonify(id)


@app.route('/alarm/list', methods=['GET'])
def list_all():
    return jsonify([a.serialize() for a in manager.alarms])


@app.route('/alarm/<int:id>', methods=['GET', 'POST', 'DELETE'])
def read_update_delete(id):
    if request.method == 'GET':
        return _read(id)
    elif request.method == 'POST':
        return _update(id)
    elif request.method == 'DELETE':
        return _delete(id)


@app.route('/alarm/create', methods=['POST'])
def create():
    alarm = manager.Alarm(request.form['hour'], request.form['minute'])
    manager.alarms.append(alarm)
    manager.save()

    return jsonify(alarm.id)


@app.route('/', methods=['GET'])
def index():
    return jsonify('AlarmPi v0.1')