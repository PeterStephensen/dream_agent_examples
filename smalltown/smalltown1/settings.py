class Settings():
    household_search_number_of_firms=10
    number_of_households = 10000

    number_of_firms = 1000

    firm_init_wage_mean = -1 # Mean in initial log-normal wage distribution. LOW WAGE to start
    firm_init_wage_sd = 0.1 # Sd in initial log-normal wage distribution

    firm_min_employment = 4 # L_bar in the documentation
    firm_alpha = 0.75       # Cobb-Douglas parameter
    firm_log_theta_initial_mean = 0
    firm_log_theta_initial_sd = 0.05
    firm_log_theta_error_mean = 0
    firm_log_theta_error_sd = 0.005
    firm_number_of_new_born = 5

    random_seed=0   # If 0, no seeding
    graphics_periods_per_pic = 10
    graphics_file = "smalltown//smalltown1//plots//pic.png"

    number_of_periods = 500
