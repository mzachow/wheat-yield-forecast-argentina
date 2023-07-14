# NMME

The [North American Multi-Model Ensemble](https://www.cpc.ncep.noaa.gov/products/NMME/)(NMME) consists of six Seasonal climate models whose hindcasts are available [here](http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/). We are not aware of an API, so we collected the NMME System Phase II data manually from their data library. Out of the six models that are part of the NMME, we collected data from four.

- NCAR/University of Miami CCSM4.0 (**CCSM4**)
- GFDL-SPEAR (**GFDL**)
- NASA Goddard Space Flight Center GEOS5 (**GSFC**)
- NOAA NCEP CFSv2 (**NCEP**)
- NCAR CESM - **data for 2011-2015 not available; not considered in this study**
- Environment Canada CanCM3 and CanCM4 - **collected from APCC CLIK; see ../clik/**	

## Information

The data obtained from NMME library is stored in *data/* folder within corresponding subfolders (e.g. *data/NCEP/*). Note: the subfolders will be made available upon request and are not part of this repository. The notebook *netcdf4_hindcasts_to_feature_csv* contains the code that was used to perform the following tasks:

 1. Read data  
   1.1 NMME model output  
   1.2 Polygon shapes of the two Argentinian municipalitites that serve as locations for weather features  
   1.3 Read ERA-Reanalysis CSV that is used for bias adjustment  
 2. Filter NMME model output by location, year, forecasted_month, and init_month
 3. Perform bias-adjustment with quantile mapping
 4. Bring into right structure and combine with ERA data
 5. EXPORT to csv that is saved in *data/features/bias_adjusted_nmme_features.csv*

## Acknowledgments

We acknowledge the agencies that support the NMME-Phase II system, and we thank the climate modeling groups (Environment Canada, NASA, NCAR, NOAA/GFDL, NOAA/NCEP, and University of Miami) for producing and making available their model output. NOAA/NCEP, NOAA/CTB, and NOAA/CPO jointly provided coordinating support and led development of the NMME-Phase II system.


## References

Kirtman, Ben P., and Coauthors, 2014: The North American Multimodel Ensemble: Phase-1 seasonal-to-interannual prediction; Phase-2 toward developing intraseasonal prediction. Bull. Amer. Meteor. Soc., 95, 585–601. doi: http://dx.doi.org/10.1175/BAMS-D-12-00050.1