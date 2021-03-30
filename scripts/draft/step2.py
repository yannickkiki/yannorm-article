# ---------------------------  Core  ------------------------------ #
import psycopg2


class BaseManager:
    connection = None

    def __init__(self, model_class):
        self.model_class = model_class

    @classmethod
    def set_connection(cls, database_settings):
        connection = psycopg2.connect(**database_settings)
        connection.autocommit = True  # https://www.psycopg.org/docs/connection.html#connection.commit
        cls.connection = connection

    def select(self, *field_names, chunk_size=2000):
        # Build SELECT query
        fields_format = ', '.join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"

        # Execute query
        cursor = self.connection.cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution and transform
        # it into `model_class` objects.
        # The fetching is done by batches to avoid to run out of memory.
        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            rows = cursor.fetchmany(size=chunk_size)
            for row in rows:
                keys, values = field_names, row
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(rows) < chunk_size

        return model_objects


class BaseModel:
    manager_class = BaseManager
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    @classmethod
    def get_manager(cls):
        return cls.manager_class(model_class=cls)


# ---------------------- Database config -------------------------- #


DB_SETTINGS = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'ormify',
    'user': 'yank',
    'password': 'yank'
}

BaseManager.set_connection(database_settings=DB_SETTINGS)


# ------------------------- Models -------------------------------- #


class Employee(BaseModel):
    table_name = "employees"
    manager_class = BaseManager


# ------------------------- Main code ----------------------------- #

employees = Employee.get_manager().select('salary', 'grade')
print(employees)
