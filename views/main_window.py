import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QMenuBar, QAction,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
)
from controllers import employee_controller
from views.about_page import AboutPage
from PyQt5.QtCore import Qt

class EmployeeForm(QWidget):
    # [Same as previous EmployeeForm code, or use QDialog instead if preferred]
    # For brevity, we assume the EmployeeForm code from the previous sample.
    pass

class EmployeeFormDialog(QDialog):
    def __init__(self, employee=None, parent=None):
        """
        :param employee: a dict with keys ('name', 'department', 'position', 'contact', 'base_salary')
                         if editing an existing employee; otherwise None.
        """
        super().__init__(parent)
        self.setWindowTitle("Employee Form")
        self.resize(300, 200)
        self.employee = employee  # This holds the existing data for editing, if any.
        self.initUI()
    
    def initUI(self):
        self.layout = QFormLayout(self)
        
        # Create line edits for each field.
        self.name_edit = QLineEdit(self)
        self.dept_edit = QLineEdit(self)
        self.position_edit = QLineEdit(self)
        self.contact_edit = QLineEdit(self)
        self.salary_edit = QLineEdit(self)
        
        # If editing, pre-populate fields.
        if self.employee:
            self.name_edit.setText(self.employee.get("name", ""))
            self.dept_edit.setText(self.employee.get("department", ""))
            self.position_edit.setText(self.employee.get("position", ""))
            self.contact_edit.setText(self.employee.get("contact", ""))
            self.salary_edit.setText(str(self.employee.get("base_salary", "")))
        
        self.layout.addRow("Name:", self.name_edit)
        self.layout.addRow("Department:", self.dept_edit)
        self.layout.addRow("Position:", self.position_edit)
        self.layout.addRow("Contact:", self.contact_edit)
        self.layout.addRow("Base Salary:", self.salary_edit)
        
        # Dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)
    
    def get_data(self):
        """Return a dictionary with form data."""
        try:
            salary = float(self.salary_edit.text())
        except ValueError:
            salary = 0.0
        return {
            "name": self.name_edit.text(),
            "department": self.dept_edit.text(),
            "position": self.position_edit.text(),
            "contact": self.contact_edit.text(),
            "base_salary": salary
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.resize(800, 600)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create Menu Bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.open_about_page)
        menu_bar.addAction(about_action)

        # Buttons Layout
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Employee")
        self.edit_button = QPushButton("Edit Employee")
        self.delete_button = QPushButton("Delete Employee")
        self.refresh_button = QPushButton("Refresh")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.refresh_button)
        self.layout.addLayout(self.button_layout)

        self.add_button.clicked.connect(self.add_employee)
        self.edit_button.clicked.connect(self.edit_employee)
        self.delete_button.clicked.connect(self.delete_employee)
        self.refresh_button.clicked.connect(self.load_employees)

        # Table for Employee Records
        self.table = QTableWidget(0, 6, self)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Department", "Position", "Contact", "Base Salary"])
        self.layout.addWidget(self.table)

        self.load_employees()

    def load_employees(self):
        self.table.setRowCount(0)
        employees = employee_controller.get_all_employees()
        for emp in employees:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(emp.id)))
            self.table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.table.setItem(row, 2, QTableWidgetItem(emp.department))
            self.table.setItem(row, 3, QTableWidgetItem(emp.position))
            self.table.setItem(row, 4, QTableWidgetItem(emp.contact))
            self.table.setItem(row, 5, QTableWidgetItem(str(emp.base_salary)))

    def add_employee(self):
        dialog = EmployeeFormDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                employee_controller.add_employee(**data)
                self.load_employees()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def edit_employee(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "Please select an employee to edit.")
            return
        emp_id = int(self.table.item(selected, 0).text())
        # Fetch the existing record from your controller
        employees = employee_controller.get_all_employees()
        employee_obj = next((emp for emp in employees if emp.id == emp_id), None)
        if employee_obj:
            # Create a dict with the current employee details.
            emp_data = {
                "name": employee_obj.name,
                "department": employee_obj.department,
                "position": employee_obj.position,
                "contact": employee_obj.contact,
                "base_salary": employee_obj.base_salary
            }
            dialog = EmployeeFormDialog(employee=emp_data, parent=self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                try:
                    employee_controller.update_employee(emp_id, **data)
                    self.load_employees()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def delete_employee(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "Please select an employee to delete.")
            return
        emp_id = int(self.table.item(selected, 0).text())
        confirm = QMessageBox.question(self, "Confirm", f"Delete employee ID {emp_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                employee_controller.delete_employee(emp_id)
                self.load_employees()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def open_about_page(self):
        self.about_page = AboutPage(self)
        self.about_page.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
