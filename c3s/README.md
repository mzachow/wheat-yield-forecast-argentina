# Copernicus Climate Change Service (C3S)

The [Copernicus Climate Change Service operated by the ECMWF](https://cds.climate.copernicus.eu/cdsapp#!/home)(C3S) offers access to eight Seasonal climate models whose hindcasts are available to download [here](https://cds.climate.copernicus.eu/cdsapp#!/dataset/seasonal-monthly-single-levels?tab=overview). Alternatively, C3S has an API that we used in our research. More information is available [here](https://cds.climate.copernicus.eu/api-how-to). Out of the eight models that are available at C3S, we collected data from seven. Data from NCEP was already collected from the NMME (more in *../nmme/*)

- ECWMF SEAS5 from the EU - **ECMWF**
- CMCC CM2 from Italy - **CMCC**
- DWD GCFS2.1 from Germany - **DWD**
- ECCC CanCM4i from Canada - **ECCC**
- JMA cps from Japan - **JMA**
- Météo-France System8 from France - **METFR**
- UKMO HadGEM3 from the UK- **UKMO**
- NCEP CFSv2 from the USA - **collected from NMME**


## Information

First, we use the notebook *c3s_api* to obtain the hindcast data of a specific model from the C3S API. After the job is finished, the raw hindcasts is manually moved into the *data/* folder and then into the subfolders corresponding to the seasonal climate model (e.g. *data/ECMWF/*). Note: the subfolders will be made available upon request and are not part of this repository. The notebook *grib_hindcasts_to_feature_csv* contains the code that was used to perform the following tasks:

 1. Read data  
   1.1 Output of specified C3S model  
   1.2 Polygon shapes of the two Argentinian municipalitites that serve as locations for weather features  
   1.3 Read ERA-Reanalysis CSV that is used for bias adjustment  
 2. Filter C3S model output by location, year, forecasted_month, and init_month
 3. Perform bias-adjustment with quantile mapping
 4. Bring into right structure and combine with ERA data
 5. EXPORT to csv that is saved in *data/features/bias_adjusted_c3s_features.csv*

## Acknowledgments

Our analysis contains modified Copernicus Climate Change Service information 2023. Neither the European Commission nor any modelling group is responsible for any use that may be made of the Copernicus information or data it contains.

