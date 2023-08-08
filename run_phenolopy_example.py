from phenolopy import phenolopy
import rioxarray
import seaborn
from matplotlib import pyplot as plt
import pandas

from datetime import datetime

def run():
    data = rioxarray.open_rasterio("/home/nick/Code/FluxCapacitor/phenolopy/test_data/s2_msavi_timeseries_small_area_sample.tif")
    data = data.rename({'band': 'time'})  # the "band" dimension is basically the time dimension
    data['time'] = [datetime.strptime(item.split("_")[1], "%Y-%m-%d") for item in data.long_name]  # parse out times from the long-name field coming from the band name in the TIF and replace the time dimension

    ds = data.to_dataset(name="veg_index")
    outliers_removed = phenolopy.remove_outliers(ds)
    smoothed = phenolopy.smooth(outliers_removed, method="symm_gaussian", window_length=9, polyorder=1)
    results = phenolopy.calc_phenometrics(smoothed.to_array())  # then calculate the phenometrics. This seems to work to a point, then crash when merging the results back together, possibly due to how I'm handling the above.

    print(results)
    return {
            "original": data,
            "outliers_removed_ds": outliers_removed,
            "smoothed_ds": smoothed,
            "results": results
            }



def plot_example(original, no_outliers, smoothed, x=None, y=None, plotall=False):
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
    if x is None:  # if the coordinates aren't provided, just use the origin
        x = int(original.x[0])
    if y is None:
        y = int(original.y[0])

    no_outliers = no_outliers.to_array()
    smoothed = smoothed.to_array()

    if not plotall:
        plot_single(no_outliers, original, smoothed, x, y)
    else:
        for x in range(len(original.x)):
            x_coord = int(original.x[x])
            for y in range(len(original.y)):
                y_coord = int(original.y[y])
                plot_single(no_outliers, original, smoothed, x_coord, y_coord)


def plot_single(no_outliers, original, smoothed, x, y):
    results = {
        "time": original['time'].data,
        "original": original.sel(x=x, y=y).data,
        "no_outliers": no_outliers.sel(x=x, y=y).data[0],
        "smoothed": smoothed.sel(x=x, y=y).data[0]
    }
    rdf = pandas.DataFrame(results)
    rdf.set_index("time", inplace=True)
    plot = seaborn.lineplot(rdf)
    plot.get_figure().savefig(f"/home/nick/Code/FluxCapacitor/plots/plot_vw_{x}_{y}.png")
    plt.clf()


if __name__ == "__main__":
    results = run()
    plot_example(original=results["original"],
             no_outliers=results["outliers_removed_ds"],
             smoothed=results["smoothed_ds"],
            x=630065, y=4087565, plotall=False
             )
    sample_results = results["results"].sel(x=630065, y=4087565)
    print(f"Start of Season: {int(sample_results.sos_times)}")
    print(f"Peak of Season: {int(sample_results.pos_times)}")
    print(f"End of Season: {int(sample_results.eos_times)}")


