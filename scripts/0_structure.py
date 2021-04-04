# ------------ Manager (Model objects handler) ------------ #
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


# ----------------------- Usage ----------------------- #
class Employee(BaseModel):
    manager_class = BaseManager
    table_name = "employees"


# # SQL: SELECT salary, grade FROM employees;
# employees = Employee.objects.select('salary', 'grade')  # employees: List[Employee]
#
#
# # SQL: INSERT INTO employees (first_name, last_name, salary)
# #  	VALUES ('Yan', 'KIKI', 10000), ('Yoweri', 'ALOH', 15000);
# employees_data = [
#     {"first_name": "Yan", "last_name": "KIKI", "salary": 10000},
#     {"first_name": "Yoweri", "last_name": "ALOH", "salary": 15000}
# ]
# Employee.objects.bulk_insert(rows=employees_data)
#
#
# # SQL: UPDATE employees SET salary = 17000, grade = 'L2';
# Employee.objects.update(
#     new_data={'salary': 17000, 'grade': 'L2'}
# )
#
#
# # SQL: DELETE FROM employees;
# Employee.objects.delete()
