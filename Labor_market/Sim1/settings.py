# The Settings object
#---------------------------
class Settings: pass

Settings.number_of_workplaces = 1000
Settings.number_of_workers_per_workplace = 20

# Settings.worker_max_S = 1.5 # maximum number of job search
# Settings.worker_min_S = 1.5 # maximum number of job search
Settings.worker_max_S = 5 # maximum number of job search
Settings.worker_min_S = 0.1 # maximum number of job search
Settings.worker_probability_job_init = 0.9 # Probability of having job when the model starts
Settings.worker_beta = 0.80 # Discounting factor
Settings.worker_delta = 0.15 # Probability of quitting job
Settings.worker_eta = 0.2 # Disutility of searching
Settings.worker_rho = 2 # Risk aversion

# Settings.workplace_max_gamma = 0.3 # maximum gamma
# Settings.workplace_min_gamma = 0.3 # maximum gamma
Settings.workplace_max_gamma = 1.5 # maximum gamma
Settings.workplace_min_gamma = 0.01 # maximum gamma
Settings.workplace_beta = 0.80 # Discounting factor
Settings.workplace_alpha = 0.75 # Cobb-Douglas parameter in production function
Settings.workplace_sigma = 0.0 # Standard deviation of theta's distribution
Settings.workplace_kappa = 0.5 # Unit cost of vacancies

Settings.random_seed=0   # If 0, no seeding
#Settings.random_seed=123   # If 0, no seeding
Settings.graphics_periods_per_pic = 10
Settings.number_of_periods = 500
