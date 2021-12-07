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
  #fix result string - replace NA with neither
  mutate(results = results %>%
           str_replace_na() %>%
           str_replace(.,
                       pattern = "NA",
                       replacement = "neither")) %>%
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
ggplot(data = res %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp_urchin",
                              replacement = "Kelp with Urchins")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp",
                              replacement = "Kelp Forest")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "urchin",
                              replacement = "Urchin Barren")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "neither",
                              replacement = "None"))) +
  geom_bar(aes(x = init_group_id, fill = results)) + 
  scale_y_continuous(breaks = c(3,6,9,12,15,18,21,24,27)) + 
  theme_classic() +
  labs(title = "The number of ecosystem types detected for each set of parameters",
       x = "Parameter set") + 
  scale_fill_discrete(breaks = c("Kelp Forest", 
                                   "Urchin Barren", 
                                   "Kelp with Urchins", 
                                   "None"),
                        name = "Ecosystem type")
  
ggplot(data = res %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp_urchin",
                              replacement = "Kelp with Urchins")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp",
                              replacement = "Kelp Forest")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "urchin",
                              replacement = "Urchin Barren")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "neither",
                              replacement = "None"))) +
  geom_bar(aes(x = param_group_id, fill = results)) + 
  scale_y_continuous(breaks = c(3,6,9,12,15,18,21,24,27)) + 
  theme_classic() +
  labs(title = "The number of ecosystem types detected for each set of initial conditions",
       x = "Initial condition set") + 
  scale_fill_discrete(breaks = c("Kelp Forest", 
                                   "Urchin Barren", 
                                   "Kelp with Urchins", 
                                   "None"),
                        name = "Ecosystem type")

#how do the outcomes differ based on different parameters?
ggplot(data = res #%>%
         #filter(otter_carrying_capacity==1)
       ) + 
  geom_point(aes(x=initial_otter, y = urchin_reprod_prob, colour = results)) +
  facet_wrap(~otter_reprod_age)
  
ggplot(data = res #%>%
       #filter(otter_carrying_capacity==1)
) + 
  geom_point(aes(x=initial_otter, y = urchin_death_age, colour = results)) +
  facet_wrap(~otter_reprod_age)

ggplot(data = res #%>%
       #filter(otter_carrying_capacity==1)
) + 
  geom_point(aes(x=initial_otter, y = kelp_death_age, colour = results)) +
  facet_wrap(~otter_reprod_age)

ggplot(data = res #%>%
       #filter(otter_carrying_capacity==1)
) + 
  geom_point(aes(x=initial_otter, y = initial_kelp, colour = results)) +
  facet_wrap(~otter_reprod_age)

ggplot(data = res #%>%
       #filter(otter_carrying_capacity==1)
) + 
  geom_point(aes(x=initial_otter, y = initial_urchin, colour = results)) +
  facet_wrap(~otter_reprod_age)

#urchin reproduction vs otter presence

ggplot(data = res %>%
       filter(otter_carrying_capacity==1) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp_urchin",
                              replacement = "Kelp with Urchins")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp",
                              replacement = "Kelp Forest")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "urchin",
                              replacement = "Urchin Barren")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "neither",
                              replacement = "None"))) + 
  geom_jitter(aes(x=initial_otter, 
                  y = urchin_reprod_prob, 
                  colour = results),
              size = 1,
              width = 0.15,
              height = 0.3) + 
  theme_classic() +
  labs(title = "The effect of urchin reproduction probablilty and\nconsumption pressure on urchins on ecosytem type",
       x = "Consumption pressure on urchins (%)",
       y = "Urchin reproduction probability (%)") +
  scale_colour_discrete(breaks = c("Kelp Forest", 
                                   "Urchin Barren", 
                                   "Kelp with Urchins", 
                                   "None"),
                        name = "Ecosystem type")


#plot of proportion of resulting ecosytems
ggplot(data = res %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp_urchin",
                              replacement = "Kelp with Urchins")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "kelp",
                              replacement = "Kelp Forest")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "urchin",
                              replacement = "Urchin Barren")) %>%
         mutate(results = results %>%
                  str_replace(.,
                              pattern = "neither",
                              replacement = "None"))) + 
  geom_bar(aes(x = results)) +
  theme_classic() +
  labs(title = "The number of each ecosytem type seen in the model probing",
       x = "Ecosytem type",
       y = "Count") 

nrow(res %>%
       filter(results == "urchin"))


  
