# 1. RULES 
# Plant on soil
# With messure() --> to check size is 0...9
# If harvest a fully-grown can_harvest() 
# and all neighboring cacti are in sorted order
# it will also harvest all neighboring cacti recursively.
# A cactus is considered to be in sorted order when: 
# measure(North) and measure(East) = fully grown and >= measure()
# and measure(West) and measure(South) = fully grown and <= measure()
# can swap a cactus with its neighbor in any direction using the swap()
	
# 2. STRATEGY
# Plannt field 
# Check field ubtil all cactus fully grown
# Use bubble sort to sort the field ONCE


	
	
def harv():
	if can_harvest():
		harvest()
	
def go_to(x, y):
	while get_pos_x() != x:
		dx = (x - get_pos_x()) % get_world_size()
		if dx <= get_world_size() / 2:
				move(East)
		else:
				move(West)
	while get_pos_y() != y:
		dy = (y - get_pos_y()) % get_world_size()
		if dy <= get_world_size() / 2:
			move(North)
		else:
			move(South)

def check_soil():
	if get_ground_type() != Grounds.Soil:
		till()
		

def check_water():
	if get_water() < 0.75:
			use_item(Items.Water)
			
		
def plant_entire_field():
	size = get_world_size()
	
	for j in range(size):
		for i in range(size):
			go_to(i, j)
			check_soil()
			plant(Entities.Cactus)
			check_water()
			
def wait_to_grow():
	size = get_world_size()
	ready = False
	while not ready:
		ready = True
		for y in range(size):
			for x in range(size):
				go_to(x,y)
				if get_entity_type() != Entities.Cactus or not can_harvest():
					ready = False
	
def sort_field():
	size = get_world_size()
	swapped = False
	for y in range(size):
		for x in range(size):
			go_to(x,y)
			here = measure()
			if x < size - 1:
				if measure(East) != None and here > measure(East):
					swap(East) 
					swapped = True
					here = measure()
			if y < size - 1:
				if measure(North) != None and here > measure(North):
					swap(North) 
					swapped = True
					here = measure()
	return swapped

clear()
while True:
	plant_entire_field()
	wait_to_grow()
	while sort_field():
		pass
	go_to(0,0)
	harv()