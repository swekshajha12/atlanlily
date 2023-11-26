from infrastructure.local_database import LocalDatabase

class DatabaseWriter:
    def __init__(self, storage_path):
        self.local_database = LocalDatabase(storage_path)

    def write_to_database(self, data):
        self.local_database.write_to_database(data)