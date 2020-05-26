from . import client_drivers


class Reader():
    def __init__(self, path, file_format):
        # create an instance of the right driver
        self.driver = client_drivers[file_format].Driver(path)
        self.user = self.driver.get_user()

    def __iter__(self):
        for snapshot in self.driver.snapshots():
            yield snapshot
