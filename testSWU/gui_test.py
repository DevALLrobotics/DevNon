import sys,requests
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QIcon
app = QApplication([])
window = QWidget()
window.setWindowTitle("Reachy-Controller")
window.setFixedSize(400, 200)  # width, height
   # width, height
window.setStyleSheet("QPushButton { font-size: 20px; }")
window.setWindowIcon(QIcon("logo.png"))
def test1():
    x="1"
    # url = "http://127.0.0.1:5000/receive"
    url = "http://172.20.10.5:5000/receive"
    data = {"name": "Kin", "data": x}
    response = requests.post(url, json=data)
    print(response.json())
def test2():
    x="2"
    url = "http://127.0.0.1:5000/receive"
    data = {"name": "Kin", "data": x}
    response = requests.post(url, json=data)
    print(response.json()) 
def test3():
    x="3"
    url = "http://127.0.0.1:5000/receive"
    data = {"name": "Kin", "data": x}
    response = requests.post(url, json=data)
    print(response.json())
layout = QVBoxLayout()
button1=QPushButton("ACTION1")
button2=QPushButton("ACTION2")
button3=QPushButton("ACTION3")
button1.setMinimumHeight(60)
button2.setMinimumHeight(60)
button3.setMinimumHeight(60)

layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)
button1.clicked.connect(test1)
button2.clicked.connect(test2)
button3.clicked.connect(test3)
window.setLayout(layout)
window.show()
sys.exit(app.exec())