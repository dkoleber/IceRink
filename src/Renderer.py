import math
import random
import sys
import threading
from typing import List

import pyximport
from PyQt5.QtCore import QEvent, Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget

pyximport.install()
from Engine import Engine, Mass


class WorldView(QWidget):
    def __init__(self, reference_engine:Engine, bounds=(1000,1000)):
        super().__init__()
        self.setGeometry(100, 100, bounds[0], bounds[1])
        self.show()
        self.count = 0
        self.reference_engine = reference_engine

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 60)

    def paintEvent(self, event:QEvent):
        painter = QPainter()
        painter.begin(self)
        self.paint(event, painter)
        painter.end()
    def paint(self, event:QEvent, painter: QPainter):
        for entity in self.reference_engine.entities:
            alpha = math.tanh(entity.density) * 255
            painter.setBrush(QColor(100, 200, 50, alpha))
            painter.setPen(QColor(100, 200, 50, alpha))
            painter.drawEllipse(QPoint(entity.x, entity.y), entity.radius, entity.radius)

    def mousePressEvent(self, event:QEvent):
        x = event.pos().x()
        y = event.pos().y()
        for entity in self.reference_engine.entities:
            if entity.contains_point(x, y):
                new_mass = entity.eject(int(entity.amount / 2), entity.density, random.randint(-2, 2), random.randint(-2, 2))
                if new_mass != None:
                    self.reference_engine.add_mass(new_mass)
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
