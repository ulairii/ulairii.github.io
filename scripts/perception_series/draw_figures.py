#!/usr/bin/env python3
"""Rebuild the original, schematic SVGs for chapters 2–24. Python stdlib only."""
from pathlib import Path
from html import escape
import math
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'images/perception-series'
BLUE, GREEN, ORANGE, PURPLE, GRAY = '#2563eb', '#047857', '#c2410c', '#7c3aed', '#475569'
class Diagram:
    def __init__(self, n, title, desc, height=460):
        self.n, self.title, self.desc, self.height = n, title, desc, height
        self.parts=[]
        self.text(24,35,title,25,bold=True)
    def text(self,x,y,s,size=21,color='#172033',bold=False,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'+(' font-weight="bold"' if bold else '')+'>'+escape(str(s))+'</text>')
    def rect(self,x,y,w,h,fill='#eff6ff',stroke='#94a3b8',r=6,dash=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
    def line(self,x1,y1,x2,y2,color=GRAY,arrow=False,dash=False,width=2):
        self.parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="7 5"' if dash else '')+'/>')
    def path(self,path,color=BLUE,fill='none',width=3,dash=False):
        self.parts.append(f'<path d="{path}" fill="{fill}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 5"' if dash else '')+'/>')
    def dot(self,x,y,color=BLUE,r=6):self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
    def box(self,x,y,w,h,lines,color='#eff6ff'):
        self.rect(x,y,w,h,color)
        for i,s in enumerate(lines):self.text(x+w/2,y+29+i*27,s,21,anchor='middle')
    def grid(self,x,y,cols,rows,cell=30,active=(),color=BLUE):
        for j in range(rows):
            for i in range(cols):self.rect(x+i*cell,y+j*cell,cell,cell,'#dbeafe' if (i,j) in active else '#f8fafc','#cbd5e1',0)
        for i,j in active:self.dot(x+(i+.5)*cell,y+(j+.5)*cell,color,4)
    def save(self):
        s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {self.height}" role="img" aria-labelledby="title desc"><title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="{GRAY}"/></marker></defs><rect width="720" height="{self.height}" fill="white"/><g font-family="Arial, sans-serif">'+''.join(self.parts)+'</g></svg>\n'
        (OUT/f'{self.n:02d}.svg').write_text(s)

def draw():
 d=Diagram(2,'Different sensors, different evidence','Camera pixels describe appearance, lidar samples surfaces, and radar measures range and radial motion.')
 for x,title in [(25,'Camera'),(260,'Lidar'),(495,'Radar')]:
  d.text(x,87,title,24,bold=True);d.rect(x,110,200,210,'#f8fafc')
 d.rect(65,175,115,65,'#dbeafe',BLUE);d.dot(85,247,GRAY,13);d.dot(163,247,GRAY,13)
 for x in range(48,209,20):d.line(x,130,x,300,'#cbd5e1',width=1)
 for y in range(130,301,20):d.line(45,y,208,y,'#cbd5e1',width=1)
 for x,y in [(290,175),(320,171),(350,180),(389,185),(411,208),(300,225),(335,235),(380,236),(410,237)]:d.dot(x,y,GREEN)
 d.dot(520,271,GRAY,10);d.dot(653,169,ORANGE,10);d.line(530,262,643,177,GRAY,dash=True);d.line(625,190,590,218,arrow=True,width=3)
 d.text(27,362,'Light and color',21);d.text(260,362,'Surface positions',21);d.text(495,362,'Range + radial',21);d.text(495,389,'velocity',21)
 d.text(25,435,'Schematic measurements; not a sensor specification.',19);d.save()
 d=Diagram(3,'Learning from examples','During training a prediction is compared with a label. The loss updates parameters. At inference the label is absent.',480)
 d.box(30,80,190,65,['Training image']);d.box(265,80,190,65,['Model']);d.box(500,80,190,65,['Prediction'])
 d.line(224,112,257,112,arrow=True);d.line(459,112,492,112,arrow=True)
 d.box(500,220,190,65,['Compare: loss'],'#fff7ed');d.line(595,148,595,212,arrow=True)
 d.box(265,220,190,65,['Target label'],'#f0fdf4');d.line(459,252,492,252,arrow=True)
 d.path('M595 285V305H70V180H360',ORANGE,width=2);d.line(360,180,360,150,ORANGE,arrow=True);d.text(80,205,'Update parameters',20,ORANGE)
 d.line(25,330,695,330,'#cbd5e1');d.text(30,365,'Inference: new image → trained model → prediction',23)
 d.text(30,413,'No target label is available to correct this answer.',21);d.save()
 d=Diagram(4,'One pixel, several possible depths','Two points along one ray have identical horizontal image position under pinhole projection.')
 d.dot(75,320,GRAY,9);d.text(25,362,'Camera',21)
 d.line(75,320,650,90,BLUE,width=3);d.line(75,320,650,320,'#94a3b8',arrow=True)
 d.line(235,105,235,355,GRAY,width=3);d.text(155,86,'Virtual image plane',20)
 d.dot(235,256,ORANGE,8);d.text(247,284,'Same pixel',21,ORANGE)
 d.dot(325,220,BLUE,9);d.text(270,192,'(X, Z) = (1, 10)',20)
 d.dot(575,120,GREEN,9);d.text(490,87,'(2, 20)',20)
 d.text(565,353,'Depth Z →',21);d.text(25,407,'u = f × X / Z + c',25,bold=True);d.text(340,407,'Both points have X/Z = 0.1',21);d.save()
 d=Diagram(5,'Where detection shares computation','R-CNN processes separate crops; Fast R-CNN shares features; Faster R-CNN learns proposals from those features.',495)
 for y,name,steps in [(85,'R-CNN',['Region crops','CNN per crop','Boxes']), (220,'Fast R-CNN',['Image CNN','Region features','Boxes']), (355,'Faster R-CNN',['Image CNN','Learned proposals','Refine boxes'])]:
  d.text(25,y,name,23,bold=True)
  for i,label in enumerate(steps):
   x=25+i*235;d.box(x,y+17,200,63,[label])
   if i<2:d.line(x+204,y+48,x+227,y+48,arrow=True)
 d.text(25,475,'Each row is a simplified computation, not the full architecture.',18);d.save()
 d=Diagram(6,'Small objects need spatial detail','A large object spans several coarse cells; a small object can be represented more clearly on a fine feature grid.')
 d.text(25,88,'Coarse feature grid',23,bold=True);d.text(390,88,'Fine feature grid',23,bold=True)
 d.grid(25,115,6,5,44);d.rect(69,159,132,88,'#bfdbfe',BLUE)
 d.grid(390,115,12,10,22);d.rect(566,203,22,44,'#d1fae5',GREEN)
 d.text(25,369,'Truck: several cells',22);d.text(390,369,'Cyclist: finer evidence',22)
 d.text(25,423,'Heads combine predictions across feature scales.',23);d.save()
 d=Diagram(7,'Three ways to describe the same scene','A bounding box includes background; a semantic mask labels both cars the same; instance masks distinguish them.')
 for x,title in [(20,'Boxes'),(255,'Semantic masks'),(490,'Instance masks')]:
  d.text(x,87,title,22,bold=True);d.rect(x,112,205,220,'#f8fafc');d.rect(x+22,265,160,45,'#e2e8f0','#e2e8f0')
  for i in range(2):
   col=BLUE if x<490 or i==0 else GREEN
   d.path(f'M{x+25+i*75} 240v-55h20l12 -24h22l15 24v55Z',col,'#dbeafe' if col==BLUE else '#d1fae5')
   if x==20:d.rect(x+20+i*75,152,72,95,'none',ORANGE,0)
 d.text(20,374,'Extent',22);d.text(255,374,'Both: vehicle',22);d.text(490,374,'Car A / Car B',22)
 d.text(20,430,'A mask remains in image coordinates unless geometry is added.',20);d.save()
 d=Diagram(8,'Similar image size, different physical size','A small nearby object and a larger distant object span the same angle at a camera.')
 d.dot(50,285,GRAY,9);d.line(50,285,660,75,BLUE);d.line(50,285,660,285,BLUE)
 d.line(270,209,270,285,GREEN,width=9);d.line(560,109,560,285,ORANGE,width=9)
 d.text(170,335,'Small and near',22);d.text(455,335,'Larger and far',22)
 d.text(30,90,'Same angular extent',24,bold=True);d.text(30,388,'Image height alone does not determine distance.',24)
 d.text(30,432,'A size estimate or additional measurement is needed.',21);d.save()
 d=Diagram(9,'Order changes; the pooled result does not','Shared point encoding produces features whose channelwise maximum is independent of their order.')
 d.box(25,95,200,160,['Point features','(2, 1)','(0, 4)','(3, 2)'])
 d.box(260,125,190,90,['Maximum','per channel'],'#fff7ed');d.box(490,125,200,90,['Global feature','(3, 4)'],'#f0fdf4')
 d.line(230,170,251,170,arrow=True);d.line(455,170,482,170,arrow=True)
 d.box(25,295,200,130,['Shuffled features','(3, 2), (2, 1)','(0, 4)'])
 d.line(230,350,481,240,arrow=True);d.text(292,340,'Same result',24,bold=True);d.text(292,388,'Not all geometry survives',20);d.save()
 d=Diagram(10,'A grid organizes sparse measurements','Only some grid cells contain sampled points. Halving cell edges in 3D multiplies the number of cells by eight.')
 active=[(0,2),(1,2),(2,1),(2,2),(3,1),(4,3)]
 d.grid(25,110,5,5,44,active);d.text(25,88,'Active cells',24,bold=True)
 d.grid(370,110,10,10,22,[(2*i,2*j) for i,j in active]);d.text(370,88,'Finer cells',24,bold=True)
 d.text(25,371,'2× along X × 2× along Y × 2× along Z = 8× cells',24)
 d.text(25,423,'These drawings show one horizontal slice.',21);d.save()
 d=Diagram(11,'From pillars to object centers','Points at different heights are encoded into pillars. A top-view detector estimates centers and other box properties.')
 for x in [50,110,170]:d.rect(x,115,45,190,'#eff6ff',BLUE,0)
 for x,y in [(65,140),(70,250),(128,180),(139,280),(190,160),(186,222)]:d.dot(x,y,GREEN)
 d.text(25,89,'Encode height in features',21)
 d.line(230,205,296,205,arrow=True)
 d.grid(315,115,6,5,40,[(2,2),(4,1)]);d.dot(415,215,ORANGE,9);d.dot(495,175,ORANGE,9)
 d.text(310,89,'Predict centers in BEV',22)
 d.box(35,355,650,68,['Center outputs: size, height, heading,','and other required object properties.'])
 d.save()
 d=Diagram(12,'Three camera-to-3D routes','Image features can produce object boxes directly, reconstruct points from depth, or lift features using depth weights.',490)
 d.box(30,75,660,65,['Camera image features'])
 labels=[('Object predictions','Box geometry'),('Depth → points','Point-cloud detector'),('Depth weights','Spatial feature grid')]
 for i,(a,b) in enumerate(labels):
  x=25+i*235;d.line(360,145,x+100,203,arrow=True);d.box(x,215,200,100,[a,b],['#eff6ff','#f0fdf4','#fff7ed'][i])
 d.text(25,370,'All routes must estimate missing geometry.',24,bold=True)
 d.text(25,417,'Inferred points are not direct lidar measurements.',22);d.save()
 d=Diagram(13,'Lift image evidence, then pool it into BEV','A feature is weighted at candidate depths, transformed using calibration, and pooled into a shared horizontal grid.',510)
 d.box(25,80,240,90,['Image feature = 4','Depth weights: .1, .7, .2'])
 d.dot(45,280,GRAY,8);d.line(45,280,330,200,GRAY)
 for x,y,t in [(110,262,'.4'),(200,237,'2.8'),(300,209,'.8')]:d.dot(x,y,BLUE,10);d.text(x-13,y-23,t,22)
 d.text(25,328,'Lift: weighted candidates',22)
 d.line(335,235,412,235,arrow=True);d.grid(435,155,6,5,40,[(1,1),(2,2),(3,3)])
 d.text(435,105,'Splat into BEV',23,bold=True)
 d.text(25,405,'Camera calibration places every candidate in a shared frame.',20)
 d.text(25,454,'Other cameras can contribute to the same cells.',22);d.save()
 d=Diagram(14,'A spatial query gathers image evidence','Height reference points for one BEV cell project into different camera features, which update the query.',520)
 d.grid(25,250,5,4,42,[(2,1)]);d.text(25,460,'One BEV query',23,bold=True)
 d.line(130,314,130,150,BLUE,width=3)
 for y in [160,205,250]:d.dot(130,y,ORANGE,7)
 d.text(25,116,'Reference heights',22)
 for y,title in [(75,'Camera A'),(280,'Camera B')]:
  d.box(400,y,275,145,[title]);d.dot(480,y+85,GREEN,8);d.dot(570,y+100,BLUE,8)
 d.line(140,160,477,156,GRAY,arrow=True);d.line(140,205,565,175,GRAY,arrow=True)
 d.line(140,250,477,364,GRAY,arrow=True);d.text(290,485,'Sample features → update query',23);d.save()
 d=Diagram(15,'Where sensor information meets','Camera and lidar encoders make aligned BEV features for joint prediction; late fusion instead joins final detections.',535)
 d.box(25,80,290,65,['Camera → BEV features']);d.box(405,80,290,65,['Lidar → BEV features'],'#f0fdf4')
 d.line(170,151,330,211,arrow=True);d.line(550,151,390,211,arrow=True)
 d.box(200,225,320,85,['Align and combine','Then predict objects'])
 d.line(25,348,695,348,'#cbd5e1')
 d.text(25,386,'Late fusion:',23,bold=True)
 d.box(25,408,210,75,['Camera detections']);d.box(485,408,210,75,['Lidar detections'],'#f0fdf4')
 d.text(270,452,'Associate',23);d.line(240,445,264,445,arrow=True);d.line(481,445,405,445,arrow=True);d.save()
 d=Diagram(16,'A track can bridge an observation gap','Measured cyclist positions are solid; a dashed prediction during occlusion is less certain and must be updated.',470)
 for x,t in [(30,'Time 1'),(270,'Time 2'),(510,'Time 3')]:
  d.text(x,94,t,24,bold=True);d.rect(x,120,180,200,'#f8fafc');d.line(x+15,280,x+165,280,'#94a3b8')
 d.rect(75,215,40,60,'#d1fae5',GREEN);d.rect(330,200,40,60,'none',PURPLE,dash=True);d.rect(590,185,40,60,'#d1fae5',GREEN)
 d.text(38,357,'Measured',22);d.text(275,357,'Predicted',22);d.text(515,357,'Measured',22)
 d.line(215,220,261,220,arrow=True);d.line(455,220,501,220,arrow=True)
 d.text(25,418,'An old track is a hypothesis, not a new observation.',22);d.save()
 d=Diagram(17,'Road pixels, curves, and connections','Three panels show fragmented markings, a vector curve, and a branching lane graph.')
 for x,title in [(25,'Pixels'),(265,'Polyline'),(505,'Topology')]:d.text(x,90,title,24,bold=True)
 for y in [140,172,232,264]:d.rect(95,y,22,23,'#bfdbfe',BLUE,0)
 pts=[(310,310),(325,255),(347,213),(370,166),(410,140)]
 d.path('M'+'L'.join(f'{x} {y}' for x,y in pts),BLUE)
 for x,y in pts:d.dot(x,y,ORANGE)
 d.line(560,310,560,230,BLUE,arrow=True);d.line(560,230,560,145,BLUE,arrow=True);d.path('M560 230Q640 230 655 140',GREEN)
 for x,y in [(560,310),(560,230),(560,145),(655,140)]:d.dot(x,y,ORANGE)
 d.text(25,376,'Category',22);d.text(265,376,'Shape',22);d.text(505,376,'Relationships',22)
 d.text(25,430,'Good geometry does not guarantee the correct lane connections.',20);d.save()
 d=Diagram(18,'Dense space or selected object hypotheses?','A dense BEV grid is compared with sparse keypoints around object boxes.')
 d.grid(25,115,7,6,40);d.text(25,88,'Dense BEV',24,bold=True)
 d.rect(72,178,60,90,'#dbeafe',BLUE,0);d.rect(206,143,45,70,'#d1fae5',GREEN,0)
 d.text(410,88,'Sparse object queries',22,bold=True)
 for x,y,w,h in [(430,180,75,105),(575,135,55,90)]:
  d.rect(x,y,w,h,'none',BLUE,0)
  for xx,yy in [(x,y),(x+w,y),(x,y+h),(x+w,y+h),(x+w/2,y+h/2)]:d.dot(xx,yy,ORANGE,7)
 d.text(25,405,'Every cell has a location.',21);d.text(390,405,'Samples follow hypotheses.',21)
 d.save()
 d=Diagram(19,'No return behind a surface does not mean empty','A ray crosses observed free cells, reaches an occupied surface, and leaves unknown space beyond.',430)
 d.dot(35,200,GRAY,10);d.text(25,130,'Sensor',22)
 for i in range(9):
  x=95+i*65;col='#d1fae5' if i<4 else ('#ffedd5' if i==4 else '#ede9fe')
  d.rect(x,165,65,70,col,'#94a3b8',0)
  if i>4:d.text(x+32,211,'?',26,PURPLE,anchor='middle')
 d.line(45,200,380,200,GRAY,arrow=True)
 d.text(120,280,'Observed free',22,GREEN);d.text(330,315,'Surface',22,ORANGE);d.text(485,280,'Unknown',22,PURPLE)
 d.text(25,379,'A benchmark may encode unknown with a visibility mask.',21);d.save()
 d=Diagram(20,'One present, more than one possible future','The cyclist can continue straight or turn. These are alternative forecasts rather than simultaneous facts.',480)
 d.box(25,180,185,90,['Current cyclist','Position + motion'])
 d.line(215,210,338,132,arrow=True);d.line(215,245,338,337,arrow=True)
 for y,title in [(65,'Future A: straight'),(270,'Future B: turn')]:
  d.rect(350,y,340,155,'#f8fafc');d.text(365,y+31,title,22,bold=True)
  d.dot(390,y+113,GREEN,9)
 d.line(403,178,640,178,GREEN,arrow=True,width=3)
 d.path('M403 383H510Q600 383 600 326',PURPLE,width=3)
 d.text(25,460,'Forecast alternatives must remain distinct.',23);d.save()
 d=Diagram(21,'Coordinate tasks around the driving objective','Structured perception and prediction share information with planning while keeping task supervision.',515)
 d.box(30,75,660,65,['Sensor features'])
 d.box(30,210,195,95,['Objects / tracks','Road map']);d.box(265,210,195,95,['Future motion','Occupancy'],'#f0fdf4');d.box(500,210,195,95,['Our trajectory','Planning'],'#fff7ed')
 for x in [125,360,595]:d.line(360,145,x,202,arrow=True)
 d.line(230,255,257,255,arrow=True);d.line(465,255,492,255,arrow=True)
 for x,t in [(125,'Perception loss'),(360,'Prediction loss'),(595,'Planning loss')]:d.text(x,364,t,20,anchor='middle');d.line(x,310,x,336,ORANGE,arrow=True)
 d.text(30,430,'Shared training can retain named intermediate outputs.',22)
 d.text(30,478,'Execution still needs control and new observations.',22);d.save()
 d=Diagram(22,'Broader data, then task-specific grounding','Pretraining learns features from broad data, while driving supervision teaches metric outputs and task behavior.',510)
 d.box(30,75,300,85,['Images / image-text pairs','Broad source data'])
 d.box(400,75,290,85,['Pretrained features']);d.line(335,115,391,115,arrow=True)
 d.box(30,260,300,90,['Driving observations','Geometry + labels'],'#f0fdf4')
 d.box(400,260,290,90,['Adapted driving model','Metric outputs'],'#fff7ed')
 d.line(545,165,545,250,arrow=True);d.line(335,305,391,305,arrow=True)
 d.text(30,418,'Knowing an object name does not establish its distance.',22)
 d.text(30,466,'Training data and inference inputs must be reported separately.',20);d.save()
 d=Diagram(23,'A world model predicts action-dependent futures','One current state branches into rollouts for slowing down or continuing; predicted futures require validation.',510)
 d.box(25,195,175,90,['Current state','Observations'])
 for y,a,b,col in [(75,'Slow down','Predicted future A','#f0fdf4'),(300,'Continue','Predicted future B','#fff7ed')]:
  d.box(270,y,170,75,[a],col);d.box(485,y,210,110,[b,'Not an observation'],col)
  d.line(205,240,260,y+37,arrow=True);d.line(445,y+37,477,y+37,arrow=True)
 d.text(25,463,'Check geometry, action response, and error over time.',22);d.save()
 d=Diagram(24,'Match the evidence to the claim','Evaluation examines data independence, component predictions, timing and degradation, then closed-loop behavior.',530)
 rows=[('1. Data and labels','Independent splits; valid targets'),('2. Component outputs','Geometry, semantics, identity, motion'),('3. Timing and degradation','Latency, missing inputs, recovery'),('4. Closed-loop behavior','Actions change later observations')]
 for i,(a,b) in enumerate(rows):
  y=70+i*110;d.box(30,y,660,83,[a,b],['#eff6ff','#eff6ff','#f0fdf4','#fff7ed'][i])
  if i<3:d.line(360,y+87,360,y+105,arrow=True)
 d.text(30,515,'A strong result at one level does not prove every other level.',20);d.save()

if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 draw()
 print('Wrote 23 original SVG diagrams.')
