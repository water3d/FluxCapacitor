
#
Flux Capacitor
Water balance modeling for agricultural fields using future climate scenarios compared with today.

## Pseudocode Plan
1. User provides field boundary (likely via clicking field boundaries)
2. We pre-extract water balance components from both current and future data files for all models and scenarios
   3. PET
   4. AET
   5. 
3. Calculate additional required water by year/model/scenario
	---- Nick - what actually happens here for a single year/model/scenario? How do we calculate estimated ET
		based on changed atmospheric conditions - likely calculation of PET (penman monteith based on Katherine's feedback)( along with a Kc factor?


Get field/fields boundary and crop information from user
Retrieve consumptive use from OpenET - let user approve (optionally)
Optionally ask user which types of climate models they want - an ensemble mean, hotter, drier, or wetter
Extract data from climate models for ET for the same time as the OpenET data - develop a scaling factor that compares the OpenET value (more accurate) with the climate model value for the same area.
Extract ET for many years in the future from climate models. Use scaling factor to estimate field-level ET. 
Simultaneously, compare total precipitation from those years to total precipitation of the baseline years for a large surrounding area.
Do we need to add any additional water demand based on specific humidity? Or will that be captured in the ET estimate?
Present user with future water need differenced with current water needs (based on ET) - Describe whether the surrounding area is expected to have more, similar, or less water too, so they can assess if they may actually be able to acquire the water or not.


Challenges - much of the scarcity will actually be driven by reductions in precip or pumping restrictions (CA) in some areas, but that's hard to quantify
because of water rights and potential for markets. Can we say "the catchment that flows into your area will lose ___ water",
but then how do we handle water imports in a simple manner?

Still also have the increased ET demand from the atmosphere, but that's only a piece of the puzzle. Need a more comprehensive model


## What's with the name??
It's a reference to both water fluxes (such as via ET) and to Back to the Future, since we're modeling
fields using data for future climate scenarios.


### Installation in a clean Ubuntu Server 22.04 VM
sudo apt-get install python-is-python3
sudo apt-get install python3-pip
sudo apt-get install python3-gdal
python -m pip install geopandas xarray rasterio rioxarray