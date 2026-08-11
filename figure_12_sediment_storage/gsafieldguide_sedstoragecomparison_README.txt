-------------------
GENERAL INFORMATION
-------------------


1. Title of Dataset:  
Datasets and files associated with figure 12 in "Changing streamflow and sediment dynamics in rivers of the southern Colorado Rockies", Geological Society of America field guide for the 2026 Kirk Bryan field trip

2. Authors: 
Shobe, C.M., K.B. Lininger, and S. Warix

3. Contact information:
katherine.lininger@colorado.edu


---------------------------------------------------------------
DATA & FILE LIST, DESCRIPTIONS, AND RELATIONSHIPS BETWEEN FILES
---------------------------------------------------------------


1. Filename: rm_reservoir_sedstorage_y2025_m3.csv

This dataset contains the predicted sediment storage volumes in the year 2025 for the dams included in the Rocky Mountain Region; methods are described in Eckland et al., in review. Columns include: 
	NID: National Inventory of Dams ID
	sedstorage_y2025_m3: volume of sediment stored in year 2025, m^3
	sedstorage_ci_hi_y2025_m3: high bound of 95% confidence interval from year 2025 sediment storage predicted
	using multiple linear regression model, m^3
	sedstorage_ci_lo_y2025_m3: low bound of 95% confidence interval from year 2025 sediment storage predicted 	using multiple linear regression model, m^3

2. Filename: resnet_attributes_gsafieldguide.csv

This csv file is the ResNet attribute file for ResNet, which is used for determining sediment storage volumes in human built reservoirs in year 2025 (see file: rm_reservoir_sedstorage_y2025_m3.csv). For variable definitions and explanations, see Hurst, A. A., Foster, M. A., & Eckland, A. C. (2025). The ResNet network of dams impounding storage reservoirs across the continental United States. Scientific Data. https://doi.org/10.1038/s41597-025-06315-8


3. Filename: RM_bd_ct.csv

This csv file contains the total number of beaver dams in the Rocky Mountain physiographic region for existing beaver dam capacity and historical beaver dam capacity, using the Beaver Restoration Assessment Tool (Macfarlane et al., 2017). Columns include:
	dams_ex_tot_ct: beaver dam count in Rocky Mountain region based on existing capacity
	dams_hist_tot_ct: beaver dam count in Rocky Mountain region based on historical capacity


4. Filename: beaver_sediment_synthesis_data_gsafieldguide.csv

This csv file contains data on beaver pond areas and beaver pond sediment volumes taken from a literature review, used within the Monte Carlo simulations to estimate total sediment storage in beaver ponds for the Rocky Mountain Region. Columns include: 
	country: country in which beaver pond is located	
	state: state in which beaver pond is located
	reference: peer-reviewed references from where the information on the pond comes from
	watershed: watershed in which the beaver pond is located
	latitude: latitude of beaver pond
	longitude: longitude of beaver pond
	pond_area_m2: beaver pond area, m^2
	sed_vol_m3: sediment volume in beaver pond, m^3


5. Filename: rm_MCsims_v5_gsafieldguide.R

This R script uses the RM_bd_ct.csv file and the beaver_sediment_synthesis_data_gsafieldguide.csv file to conduct Monte Carlo simulations of total sediment storage in beaver ponds in the Rocky Mountain region. Output includes the mean of 10,000 Monte Carlo simulation draws, the 2.5 and 97.5 percentiles from 10,000 Monte Carlo simulation draws, and a file with all 10,000 Monte Carlo simulation draws.

6. Filename: sedstorage_estimates_km3_gsafieldguide.csv

This csv file includes the sediment storage estimates and uncertainties used to plot figure 12 in the GSA field guide. Columns include: 
	label: ex: beaver pond sediment storage at existing capacity; hist: beaver pond sediment storage at 	historical capacity; sed_2025: sediment storage in human built reservoirs
	estimate_km3: sediment storage volume, km^3
	ci_lo_km3: low bound of 95% interval as described in figure 12 caption, km^3
	ci_hi_km3: high bound of 95% interval as described in figure 12 caption, km^3



