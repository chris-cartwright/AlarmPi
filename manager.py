import json


ALARMS_JSON = 'alarms.json'
VERSION = 1

__loaders = {}

alarms = []


def loader(version):
    def _decorator(func):
        __loaders[version] = func
        return func

    return _decorator


class Alarm:
    __next_id = 0

    def __init__(self, hour, minute):
        Alarm.__next_id += 1
        self.__id = Alarm.__next_id

        self.hour = hour
        self.minute = minute

    @property
    def id(self):
        return self.__id

    def serialize(self):
        return {
            'id': self.__id,
            'hour': self.hour,
            'minute': self.minute
        }

    @staticmethod
    def deserialize(obj):
        a = Alarm(obj['hour'], obj['minute'])
        a.__id = obj['id']

        # Make sure max is always larger than any alarm
        Alarm.__next_id = max(Alarm.__next_id, a.__id)

        return a



@loader(1)
def __load_v1(data):
    global alarms

    alarms = [Alarm.deserialize(a) for a in data]

def load():
    global alarms

    try:
        with open(ALARMS_JSON, 'r') as infile:
            data = json.load(infile)
            __loaders[data['version']](data['alarms'])
    except IOError:
        alarms = []


def save():
    global alarms

    with open(ALARMS_JSON, 'w') as outfile:
            json.dump({ "version": VERSION, "alarms": [a.serialize() for a in alarms] }, outfile)
