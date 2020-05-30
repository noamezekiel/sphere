from furl import furl
import json
from .. import db_drivers

class Saver():
    """
    Saver that saves data to the database
    
    :param db_url: The database URL, in the format: `db_name://host:port/`.
    :type db_url: str
    """
    def __init__(self, db_url):
        """
        Constructor method.
        """
        f = furl(db_url)
        db, db_host, db_port = f.scheme, f.host, f.port
        self._driver = db_drivers[db].Driver(db_host, db_port)

    def __repr__(self):
    	return f'Saver(db_url={self.db_url})'

    def save(self, topic, raw_data):
        """
        Saves the raw data of the specified topic to the database.
        
        :param topic: The topic of the data
        :type topic: str
        :param raw_data: The raw data to be saved
        :type raw_data: json
        """ 
        data = json.loads(raw_data)
        self._driver.save(topic, data)
