from . import client_drivers


class Reader():
    """ Reader of a file.
    :param path: The path to the file
    :type path: str
    :param file_format: The format of the file
    :type file_format: str
    """
    def __init__(self, path, file_format):
        # create an instance of the right driver
        self.driver = client_drivers[file_format].Driver(path)
        self.user = self.driver.get_user()

    def __repr__(self):
    	return f'Reader(path={self.path}, file_format={self.file_format})'

    def __iter__(self):
        for snapshot in self.driver.snapshots():
            yield snapshot
