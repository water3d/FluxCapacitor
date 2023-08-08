## Prior to coding
It would be good to verify the centroids of a few polygons have sensible results with the annual timeseries we generated.
We should get the plotting function up to snuff first so we can verify if we think results at centroids look good.


## Preprocessing
Make an index of the tile boundaries

Get centroids of ag fields (force inside polygons)
    spatial join/extract tile that the centroid falls within
    Keep data structure/index of points and which tiles they should extract data from
        and maybe a reverse lookup by tile so that when we process a tile, we can extract all the points of interests'
        data, generate charts, and then discard the data structures

# raster maniupulations
merge the tiles into a VRT with GDAL
Then reextract them into overlapping tiles with the same names as the originals, but with padding from the other original
    tiles around the edge in order to minimize edge effects
    GDAL has an srswin flag where we can specify sizes and offsets. We will need to be smart about the extraction function.
Trash the original files for space savings, unless they take too long to generate again, should we need to change our tiling

Loop through the new tiles and run phenolopy code as in run_phenolopy_example on each one
Then extract parameters per-point as noted above