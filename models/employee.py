from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    contact = Column(String(50))
    base_salary = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Employee(name={self.name}, department={self.department}, position={self.position})>"
