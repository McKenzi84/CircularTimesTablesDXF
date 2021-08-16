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

doc.saveas('ctt.dxf')  # save to .dxf file

fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
#ax = fig.subplots(111)
ctx = RenderContext(doc)
out = MatplotlibBackend(ax)
Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
#fig.savefig(DIR /'your.png', dpi=300)    # uncomment this line to save plot to .png   
plt.show()
