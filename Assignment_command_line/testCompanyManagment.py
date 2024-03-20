import unittest
from CompanyManagement import CompanyManager, EmployeeManager

class TestEmployeeManagementSystem(unittest.TestCase):
    def setUp(self):
        self.CM = CompanyManager()

    def test_add_department(self):
        self.CM.addDepartment("IT")
        self.assertIn("IT", self.CM.departments)

    def test_remove_department(self):
        self.CM.addDepartment("IT")
        self.CM.removeDepartment("IT")
        self.assertNotIn("IT", self.CM.departments)

    def test_add_employee_to_department(self):
        self.CM.addDepartment("IT")
        emp1 = EmployeeManager("Tanmay", "1", "Software Engineer", "IT")
        self.CM.departments["IT"].addEmployee(emp1)
        self.assertIn(emp1, self.CM.departments["IT"].employees)

    def test_remove_employee_from_department(self):
        self.CM.addDepartment("IT")
        emp1 = EmployeeManager("Tanmay", "1", "Software Engineer", "IT")
        self.CM.departments["IT"].addEmployee(emp1)
        self.CM.departments["IT"].removeEmployee(emp1)
        self.assertNotIn(emp1, self.CM.departments["IT"].employees)

    def test_list_employees_in_department(self):
        self.CM.addDepartment("IT")
        emp1 = EmployeeManager("Tanmay", "1", "Software Engineer", "IT")
        emp2 = EmployeeManager("Gopal", "2", "Data Scientist", "IT")
        emp3 = EmployeeManager("Mayank", "3", "Data Scientist", "IT")
        emp4 = EmployeeManager("Payal", "4", "Software Engineer", "IT")
        emp5 = EmployeeManager("Monalisa", "5", "Data Analyst", "IT")
        self.CM.departments["IT"].addEmployee(emp1)
        self.CM.departments["IT"].addEmployee(emp2)
        self.CM.departments["IT"].addEmployee(emp3)
        self.CM.departments["IT"].addEmployee(emp4)
        self.CM.departments["IT"].addEmployee(emp5)
        self.assertIn(emp1, self.CM.departments["IT"].employees)
        self.assertIn(emp2, self.CM.departments["IT"].employees)
        self.assertIn(emp3, self.CM.departments["IT"].employees)
        self.assertIn(emp4, self.CM.departments["IT"].employees)
        self.assertIn(emp5, self.CM.departments["IT"].employees)

if __name__ == "__main__":
    unittest.main()
