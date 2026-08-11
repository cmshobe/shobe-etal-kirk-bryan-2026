# Monte Carlo simulations for estimating total beaver pond sediment storage 
# in the Rocky Mountain region 
# last modified by Katherine Lininger on 9 July 2026

# General description 
# This code uses a dataset taken from published papers on beaver pond sediment 
# storage and beaver pond areas (beaver_sediment_synthesis_data_gsafieldguide.csv) 
# and Monte Carlo simulations to estimate total beaver pond sediment storage
# in the Rocky Mountain physiographic region. Beaver dam counts within the region 
# have scenarios of 100% existing capacity, 150% of existing capacity, 50% existing
# capacity, and historical capacity.


##### load libraries #####
rm(list = ls())
library(purrr)
library(dplyr)
library(tibble)
library(MASS)
library(ggplot2)
library(tidyr)

##### read in data #####
#dataset from literature for pond areas and sediment volumes:
synth_data <- read.csv("beaver_sediment_synthesis_data_gsafieldguide.csv")

#beaver dam counts (historical, existing)
bd_ct <- read.csv(
  file = "RM_bd_ct.csv",
  header = TRUE
)


###### fit non linear regression as a power law #####
synth_data_clean <- na.omit(synth_data[, c("pond_area_m2", "sed_vol_m3")])
model <- lm(log(sed_vol_m3) ~ log(pond_area_m2), data = synth_data_clean)
model2 <- nls(sed_vol_m3 ~ a*pond_area_m2^b, data = synth_data_clean,
              start = list(a = exp(coef(model)[1]), b = coef(model)[2])
)
summary(model2)

# pull NLS residuals and coefficients to use in Monte Carlo simulations
coef_mean_nls <- coef(model2)
coef_vcov_nls <- vcov(model2)

##### MC simulations with nls #####
# set up function
run_mc <- function(
    n_ponds,
    coef_mean,
    coef_vcov,
    pond_area_data,
    n_sim = 10000,
    seed  = 42
) {
  set.seed(seed)
  
  total_volumes_nls   <- numeric(n_sim)

  for (i in seq_len(n_sim)) {
    sim_areas       <- sample(pond_area_data, n_ponds, replace = TRUE)
    # NLS 
    coef_draw_nls   <- mvrnorm(1, mu = coef_mean, Sigma = coef_vcov)
    pred_volume     <- coef_draw_nls[1]*sim_areas^coef_draw_nls[2]     
    
    # sum total volume
    total_volumes_nls[i]   <- sum(pred_volume)
    
  }
  
  ci_nls <- quantile(total_volumes_nls,   c(0.025, 0.975))

  summary_out <- bind_rows(
    tibble(
      modeltype     = "NLS Model",
      estimate       = mean(total_volumes_nls),
      lo_estimate_95 = ci_nls[1],
      hi_estimate_95 = ci_nls[2]
    )
  )
  
  draws_out <- bind_rows(
    tibble(
      simulation   = seq_len(n_sim),
      modeltype   = "NLS Model",
      total_volume = total_volumes_nls
    )
  )
  
  list(summary = summary_out, draws = draws_out)
}

##### define scenarios #####
n_ponds_list <- list(
  ex    = round(bd_ct$dams_ex_tot_ct[1]),
  ex50  = round(bd_ct$dams_ex_tot_ct[1] * 0.5),
  ex150 = round(bd_ct$dams_ex_tot_ct[1] * 1.5),
  hist  = round(bd_ct$dams_hist_tot_ct[1])
)

##### run MC across all scenarios #####
results <- imap(
  n_ponds_list,
  ~ run_mc(
    n_ponds        = .x,
    coef_mean      = coef_mean_nls,
    coef_vcov      = coef_vcov_nls,
    pond_area_data = synth_data_clean$pond_area_m2
  )
)

##### extract summaries and draws #####
all_summaries <- bind_rows(lapply(results, `[[`, "summary"), .id = "scenario")
all_draws     <- bind_rows(lapply(results, `[[`, "draws"),   .id = "scenario")


##### export results #####
write.csv(all_summaries,
          file      = "RM_bd_estimates_5.csv",
          row.names = FALSE)

write.csv(all_draws,
          file      = "RM_bd_draws_5.csv",
          row.names = FALSE)

