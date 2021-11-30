#Explore model results

#set up
#install.packages("tidyverse")
#install.packages("vegan")
#install.packages("here")
library(tidyverse)
library(vegan)
library(here)

res <- read_csv(here("model_results.csv"))

#clean data

res <- res %>% 
  #drop empty rows
  drop_na(results) %>%
  #add indicator for unique groups of parameters/ initial conditions
  add_count(initial_otter,
            initial_empty,
            initial_kelp,
            initial_urchin,
            #name of new column
            name = "init_group"
            ) %>%
  add_count(kelp_reprod_prob,
            kelp_reprod_age,
            kelp_death_age,
            urchin_reprod_prob,
            urchin_reprod_age,
            urchin_death_age,
            otter_reprod_prob,
            otter_reprod_age,
            otter_death_age,
            otter_carrying_capacity,
            name = "param_group") %>%
  group_by(initial_otter,
           initial_empty,
           initial_kelp,
           initial_urchin) %>%
  mutate(init_group_id = cur_group_id()) %>%
  ungroup() %>%
  group_by(kelp_reprod_prob,
           kelp_reprod_age,
           kelp_death_age,
           urchin_reprod_prob,
           urchin_reprod_age,
           urchin_death_age,
           otter_reprod_prob,
           otter_reprod_age,
           otter_death_age,
           otter_carrying_capacity) %>%
  mutate(param_group_id = cur_group_id())

# do the results differ for different intial conditions for the same parameter/ intital condition values? 
ggplot(data = res) +
  geom_bar(aes(x = init_group_id, fill = results)) + 
  scale_y_continuous(breaks = c(3,6,9,12,15,18,21))
ggplot(data = res) +
  geom_bar(aes(x = param_group_id, fill = results)) + 
  scale_y_continuous(breaks = c(3,6,9,12,15,18,21))
  
  
  
