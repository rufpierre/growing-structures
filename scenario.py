# coding=utf-8
import world
import random

#debut du main
grid = world.Grid(world.nb_vcases, world.nb_hcases)

if False:
	for y in range(world.nb_vcases):
		for x in range(world.nb_hcases):
			case = Case(x-math.ceil(y/2),y)
			grid.cases.append(case)
	grid.draw()

"""tests = False

# tests
if tests:
	print("tests")
	if False:
		co = world.Cell("a a a a a a")
		co.move_to(grid.get_case_at(4,4))
		cu = world.Cell("b a a a a a")
		print("co case is:"+str(co.case.to_str()))
		cu.move_to(co.case.u)# ==> tester si la detection initiale de voisins fonctionne
	
	# postionnement de base
	# décrit un cercle autour de co, commencant par dr et tournant dans le sens des aiguilles d'une montre
	if True:
		[ox,oy]=[3,3]
		co = world.Cell("a a a a a a")
		co.move_to(grid.get_case_at(ox+0,oy+0))
		co.draw()
		root.update()
		time.sleep(0.2)
		
		cdr = world.Cell("b a a a a a")
		cdr.move_to(grid.get_case_at(ox+0,oy+1))
		cdr.draw()
		root.update()
		time.sleep(0.2)

		cr = world.Cell("c a a a a a")
		cr.move_to(grid.get_case_at(ox+1,oy+0))
		cr.draw()
		root.update()
		time.sleep(0.2)

		cu = world.Cell("d a a a a a")
		cu.move_to(grid.get_case_at(ox+1,oy-1))
		cu.draw()
		root.update()
		time.sleep(0.2)

		cul = world.Cell("e a a a a a")
		cul.move_to(grid.get_case_at(ox+0,oy-1))
		cul.draw()
		root.update()
		time.sleep(0.2)
		
		cl = world.Cell("f a a a a a")
		cl.move_to(grid.get_case_at(ox-1,oy+0))
		cl.draw()
		root.update()
		time.sleep(0.2)
		
		cd = world.Cell("a b a a a a")
		cd.move_to(grid.get_case_at(ox-1,oy+1))
		cd.draw()
		root.update()
		time.sleep(0.2)


		root.mainloop()
	
	if False:
		pattern = "a b b a b b"
		cell1 = world.Cell(pattern)
		cell1.move_to(grid.get_case_at(3,3))
		cell1.draw()
		cell2 = world.Cell(pattern)
		cell2.move_to(grid.get_case_at(3,4))
		cell2.draw()
		root.update()
		root.mainloop()
	
	#==> recup 2 cases proches l'une de l'autre"""

# main use
#if not tests:
print("main use")
for i in range(400):
	cell = world.Cell("a b a b c c")
	# on cherche une case libre dans la grills
	isFree=False
	while not isFree:
		case = random.choice(grid.cases)
		isFree = case.is_free()
	cell.move_to(case)	
	cell.draw()
world.root.update()
world.root.mainloop()
