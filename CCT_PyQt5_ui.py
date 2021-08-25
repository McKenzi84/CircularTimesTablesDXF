from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import dtype
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import random
import numpy as np

        

class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        uic.loadUi('cct.ui', self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas = self.findChild(FigureCanvas, 'graphWidget')
        

        self.radius = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.radius.setValidator(QDoubleValidator(0.99,99.999,4))
        self.lines = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
        self.lines.setValidator(QDoubleValidator(0.99,99.999,4))
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        
        self.button.clicked.connect(self.plot)
        self.button1.clicked.connect(self.plot_1)
        
        #self.canvas = self.findChild(QtWidgets.QWidget, 'graphWidget')
        

      
    
        self.show()

    def test_print(self):

        print('Works')

    def plot(self):
        
        self.graphWidget.clear()

        #a = int(self.radius.text())
        #b = int(self.lines.text())

        x = np.random.randint(1, 20, 5, dtype=int)
        y = np.random.randint(20, 200, 5, dtype=int)
        self.graphWidget.plot(x, y, symbol='o')

    def plot_1(self):

        doc = ezdxf.new("R2000")
        msp = doc.modelspace()
        msp.add_circle(center=(0,0), radius=10)
        ax = self.figure.add_subplot(111)
        ctx = RenderContext(doc)
        ctx.current_layout.set_colors(bg='#FFFFFF')
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc.modelspace())

        #self.canvas.draw()
        #self.graphWidget.plot()
        #plt.show()
        #self.graphWidget.plot()


    

app = QtWidgets.QApplication(sys.argv)
window = Ui()

app.exec_()