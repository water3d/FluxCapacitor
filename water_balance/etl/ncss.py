"""
    tools and class to make working with a NetCDF Subset Service on a THREDDS server easy to work with
"""

# I think we can use siphon and NCSS to do most of our extraction work from the NKN servers, assuming John and Katherine
# agree that this approach is OK. We'll proxy it through one of our own servers, most likely.

# Basically, I think the workflow looks like - pass bounding box start date, end date, and model to extract data for.
# Function requests it from NCSS, then outputs a file as either the raw netCDF4 or something else.
# we then need to get polygon statistics for the data in the netcdf, and we need it as a timeseries. We'll need
# a data structure to hold the data (maybe just the database itself), and then we'll need an approach that extracts
# zonal statistics efficiently across the time slices. xarray-spatial might do this, but we'll want to check if it
# does exactly what we need. An alternative would be extracting the individual time slices and then running rasterstats.
# I'd prefer not to do something like that. Is there already a tool that gives an efficient zonal computation of stats
# across time slices and variables in a netcdf?
#
# the reason to use NCSS before an additional extraction layer would be to avoid the need to load the whole dataset
# into RAM on the server in order to extract the data - it's possible it'd be fine though (and there are some methods
# with, I think, rioxarray or similar that don't load it all. But getting just the exact subset we need by bounding box
# and then pulling out the zonal stats seems like a reasonable starting point.

class NetCDFVariable(object):
    timeslices = list()

class NetCDFTimeslice(object):
    value = None

class NCSSExtract(object):
    def __init__(self):
        pass

    def extract(self, model, start_time, end_time, ):
