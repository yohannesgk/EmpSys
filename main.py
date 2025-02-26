import sys
from PyQt5.QtWidgets import QApplication
from utils.db import engine
from models.employee import Base
from views.main_window import MainWindow

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 
