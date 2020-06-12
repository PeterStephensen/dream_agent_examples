# The Settings object
#---------------------------
class Settings():
    number_of_workplaces = 1000
    number_of_workers_per_workplace = 20

    worker_max_S = 5 # maximum number of job search
    worker_min_S = 0.1 # maximum number of job search
    worker_probability_job_init = 0.9 # Probability of having job when the model starts
    worker_beta = 0.80 # Discounting factor
    worker_delta = 0.01 # Probability of quitting job
    worker_eta = 0.2 # Disutility of searching
    worker_rho = 2 # Risk aversion
    worker_learn = True # Learn about S from others
    worker_learn_n_points = 30 # Number of points in the local_mean
    worker_learn_probabilily = 0.1 # Probabilily of update in learning
    worker_learn_adjustment = 0.15 # Adjustment speed in learning process
    worker_learn_probabilily_mutation = 0.0 # Probabilily of mutation

    workplace_max_gamma = 2.5 # maximum gamma
    workplace_min_gamma = 0.001 # maximum gamma
    workplace_beta = 0.80 # Discounting factor
    workplace_alpha = 0.75 # Cobb-Douglas parameter in production function
    workplace_sigma = 0.001 # Standard deviation of theta's distribution
    workplace_kappa = 0.5 # Unit cost of vacancies
    workplace_learn = True # Learn about gamma from others
    workplace_learn_n_points = 15 # Number of points in the local_mean
    workplace_learn_probabilily = 0.1 # Probabilily of update in learning
    workplace_learn_adjustment = 0.15 # Adjustment speed in learning process
    workplace_learn_probabilily_mutation = 0.0 # Probabilily of mutation

    statistics_update_learn = 10 # How often should learn-information be updated
    statistics_update_learn_adjust = 0.25 # Adjustment speed in learning process

    random_seed=0   # If 0, no seeding
#   random_seed=123   # If 0, no seeding
    graphics_periods_per_pic = 10

    number_of_periods = 200
