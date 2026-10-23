#=================================================	
def harv():
	if can_harvest():
		harvest()
#-------------------------------------------------	
def check_soil():
	if get_ground_type() != Grounds.Soil:
		till()
#-------------------------------------------------	
def check_water():
	if get_water() < 0.75:
			use_item(Items.Water)
#-------------------------------------------------
def decision(x,y, field):
	if field == "Carrots":
		carrot_field(x, y, 9, 9)
	elif field == "Grass":
		grass_field(x, y, 9, 9)
	elif field == "Trees1":
		tree_field(x, y, 18, 4)
	else:
		tree_field(x, y, 4, 22)
#=================================================	