import psycopg2


# ------------ Manager (Model objects handler) ------------ #
class BaseManager:
    database_settings = {}

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000):
        # Build SELECT query
        fields_format = ', '.join(field_names)
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"

        # Execute query
        connection = psycopg2.connect(**self.database_settings)
        cursor = connection.cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution
        # and transform it into `model_class` objects.
        # The fetching is done by batches of `chunk_size` to
        # avoid to run out of memory.
        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(result) < chunk_size

        return model_objects

    def bulk_insert(self, rows: list):
        pass

    def update(self, new_data: dict):
        pass

    def delete(self):
        pass


# ----------------------- Model ----------------------- #
class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>"


# ----------------------- Setup ----------------------- #
DB_SETTINGS = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'ormify',
    'user': 'yank',
    'password': 'yank'
}

BaseManager.database_settings = DB_SETTINGS


# ----------------------- Usage ----------------------- #
class Employee(BaseModel):
    manager_class = BaseManager
    table_name = "employees"


# SQL: SELECT salary, grade FROM employees;
employees = Employee.objects.select('salary', 'grade')  # employees: List[Employee]
print(employees)
