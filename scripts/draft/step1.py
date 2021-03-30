# ---------------------------  Core  ------------------------------ #
class BaseManager:

    def __init__(self, model_class, database_settings):
        self.model_class = model_class
        self.table_name = model_class.table_name
        self.database_settings = database_settings


class BaseModel:
    manager_class = BaseManager
    table_name = ""

    @classmethod
    def get_manager(cls, database_settings):
        return cls.manager_class(model_class=cls, database_settings=database_settings)


# ---------------------- Database config -------------------------- #

DB_SETTINGS = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'ormify',
    'user': 'yank',
    'password': 'yank'
}

# ------------------------- Models -------------------------------- #


class Employee(BaseModel):
    table_name = "employees"


# ------------------------- Main code ----------------------------- #

manager = Employee.get_manager(database_settings=DB_SETTINGS)
