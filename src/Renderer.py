import math
import random
import sys
import threading
from typing import List

import pyximport
from PyQt5.QtCore import QEvent, Qt, QTimer, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

pyximport.install()
from Engine import Engine, Mass



default_density = 1

class WorldView(QWidget):
    def __init__(self, reference_engine:Engine, bounds=(1000,1000)):
        super().__init__()

        self.bounds = bounds
        self.count = 0
        self.engine = reference_engine

        self.initUI()

    def initUI(self):
        button_width = 500
        button_height = 100

        self.setGeometry(100, 100, self.bounds[0] + button_width, self.bounds[1])

        split_button = QPushButton('Split All', self)
        split_button.setGeometry(self.bounds[0], button_height * 0, button_width, button_height)
        split_button.clicked.connect(self.splitAll)

        self.count_label = QLabel(self)
        self.count_label.setGeometry(self.bounds[0], button_height * 1, button_width, button_height)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 60)

        self.show()

    def paintEvent(self, event:QEvent):
        painter = QPainter()
        painter.begin(self)
        self.paint(event, painter)
        painter.end()
    def paint(self, event:QEvent, painter: QPainter):
        self.count_label.setText(str(len(self.engine.entities)))
        for entity in self.engine.entities:
            alpha = math.tanh(entity.density) * 255
            painter.setBrush(QColor(100, 200, 50, alpha))
            painter.setPen(QColor(100, 200, 50, alpha))
            painter.drawEllipse(QPoint(entity.x, entity.y), entity.radius, entity.radius)

    @pyqtSlot()
    def splitAll(self):
        for entity in self.engine.entities:
            new_mass = entity.eject(int(entity.amount / 2), default_density, random.randint(-2, 2), random.randint(-2, 2))

            if new_mass is not None:
                self.engine.add_mass(new_mass)
        print(len(self.engine.entities))

    def mousePressEvent(self, event:QEvent):
        x = event.pos().x()
        y = event.pos().y()
        for entity in self.engine.entities:
            if entity.contains_point(x, y):
                new_mass = entity.eject(int(entity.amount / 2), entity.density, random.randint(-2, 2), random.randint(-2, 2))
                if new_mass != None:
                    self.engine.add_mass(new_mass)
                break


class Renderer(threading.Thread):
    def __init__(self, reference_engine:Engine, bounds=(1000,1000)):
        super().__init__()
        self.engine = reference_engine
        self.is_running = False
        self.bounds = bounds

    def run(self):
        self.is_running = True
        self.application = QApplication([])
        self.world_view = WorldView(self.engine, self.bounds)
        self.application.exec_()
        # sys.exit(self.application.exec_())
        self.is_running = False
