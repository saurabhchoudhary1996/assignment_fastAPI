import json
import os

defaultPath = os.path.dirname(os.path.abspath(__file__))
filePath = os.path.join(defaultPath, 'companyManagement.json')

# Employee Manager class to represent individual employees
class EmployeeManager:
    def __init__(self, employeeName, employeeID, title, department):
        self.employeeName = employeeName
        self.employeeID = employeeID
        self.title = title
        self.department = department

    # Method to display employee details
    def display_details(self):
        print(f"Name: {self.employeeName}, ID: {self.employeeID}, Title: {self.title}, Department: {self.department}")
    
    # String representation of an employee (name and ID)
    def __str__(self):
        return f"{self.employeeName} - ID: {self.employeeID}"

# Department Manager class to represent departments and manage that departments employees
class DepartmentManager:
    def __init__(self, departmentName):
        self.departmentName = departmentName
        self.employees = []

    # Method to add an employee to the department
    def addEmployee(self, employee):
        self.employees.append(employee)

    # Method to remove an employee to the department
    def removeEmployee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
            print(f"Employee {employee.employeeName} removed from department {self.departmentName}")
        else:
            print(f"Employee {employee.employeeName} is not in department {self.departmentName}")

    # Method to list all employees in the department
    def fetchEmployeesList(self):
        print(f"Employees in department {self.departmentName}:")
        for employee in self.employees:
            print(employee)

# Company Manager class to manage departments and it's employees
class CompanyManager:
    def __init__(self):
        self.departments = {}

    # Method to add a new department to the company
    def addDepartment(self, departmentName):
        if departmentName not in self.departments:
            self.departments[departmentName] = DepartmentManager(departmentName)
            print(f"Department {departmentName} added successfully")
        else:
            print(f"Department {departmentName} already exists")

    # Method to remove a department from the company
    def removeDepartment(self, departmentName):
        if departmentName in self.departments:
            del self.departments[departmentName]
            print(f"Department {departmentName} removed successfully")
        else:
            print(f"Department {departmentName} does not exist")

    # Method to display all departments in the company
    def fetchDepartmentList(self):
        for departmentName in self.departments:
            print(departmentName)

    # Save data into json file
    def saveDataInFile(self):
        convertToDict = self.convertToDict()
        with open(filePath, 'w') as f:
            json.dump(convertToDict, f, indent=4)

    # Load json file add into objects 
    def loadFile(self):
        try:
            with open(filePath, 'r') as f:
                companyDict = json.load(f)
            self.convertToObject(companyDict)
        except FileNotFoundError:
            print("File not found")
        except json.decoder.JSONDecodeError:
            print("Invalid JSON format")
    
    def convertToDict(self):
        companyDict = {}
        for departmentName in self.departments:
            companyDict[departmentName] = [{'employeeName':employee.employeeName,'employeeID':employee.employeeID,'title':employee.title}for employee in self.departments[departmentName].employees]
        return companyDict
    
    def convertToObject(self, companyDict):
        for departmentName in companyDict:
            # self.departments[departmentName] = 
            DM = DepartmentManager(departmentName = departmentName)
            for employee in companyDict[departmentName]:
                DM.addEmployee(EmployeeManager(employeeName=employee['employeeName'], employeeID=employee['employeeID'], title=employee['title'], department = departmentName))
            self.departments[departmentName] = DM
        print('Done')
    
    

# Show menu
def menu():
    print("\n Employee Management System Menu:")
    print("1 - Add Employee in department")
    print("2 - Remove Employee from department")
    print("3 - List Employees in Department")
    print("4 - Add Department")
    print("5 - Remove Department")
    print("6 - List Departments")
    print("7 - Exit")


def main():
    company = CompanyManager()
    company.loadFile()

    while True:
        menu()
        option = input("Enter your option: ")

        if option == '1':
            name = input("Enter employee name: ")
            employeeID = input("Enter employee ID: ")
            title = input("Enter employee title: ")
            department = input("Enter employee department: ")
            employee = EmployeeManager(name, employeeID, title, department)
            if department in company.departments:
                company.departments[department].addEmployee(employee)
            else:
                print(f"Department {department} does not exist")

        elif option == '2':
            department = input("Enter department name: ")
            if department in company.departments:
                print(f"Employees in department {department}:")
                company.departments[department].fetchEmployeesList()
                employeeID = input("Enter employee ID to remove: ")
                employee_to_remove = None
                for employee in company.departments[department].employees:
                    if employee.employeeID == employeeID:
                        employee_to_remove = employee
                        break
                if employee_to_remove:
                    company.departments[department].removeEmployee(employee_to_remove)
                else:
                    print(f"Employee with ID {employeeID} not found in department {department}")
            else:
                print(f"Department {department} does not exist")

        elif option == '3':
            department = input("Enter department name: ")
            if department in company.departments:
                company.departments[department].fetchEmployeesList()
            else:
                print(f"Department {department} does not exist")

        elif option == '4':
            departmentName = input("Enter department name to add: ")
            company.addDepartment(departmentName)

        elif option == '5':
            departmentName = input("Enter department name to remove: ")
            company.removeDepartment(departmentName)

        elif option == '6':
            company.fetchDepartmentList()

        elif option == '7':
            company.saveDataInFile()
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
