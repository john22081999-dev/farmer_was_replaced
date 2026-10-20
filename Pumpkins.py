# 1. RULES 
# Plant on soil
# 20% chance to plant bad pumpkin 
# Pumpkins merge -> 2x2, 3x3, 4x4, 5x5, 6x6
# Planting anything on a dead pumpkin clears it 
# Optionally fertilize the **new** plant after replanting to cut 2s grow time.
	
# 2. STRATEGY
# Do not re-scan the whole farm forever. After the first pass, keep a list of coordinates that are empty, dead, or not yet harvestable.
# 1. Plant: Till + plant every tile once. 2. Track: Append `[x, y]` when `not can_harvest()` or entity is Dead_Pumpkin.
# 3. Patch: Replant over dead/empty; optionally `use_item(Items.Fertilizer)` on the new plant.
# 4. Harvest: When the bad list is empty, `harvest()` once anywhere on the giant pumpkin.

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
			
def plant_entire_field():
	size = get_world_size()
	
	for j in range(size):
		for i in range(size):
			go_to(i, j)
			check_soil()
			plant(Entities.Pumpkin)
			check_water()

def check_water():
	if get_water() < 0.75:
			use_item(Items.Water)
			
def dead_pumps():
	size = get_world_size()
	dead = []
	for j in range(size):
		for i in range(size):
			go_to(i, j)
			pump = get_entity_type()
			if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
				dead.append([i, j])
	return dead		

def replant(dead):
	while len(dead) > 0:
		still_dead = []
		for pos in dead:
			go_to(pos[0], pos[1])
			check_soil()
			plant(Entities.Pumpkin)
			check_water()
			pump = get_entity_type()
			if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
				still_dead.append([pos[0], pos[1]]) 
		dead = still_dead
		
clear()	
while True:
	plant_entire_field()
	dead = dead_pumps()
	replant(dead)
	go_to(0,0)
	harv()
			
	