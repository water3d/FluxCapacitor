

def balance():



	pass




def single_timestep_water_requirements(year, field, crop, climate):
	"""
		We need a function that returns the water requirements of a field (acreage, location, etc), if it grows a
		specific crop in a specific year, based on climate modeling

	:param year: numeric year
	:param field: a Field model, which should have a field boundary (spatial) for location, as well as acreage
	:param crop: a Crop model that associates that crop with other parameters, possibly including a yield curve,
				or functions that can retrieve yields from other APIs
	:param climate: a Climate model instance that provides access to temperature, ET, etc
					- alternatively, the Field instance might have a related model to all of the climate data that's
					been extracted and summarized for the field, and this is just an optional parameter that limits
					what we process to the provided model(s). We'll need to think about this a bit as we proceed.

	Need to consider if there's a way to batch extract the data for this. It's possible that's a preprocessing
	step when we define a field, and that we can then quickly pull timeseries pieces straight from the DB here, but
	need to think about

	:return: monthly water volume timeseries in acre-feet
	"""