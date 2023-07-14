# CLIK APCC

The [Climate Information Toolkit (CLIK) from the APEC Climate Center (APCC)](https://cliks.apcc21.org/)(CLIK) consists of fifteen Seasonal climate models whose hindcasts are available to download [here](https://cliks.apcc21.org/dataset/model). Alternatively, CLIK has an API that we used in our research. More information is available [here](https://cliks.apcc21.org/contents/openapi). Out of the fifteen models that are part of the APCC MME, we collected data from five. Partly because some data was not consistently available for all years and months of initialization, and partly because the data was already collected from the NMME or the Copernicus Climate Data Store (more in *../c3s/* or *../nmme/*)

- BoM ACCESS-S2 from Australia - **BOM**
- PNU-RDA CGCMv2.0 from Korea - **PNU**
- CWB TCWB1Tv1.1 from Chinese Taipei - **CWB**
- HMC SL-AV from Russia - **HMC**
- KMA GloSea6GC3.2 from Korea - **KMA**
- NCEP CFSv2 from the USA - **collected from NMME**
- METFR SYS8 from France - **collected from C3S**
- CMCC SOS3.5 from Italy - **collected from C3S**
- UKMO GloSea6 from the UK - **collected from C3s**
- ECCC CANSIPSv2.1 from Canada - **collected from C3S**
- APCC SCoPS from Korea - **not considered, because of missing data**
- BCC CSM1.1m from China - **not considered, because of missing data**
- MGO MGOAM-2 grom Russia - **not considered, because of missing data**


## Information

First, we use the notebook *clik_api* to obtain the hindcast data of a specific model from the CLIK API. After the job is finished, the raw hindcasts is manually moved into the *data/* folder and then into the subfolders corresponding to the seasonal climate model (e.g. *data/BOM/*). Note: the subfolders will be made available upon request and are not part of this repository. The notebook *netcdf4_hindcasts_to_feature_csv* contains the code that was used to perform the following tasks:

 1. Read data  
   1.1 Output of specified CLIK model  
   1.2 Polygon shapes of the two Argentinian municipalitites that serve as locations for weather features  
   1.3 Read ERA-Reanalysis CSV that is used for bias adjustment  
 2. Filter CLIK model output by location, year, forecasted_month, and init_month
 3. Perform bias-adjustment with quantile mapping
 4. Bring into right structure and combine with ERA data
 5. EXPORT to csv that is saved in *data/features/bias_adjusted_clik_features.csv*

## Acknowledgments

We acknowledge the APCC MME Producing Centers for making their hindcast/forecast data available for analysis, the APEC Climate Center for collecting and archiving the data, as well as for producing APCC MME predictions.

