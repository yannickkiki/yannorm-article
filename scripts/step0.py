class BaseManager:

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names):
        pass

    def bulk_insert(self, rows: list):
        pass

    def update(self, new_data: dict):
        pass

    def delete(self):
        pass


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""


# ----------------------- Usage ------------------------------ #
class Employee(BaseModel):
    table_name = "employees"


employees = Employee.objects.select('salary', 'grade')
