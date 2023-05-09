import sys
#sys.path.insert(0, r"C:\Users\dsx\.conda\pkgs\libgdal-3.6.3-hd256549_1\Library\bin")

import os
#os.environ["GDAL_DATA"] = r"C:\Users\dsx\.conda\pkgs\libgdal-3.6.3-hd256549_1\Library\share\gdal"
#os.environ["GDAL_CONFIG"] = r"C:\Users\dsx\.conda\pkgs\libgdal-3.6.3-hd256549_1\Library\bin\gdal-config"

# from rasterio import features, transform
import geopandas
import rioxarray

current_folder = os.path.dirname(os.path.abspath(__file__))

def simple_extraction(data_file=os.path.join(current_folder, "data", "mean_et_2020-2020-05-01--2020-05-31__swf_sseb_monthly_v2_mosaic.tif"),
						   zone_shp=os.path.join(current_folder, "data", "tlb_boundary.shp")):
	"""
		This was meant to be a way to test if xrspatial can extract a subset of an xarray. I'm not sure if it can do it
		at all though - it might pass that kind of task off to a GDAL-backed item.
	:param data_file:
	:param zones:
	:return:
	"""

	mask = geopandas.read_file(zone_shp)
	# mask = features.geometry_mask(zone_shp, (10, 10), transform.Affine.identity())
	print("Mask opened")
	xarray_raster = rioxarray.open_rasterio(data_file)
	print("Raster opened")
	#clipped_raster = xarray_raster.rio.clip_box(mask.geometry, mask.crs)
	#print("Raster clipped to bbox")
	clipped_raster = xarray_raster.rio.clip(mask.geometry.values, mask.crs, drop=False, invert=True, from_disk=True)
	print("Raster fully clipped")
	clipped_raster.plot()

simple_extraction()