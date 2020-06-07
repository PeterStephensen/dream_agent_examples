class Settings():
    household_search_number_of_firms=10
    household_probability_search=0.1 # Probability of search when you are employied
    number_of_households = 1000

    number_of_firms = 100
    firm_init_wage_mean = 0
    firm_init_wage_sd = 0.3 # Sd in initial log-normal wage distribution
    
    firm_min_employment = 1 # L_bar in the documentation
    firm_initial_vacancies = 3 
    firm_alpha = 0.6       # Cobb-Douglas parameter
    
    firm_wage_markup = 0.005
    firm_wage_markdown = 0.005
    
    firm_log_theta_initial_mean = 2
    firm_log_theta_initial_sd = 0.5
    
    firm_log_theta_error_mean = 0
    firm_log_theta_error_sd = 0
    
    firm_number_of_new_born = 1
    
    firm_credit_limit = -100 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    firm_reserve_target_wagesum_parameter = 0.8 # Zeta in the documentation
    firm_buffer_stock_speed = 0.5 # Gamma in the documentation (< 1)
    
    firm_wage_reaction = 0.05 # E in documentation (< 1)
    
    firm_calc_variables_max_iterations=50
    firm_calc_variables_error_ok = 1e-6

    random_seed=0   # If 0, no seeding
    
    graphics_show=True
    graphics_periods_per_pic = 100
    graphics_file = "smalltown//smalltown1//plots//pic.png"

    interest_rate = 0.05/12
    price = 1 # The exogeneous international good price

    number_of_periods = 10000
