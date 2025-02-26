from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QDialogButtonBox
from PyQt5.QtCore import Qt

class AboutPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Team")
        self.setModal(True)  # Make the dialog modal.
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Header label (centered and styled)
        header = QLabel("Team Members")
        header.setStyleSheet("font-size: 16pt; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Table for team members (non-editable)
        self.table = QTableWidget(0, 2, self)
        self.table.setHorizontalHeaderLabels(["Name", "Student ID"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table cells read-only
        layout.addWidget(self.table)

        # Example team data; replace with your actual team details.
        team_members = [
            {"name": "Alice Smith", "student_id": "S12345"},
            {"name": "Bob Johnson", "student_id": "S23456"},
            {"name": "Charlie Brown", "student_id": "S34567"},
            {"name": "Dana White", "student_id": "S45678"},
        ]
        self.table.setRowCount(len(team_members))
        for row, member in enumerate(team_members):
            self.table.setItem(row, 0, QTableWidgetItem(member["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(member["student_id"]))

        # DialogButtonBox with a Close button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Close)
        self.button_box.rejected.connect(self.reject)  # Close dialog when button is clicked.
        layout.addWidget(self.button_box)
