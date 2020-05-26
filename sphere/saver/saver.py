from furl import furl
import json
from .. import db_drivers

class Saver():
    def __init__(self, db_url):
        f = furl(db_url)
        db, db_host, db_port = f.scheme, f.host, f.port
        self._driver = db_drivers[db].Driver(db_host, db_port)

    def save(self, topic, raw_data):
        data = json.loads(raw_data)
        self._driver.save(topic, data)
