from models.employee import Employee
from utils.db import SessionLocal

def get_all_employees():
    db = SessionLocal()
    try:
        employees = db.query(Employee).all()
        return employees
    finally:
        db.close()

def add_employee(name, department, position, contact, base_salary):
    db = SessionLocal()
    try:
        new_emp = Employee(
            name=name,
            department=department,
            position=position,
            contact=contact,
            base_salary=base_salary
        )
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def update_employee(emp_id, **kwargs):
    db = SessionLocal()
    try:
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            return None
        for key, value in kwargs.items():
            setattr(emp, key, value)
        db.commit()
        return emp
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def delete_employee(emp_id):
    db = SessionLocal()
    try:
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            return False
        db.delete(emp)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
 
