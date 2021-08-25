import ezdxf
import matplotlib.pyplot as plt
import math
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


lines = 50
m = 50
n = 2
r = 100
b = 360/m
d = (-b)
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import ezdxf 
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from PyQt5 import QtWidgets
import math


class Window(QDialog):
     
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(900,800)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
        self.label_point = QLabel('How many points around the circle:')
        self.points = QLineEdit('50')
        self.label_lines = QLabel('How many lines:')
        self.lines = QLineEdit('50')
        self.label_factor = QLabel('Factor:')
        self.factor = QLineEdit('3')
        self.button.clicked.connect(self.embedded_plot)
 
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.toolbar)
        self.layout1.addWidget(self.button)
        self.layout1.addWidget(self.canvas)
        self.layout1.addWidget(self.label_point)
        self.layout1.addWidget(self.points)
        self.layout1.addWidget(self.label_lines)
        self.layout1.addWidget(self.lines)
        self.layout1.addWidget(self.label_factor)
        self.layout1.addWidget(self.factor)               
        self.setLayout(self.layout1)

    def coordinates(self):      
        m =  int(self.points.text())       
        r = 10 # circle radius
        b = 360/m
        d = (-b)
        points = []
        for x in range(m):
            d += b
            cor_x = r * math.cos(math.radians(d))
            cor_y = r * math.sin(math.radians(d))
    
            points.append((cor_x, cor_y))
        return points

    def embedded_plot(self):
        doc = ezdxf.new('R2000')
        msp = doc.modelspace()
        points = self.coordinates()
        n = int(self.factor.text())
        m =  int(self.points.text())
        lines = int(self.lines.text())
        r = 10
        b=360/m
        d = (-b)

        for y in range(lines):
            z = y * n 
            if z < m : 
                msp.add_line(start=(points[y]), end=(points[z]))
            elif z > m : 
                q = z // m
            #print(z // m)
                z = y * n - ((q * m)) 
                msp.add_line(start=(points[y]), end=(points[z]))
            elif z == lines: 
                z = 0
                msp.add_line(start=(points[y]), end=(points[z]))

        for index, item in enumerate (points):
            if item[0] > 0 and item[1] > 0:
                msp.add_text(index, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((item[0], item[1]), align='LEFT')
            elif item[0] < 0  and item[1] > 0:
                msp.add_text(index, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((item[0], item[1]), align='RIGHT')
            elif item[0] < 0  and item[1] < 0:
                msp.add_text(index, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((item[0], item[1]), align='TOP_RIGHT')
            elif item[0] > 0  and item[1] < 0:
                msp.add_text(index, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((item[0], item[1]), align='TOP_LEFT')

        msp.add_circle(center=(0,0), radius=r)     
        self.figure.clear()
        ax = self.figure.add_subplot(111) 
        ctx = RenderContext(doc)
        ctx.current_layout.set_colors(bg='#FFFFFF')
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc.modelspace())                   
        self.canvas.draw()
if __name__ == '__main__':

        app = QApplication(sys.argv)
        main = Window()
        main.show()   
        sys.exit(app.exec_())
