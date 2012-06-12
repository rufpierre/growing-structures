# coding=utf-8
from Tkinter import *
import math
import random
import time

root=Tk()

unit = 3
nb_hcases = 60
nb_vcases = nb_hcases
total_width = nb_hcases*2*(2*unit)+2*(2*unit)
total_height = nb_vcases*2*(2*unit)+2*(2*unit)

root.geometry(str(total_width)+"x"+str(total_height))
fond=Canvas(root, width=total_width, height=total_height, background='darkgrey')
fond.pack()

colors = ['red','black','blue','orange','yellow','green']
facets = ['up','right','downright','down','left','upleft']

class Dot:
	x=None
	y=None
	def __init__(self, x, y):
		self.x=x
		self.y=y
	def plus(self, dot):
		return Dot(self.x+dot.x, self.y+dot.y)
	def pos(self):
		return [self.x, self.y]

O=Dot(2*unit, 3*unit) #10, 15
U=Dot(2*unit, 0*unit) #10, 0
R=Dot(4*unit, 2*unit) #20, 10
DR=Dot(4*unit, 4*unit) #20, 20
D=Dot(2*unit, 6*unit) #10, 30
L=Dot(0*unit, 4*unit) #0, 20
UL=Dot(0*unit, 2*unit) #0, 10

def relative_vertex(x, y):
	t=Dot(4*unit*x+2*unit*y,4*unit*y)
	o=O.plus(t)
	u=U.plus(t)
	r=R.plus(t)
	dr=DR.plus(t)
	d=D.plus(t)
	l=L.plus(t)
	ul=UL.plus(t)
	return [o, u, r, dr, d, l, ul]

#fond.create_rectangle(10,10,20,20,fill='blue', outline='white', width=1)
def draw_hex(x, y, color):
	[o, u, r, dr, d, l, ul] = relative_vertex(x, y)
	points=u.pos()+r.pos()+dr.pos()+d.pos()+l.pos()+ul.pos()
	###print("draw hex:"+str(points))
	fond.create_polygon(points, outline='black', fill=color, width=1)

def draw_hex2(x, y, color):
	[o, u, r, dr, d, l, ul] = relative_vertex(x, y)
	points=u.pos()+r.pos()+dr.pos()+d.pos()+l.pos()+ul.pos()
	###print("draw hex:"+str(points))
	fond.create_polygon(points, outline='black', fill="", width=2)

		
def draw_facet(x, y, color, facet):
	[o, u, r, dr, d, l, ul] = relative_vertex(x, y)
	points=u.pos()+r.pos()+o.pos()
	#print(points)
	if True:
		if facet=='up':
			points=u.pos()+r.pos()+o.pos()
		elif facet=='right':
			points=r.pos()+dr.pos()+o.pos()
		elif facet=='downright':
			points=dr.pos()+d.pos()+o.pos()
		elif facet=='down':
			points=d.pos()+l.pos()+o.pos()
		elif facet=='left':
			points=l.pos()+ul.pos()+o.pos()
		elif facet=='upleft':
			points=ul.pos()+u.pos()+o.pos()
#	if facet=='right':
#		points=[10+tx,0+ty,20+tx,10+ty,10+tx,15+ty]
	fond.create_polygon(points, outline='black', fill=color, width=1)
	fond.create_line(points[0:4],width=2)
	

#draw_hex(0,0)
#draw_hex(0,1)
#draw_hex(1,0)
#draw_hex(1,1)

class Case:
	grid=None
	x=None
	y=None
	cell = None
	u=None
	r=None
	dr=None
	d=None
	l=None
	lu=None
	def __init__(self, grid, x, y):
		self.grid=grid
		self.x=x
		self.y=y
	def draw(self):
		draw_hex(self.x, self.y, 'white')
	def is_free(self):
		return self.cell==None
	def detect_neighbourhood(self):
		u=self.grid.get_case_at(self.x-1,self.y-1)
		print("for case:"+self.to_str()+", u is"+str(u))
		r=self.grid.get_case_at(self.x,self.y-1)
		
		
#	def remove_cell(self):
#		self.cell=None
#	def accept_cell(self, cell):
#		self.cell=cell
	def to_str(self):
		return "x="+str(self.x)+", y="+str(self.y)

class Grid:
	cases = []
	clusters = []
	def __init__(self, nb_horiz_cases, nb_vert_cases):
		# on créé les cases
		for y in range(nb_vert_cases):
			for x in range(nb_horiz_cases):
				case = Case(self, x-math.ceil(y/2),y)
				self.cases.append(case)
		# chaque case détectecte et mémorise ses voisines
		if False:
			for case in self.cases:
				case.detect_neighbourhood()
		self.draw()
	def draw(self):
		for case in self.cases:
			case.draw()
			#time.sleep(0.1)
			#root.update()
	def get_case_at(self, x, y):
		for case in self.cases:
			if case.x==x and case.y==y:
				return case
		return None

class Cell:
	case = None
	facets_colors = None
	cluster = None
	def __init__(self, facets_colors):
		def letter_to_color(x):
			letters = "a b c d e f".split()
			for i in range(len(letters)):
				if x==letters[i]:
					return colors[i]
		# ==> remplacer a, b, etc... par colors[0], colors[1], etc...
		self.facets_colors=map(letter_to_color, facets_colors.split())
	def draw(self):
		###print("draw cell:"+self.to_str())
		for facet in facets:
			draw_facet(self.case.x, self.case.y, self.facets_colors[facets.index(facet)], facet)
		# tentative de création d'un polygone à fond transparent et bord épais.
		# draw_hex(self.case.x, self.case.y, 'white')
	def move_to(self, new_case):
		old_case = self.case
		# si la nouvelle case est vide
		if new_case.is_free():
			# si on est déjà sur une case
			if not old_case==None:
				# on vide la l'ancienne case qu'elle occupait
				old_case.cell = None
			# on définit la nouvelle case comme étant la case d'occupation de la cellule
			self.case = new_case
			# dans la nouvelle case, on specifie cette cellule
			new_case.cell=self
		# si la cell n'a aucun cluster defini, on créé lui créé un cluster
		if self.cluster == None:
			self.cluster = Cluster()
			self.cluster.cells.append(self)
		# si la cell a une cell voisine qui a un cluster, alors on merge les cluster
#			en cours: il faut une liste des voisins en passant par la case.
#			si voisin, on merge les cluster (faire l'algo de merge')
	def touches(cell):
		#if cell.case.
		return choice([True, False])
	def to_str(self):
		return self.case.to_str()+""

# les clusters sont créés au moment où l'on place une cell sur une case
# si la cell n'a pas de cluster, on en créé un et lui assigne
class Cluster:
	cells=[]
	def merge(self, cluster):
		print "merge cluster"
		


#debut du main
grid = Grid(nb_vcases, nb_hcases)

if False:
	for y in range(nb_vcases):
		for x in range(nb_hcases):
			case = Case(x-math.ceil(y/2),y)
			grid.cases.append(case)
	grid.draw()

tests = False

# tests
if tests:
	print("tests")
	if False:
		co = Cell("a a a a a a")
		co.move_to(grid.get_case_at(4,4))
		cu = Cell("b a a a a a")
		print("co case is:"+str(co.case.to_str()))
		cu.move_to(co.case.u)# ==> tester si la detection initiale de voisins fonctionne
	
	# postionnement de base
	# décrit un cercle autour de co, commencant par dr et tournant dans le sens des aiguilles d'une montre
	if True:
		[ox,oy]=[3,3]
		co = Cell("a a a a a a")
		co.move_to(grid.get_case_at(ox+0,oy+0))
		co.draw()
		root.update()
		time.sleep(0.2)
		
		cdr = Cell("b a a a a a")
		cdr.move_to(grid.get_case_at(ox+0,oy+1))
		cdr.draw()
		root.update()
		time.sleep(0.2)

		cr = Cell("c a a a a a")
		cr.move_to(grid.get_case_at(ox+1,oy+0))
		cr.draw()
		root.update()
		time.sleep(0.2)

		cu = Cell("d a a a a a")
		cu.move_to(grid.get_case_at(ox+1,oy-1))
		cu.draw()
		root.update()
		time.sleep(0.2)

		cul = Cell("e a a a a a")
		cul.move_to(grid.get_case_at(ox+0,oy-1))
		cul.draw()
		root.update()
		time.sleep(0.2)
		
		cl = Cell("f a a a a a")
		cl.move_to(grid.get_case_at(ox-1,oy+0))
		cl.draw()
		root.update()
		time.sleep(0.2)
		
		cd = Cell("a b a a a a")
		cd.move_to(grid.get_case_at(ox-1,oy+1))
		cd.draw()
		root.update()
		time.sleep(0.2)


		root.mainloop()
	
	if False:
		pattern = "a b b a b b"
		cell1 = Cell(pattern)
		cell1.move_to(grid.get_case_at(3,3))
		cell1.draw()
		cell2 = Cell(pattern)
		cell2.move_to(grid.get_case_at(3,4))
		cell2.draw()
		root.update()
		root.mainloop()
	
	#==> recup 2 cases proches l'une de l'autre

# main use
if not tests:
	print("main use")
	for i in range(400):
		cell = Cell("a b a b c c")
		# on cherche une case libre dans la grills
		isFree=False
		while not isFree:
			case = random.choice(grid.cases)
			isFree = case.is_free()
		cell.move_to(case)	
		cell.draw()
	root.update()
	root.mainloop()
