import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import Qt, QPointF

class ZPlastyPracticeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Z-Plasty Practice")

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("#ffe0bd"))  # Skin color
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 400, 400)

        self.scar_button = QPushButton("Add Scar")
        self.scar_button.clicked.connect(self.add_scar)

        self.zplasty_button = QPushButton("Z-plasty")
        self.zplasty_button.clicked.connect(self.add_zplasty)

        self.angle_label = QLabel("Angle:")
        self.angle_input = QLineEdit()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_canvas)

        self.repair_button = QPushButton("Repair Scar")
        self.repair_button.clicked.connect(self.repair_scar)
        
        self.pct_gain_label = QLabel("Percentage Gain:")

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.scar_button)
        layout.addWidget(self.angle_label)
        layout.addWidget(self.angle_input)
        layout.addWidget(self.zplasty_button)
        layout.addWidget(self.repair_button)
        layout.addWidget(self.pct_gain_label)
        layout.addWidget(self.reset_button)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.scar_added = False

    def add_scar(self):
        if not self.scar_added:
            line_length = 200  # Adjust the length of the line as needed
            line_center = 200  # Y-coordinate of the center of the canvas

            # Calculate the x-coordinates of the endpoints to make the line shorter
            x1 = (400 - line_length) // 2  # Start point
            x2 = (400 + line_length) // 2  # End point

            pen = QPen(Qt.red, 1, Qt.DashLine)
            pen.setWidth(1)  # Adjust the thickness of the line as needed
            self.scene.addLine(x1, line_center, x2, line_center, pen)
            self.scar_added = True

    def add_zplasty(self):
        if self.scar_added:
            angle = float(self.angle_input.text())

            # Calculate coordinates for the Z-plasty lines
            scar_center_x = 200
            scar_width = 200
            scar_height = 10
            scar_top = 200 - scar_height / 2
            scar_bottom = 200 + scar_height / 2
            scar_middle = 200 - scar_height / 100
            scar_left = scar_center_x - scar_width / 2
            scar_right = scar_center_x + scar_width / 2

            # Draw the lines going up and to the right
            line_length = 200

            # Calculate the endpoint for the line going up and to the right
            pent = QPen(Qt.blue, 1, Qt.DashLine)
            angle_radians = math.radians(angle)
            line_end_x_up = scar_left + line_length * math.cos(angle_radians)
            line_end_y_up = scar_middle - line_length * math.sin(angle_radians)
            self.scene.addLine(scar_left, scar_middle, line_end_x_up, line_end_y_up, pent)

            # Calculate the endpoint for the line coming down and to the left
            penb = QPen(Qt.blue, 1, Qt.DashLine)
            angle_radians = math.radians(angle)
            line_end_x_down = scar_right - line_length * math.cos(angle_radians)
            line_end_y_down = scar_middle + line_length * math.sin(angle_radians)
            self.scene.addLine(scar_right, scar_middle, line_end_x_down, line_end_y_down, penb)

    def repair_scar(self):
        if self.scar_added:
            angle = float(self.angle_input.text())

            #Calculate coordinates of revision lines
            scar_length = 200*(1+((5/3*(angle)-25)/100)) # calculates the % length increase depending on angle
            scar_center = 200
            pct_gain = (scar_length - 200) / 200 * 100
            self.pct_gain_label.setText("Percentage Gain: {:.2f}%".format(pct_gain))


            # Calculate the x-coordinates of the endpoints to make the line shorter
            x1 = (400 - scar_length) // 2  # Start point
            x2 = (400 + scar_length) // 2  # End point

            pen = QPen(Qt.gray, 1, Qt.DashLine)
            pen.setWidth(2)  # Adjust the thickness of the line as needed
            self.scene.addLine(x1, scar_center, x2, scar_center, pen)
            self.scar_added = True

            #calculate new line going up to the right
            line_length = 200
            pent = QPen(Qt.red)
            pent.setWidth(2)
            angle_radians = math.radians(angle)
            line_end_x_up = x1 + line_length * math.sin(angle_radians)
            line_end_y_up = scar_center - line_length * math.cos(angle_radians)
            self.scene.addLine(x1, scar_center, line_end_x_up, line_end_y_up, pent)

            # Calculate the endpoint for the line coming down and to the left
            penb = QPen(Qt.red)
            penb.setWidth(2)
            angle_radians = math.radians(angle)
            line_end_x_down = x2 - line_length * math.sin(angle_radians)
            line_end_y_down = scar_center + line_length * math.cos(angle_radians)
            self.scene.addLine(x2, scar_center, line_end_x_down, line_end_y_down, penb)

            # Calculate the new line crossing the original scar
            penc = QPen(Qt.blue)
            penc.setWidth(2)
            self.scene.addLine(line_end_x_up, line_end_y_up, line_end_x_down, line_end_y_down, penc)

    def reset_canvas(self):
        self.scene.clear()
        self.scar_added = False
        self.angle_input.clear()
        self.angle_label.clear()


def main():
    app = QApplication(sys.argv)
    window = ZPlastyPracticeApp()
    window.setGeometry(100, 100, 400, 500)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()