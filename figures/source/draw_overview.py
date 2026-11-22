"""Generate the vector overview and a preview using ReportLab and SVG primitives."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from math import atan2, cos, sin, pi

OUT = Path(__file__).resolve().parents[1]
W, H = 1000, 650
BLUE, GREEN, ORANGE, BORDER = '#426E9A', '#2B7C6F', '#B78230', '#A9BDCD'
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
pdf = canvas.Canvas(str(OUT / 'ApproxPilot_SE_Overview.pdf'), pagesize=(W, H))
pdf.setTitle('ApproxPilot-SE framework overview')

def text(x,y,value,size=14,bold=False,color='#243746',anchor='middle'):
    font='Helvetica-Bold' if bold else 'Helvetica'
    pdf.setFillColor(HexColor(color)); pdf.setFont(font,size)
    if anchor=='middle': pdf.drawCentredString(x,y,value)
    elif anchor=='end': pdf.drawRightString(x,y,value)
    else: pdf.drawString(x,y,value)
    svg.append(f'<text x="{x}" y="{H-y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')

def rect(x,y,w,h,fill='#FFFFFF',stroke=BORDER,radius=5,lw=1):
    pdf.setFillColor(HexColor(fill)); pdf.setStrokeColor(HexColor(stroke)); pdf.setLineWidth(lw)
    pdf.roundRect(x,y,w,h,radius,stroke=1,fill=1)
    svg.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>')
pdf.setTitle('ApproxPilot-SE: self-evolving design space exploration')
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
INK, BLUE, GREEN, ORANGE, BORDER = '#20364B', '#346EA8', '#168071', '#B77825', '#B6C9DA'

def text(x, y, s, size=14, bold=False, color=INK, anchor='middle'):
    pdf.setFillColor(HexColor(color))
    pdf.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    {'middle': pdf.drawCentredString, 'start': pdf.drawString, 'end': pdf.drawRightString}[anchor](x, y, s)
    svg.append(f'<text x="{x}" y="{H-y}" fill="{color}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(s)}</text>')

def rect(x, y, w, h, fill='#FFFFFF', stroke=BORDER, radius=7, width=1):
    pdf.setFillColor(HexColor(fill)); pdf.setStrokeColor(HexColor(stroke)); pdf.setLineWidth(width)
    pdf.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    svg.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

def line(points, color=INK, width=1.6, arrow=True):
    pdf.setStrokeColor(HexColor(color)); pdf.setLineWidth(width)
    path=pdf.beginPath(); path.moveTo(*points[0])
    for p in points[1:]: path.lineTo(*p)
    pdf.drawPath(path)
    svg.append(f'<polyline points="{" ".join(f"{x},{H-y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')
    if arrow:
        x,y=points[-1]; px,py=points[-2]; a=atan2(y-py,x-px)
        pts=[(x,y),(x-7*cos(a-pi/7),y-7*sin(a-pi/7)),(x-7*cos(a+pi/7),y-7*sin(a+pi/7))]
        poly(pts,color,color)

def poly(points, fill='#FFFFFF', stroke=BORDER):
    pdf.setFillColor(HexColor(fill)); pdf.setStrokeColor(HexColor(stroke)); pdf.setLineWidth(1)
    path=pdf.beginPath(); path.moveTo(*points[0])
    for p in points[1:]:path.lineTo(*p)
    path.close();pdf.drawPath(path,stroke=1,fill=1)
    svg.append(f'<polygon points="{" ".join(f"{x},{H-y}" for x,y in points)}" fill="{fill}" stroke="{stroke}"/>')

def diamond(cx,cy,w,h,fill='#FFFFFF',stroke=BORDER):
    poly([(cx,cy+h/2),(cx+w/2,cy),(cx,cy-h/2),(cx-w/2,cy)],fill,stroke)

def lines(x,y,items,size=14,gap=19,**kw):
    for i,s in enumerate(items):text(x,y-i*gap,s,size,**kw)

# Initialization is distinct from the iterative search.
rect(10,548,980,92,'#F3F7FC')
text(26,618,'1  INITIALIZATION',15,True,BLUE,'start')
rect(28,558,295,48)
lines(175.5,588,['Target RTL + arithmetic-unit library','Initial sampling + synthesis + execution'],13,gap=17)
line([(323,582),(361,582)])
rect(362,558,242,48)
lines(483,588,['Measured PPA + application quality','Initial labeled configurations'],13,gap=17)
line([(604,582),(642,582)])
rect(643,558,331,48)
lines(808.5,588,['Train initial PPA and accuracy GNNs','Initialize measured calibration references'],13,gap=17)

# Main loop: a small candidate-search loop inside a measured-feedback loop.
rect(10,136,980,398,'#F8FBFE',stroke='#A4BFD6')
text(28,509,'SELF-EVOLVING DSE',22,True,BLUE,'start')
text(975,511,'Search selects data. Measured data refine search.',13,False,GREEN,'end')

rect(28,382,185,88,'#E9F2FC',BLUE)
text(120.5,448,'2  Candidate generation',15,True)
lines(120.5,421,['NSGA-III','Arithmetic-unit assignments'],13,gap=18)
line([(213,426),(246,426)])

rect(247,374,255,105,'#FFFFFF',BLUE)
text(374.5,456,'Surrogate-based evaluation',15,True)
lines(374.5,432,['PPA GNN + accuracy GNN','Similar-configuration retrieval','Local latency calibration'],13,gap=18)
line([(808,558),(808,541),(374.5,541),(374.5,479)],BLUE)
line([(502,426),(534,426)])

rect(535,382,166,88,'#E9F2FC',BLUE)
text(618,448,'Pareto ranking',15,True)
lines(618,422,['Candidate selection','Diverse candidate designs'],12.5,gap=18)
line([(701,426),(720,426)])
diamond(769,426,98,80,'#FFFFFF',BLUE)
lines(769,438,['Enough','candidates?'],13,gap=17,bold=True)
line([(769,386),(769,343),(120.5,343),(120.5,382)],BLUE)
rect(420,331,210,24,'#F8FBFE','#F8FBFE',0,0)
text(525,339,'No: continue candidate search',12.5,False,BLUE)
line([(818,426),(893,426),(893,365)],ORANGE)
text(854,436,'Yes',13,True,ORANGE)

rect(811,264,164,101,'#FFF3DE',ORANGE)
text(893,343,'3  Real evaluation',15,True)
lines(893,318,['Logic synthesis','Application execution','Measured PPA + quality'],13,gap=18)
line([(893,264),(893,237),(712,237)],GREEN,2)
text(811,245,'New measured configurations',12.5,False,GREEN)

rect(260,184,452,111,'#E7F4EF',GREEN)
text(486,271,'Surrogate and reference updates',16,True,GREEN)
rect(275,200,201,51,'#FFFFFF','#A7CDBD')
lines(375.5,231,['Expand labeled dataset','Further train both GNNs'],13,gap=18)
rect(493,200,203,51,'#FFFFFF','#A7CDBD')
lines(594.5,231,['Add calibration references','Refresh latency residuals'],13,gap=18)
line([(260,237),(204,237)],GREEN,2)

diamond(120.5,237,167,90,'#FFFFFF',GREEN)
lines(120.5,256,['Feedback','budget exhausted?'],12,gap=18,bold=True)
line([(120.5,282),(120.5,343)],GREEN,2)
lines(133,319,['No: resume search','with updated models + references'],12,gap=16,color=GREEN,anchor='start')
line([(120.5,192),(120.5,105),(155,105),(155,87)],GREEN,2)
text(131,166,'Yes',13,True,GREEN,'start')

# Final verification uses its reserved allocation after feedback ends.
rect(28,20,270,67,'#F3F7FC')
text(163,65,'4  Final search + verification',15,True)
lines(163,45,['Fixed models and references','Reserved final-evaluation budget'],12.5,gap=16)
line([(298,53),(345,53)])
rect(346,20,277,67,'#F3F7FC')
text(484.5,65,'Apply user constraints',15,True)
lines(484.5,45,['Use measured PPA and application quality','Identify feasible nondominated designs'],12.5,gap=16)
line([(623,53),(670,53)])
rect(671,20,303,67,'#E7F4EF',GREEN)
text(822.5,65,'Optimized accelerator configurations',15,True,GREEN)
lines(822.5,45,['Preferred feasible implementation','Pareto alternatives for different objectives'],12.5,gap=16)

pdf.showPage();pdf.save()
svg.append('</svg>')
(OUT/'ApproxPilot_SE_Overview.svg').write_text('\n'.join(svg),encoding='utf-8')
print(OUT/'ApproxPilot_SE_Overview.pdf')
