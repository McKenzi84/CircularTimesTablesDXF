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
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
       
        self.button.clicked.connect(self.embedded_plot)
 
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.toolbar)
        self.layout1.addWidget(self.button)
        self.layout1.addWidget(self.canvas)
        
       
                
        self.setLayout(self.layout1)
   
    # action called by thte push button

    def embedded_plot(self):
        lines = 40
        m = 50
        n = 2
        r = 10
        b = 360/m
        d = (-b)
        points = []

    # Create list with points coordinates
        for x in range(m):
            d += b
            cor_x = r * math.cos(math.radians(d))
            cor_y = r * math.sin(math.radians(d))
    
            points.append((cor_x, cor_y))

        doc = ezdxf.new("R2000")
        msp = doc.modelspace()
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

# Add points to plot 
 
        for x in range(m):
            d += b
            cor_x = r * math.cos(math.radians(d))
            cor_y = r * math.sin(math.radians(d))

            if cor_x > 0 and cor_y > 0:
                msp.add_text(x, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((cor_x, cor_y), align='LEFT')
            elif cor_x < 0  and cor_y > 0:
                msp.add_text(x, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((cor_x, cor_y), align='RIGHT')
            elif cor_x < 0  and cor_y < 0:
                msp.add_text(x, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((cor_x, cor_y), align='TOP_RIGHT')
            elif cor_x > 0  and cor_y < 0:
                msp.add_text(x, dxfattribs={ 'style': 'LiberationSerif','height': r*0.03}).set_pos((cor_x, cor_y), align='TOP_LEFT')
     
        msp.add_circle(center=(0,0), radius=r)

        self.figure.clear()

        ax = self.figure.add_subplot(111) 
        ctx = RenderContext(doc)
        ctx.current_layout.set_colors(bg='#FFFFFF')
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc.modelspace())     
        
        #ax.plot([1,2,3,4,5],[10,20,30,40,50])
               
        self.canvas.draw()
        #plt.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = Window()
    main.show()   
    sys.exit(app.exec_())