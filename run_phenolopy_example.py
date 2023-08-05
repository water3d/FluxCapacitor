from phenolopy import phenolopy
import rioxarray
import seaborn
from matplotlib import pyplot as plt

from datetime import datetime

def run():
    data = rioxarray.open_rasterio("/home/nick/Code/FluxCapacitor/phenolopy/test_data/s2_msavi_timeseries_sample.tif")
    data = data.rename({'band': 'time'})  # the "band" dimension is basically the time dimension
    data['time'] = [datetime.strptime(item.split("_")[1], "%Y-%m-%d") for item in data.long_name]  # parse out times from the long-name field coming from the band name in the TIF and replace the time dimension

    results = phenolopy.calc_phenometrics(data)  # then calculate the phenometrics. This seems to work to a point, then crash when merging the results back together, possibly due to how I'm handling the above.

    print(results)
    return results


def plot_example(data_array, x, y):
    """
        The following will plot the timeseries for a given x or y (in the units of the coordinate system. We could
        make something that retrieves the coordinates for a pixel grid x/y too, but this uses the coordinates, as
        xarray does when loading from rasterio.

        Could probably make something that plugs into ArcGIS or QGIS to show this when clicking a pixel, but it's a lot
        of data to keep in the background. Probably faster if we preprocess it spatially into timeseries in a SQL database
        or something rather than keeping it in rasters that we have to load/traverse. Or if we do that, we need
        a data format that allows an arbitrary read (can geoparquet do that for us???).

        Ultimately, I think we want something like what they have on their website - show input timeseries,
        show smoothed timeseries, plot phenometrics on top of it. We might just need to build a data processing
        pipeline that allows us to plug in a year and a grid section, it downloads the S2 data and runs the whole pipeline,
        then lets you plot up the phenometrics in the browser. That'd be a nice application and good for data QA.

        How much time would it take us to make that?
            S2 STAC -> MSAVI calculation service -> phenolopy -> storage -> plotting
        Need some kind of service running on top that runs it for a giant area and comes back with aggregate stats for
        ag regions, I think.

        Last thing, we need to check how much impact we're getting from clouds. Is the algorithm properly smoothing? Is
        it generating the correct phenometrics?
    """
    seaborn.lineplot(x=data_array['time'].data, y=data_array.sel(x=x, y=y).data)
    plt.show()

results = run()
