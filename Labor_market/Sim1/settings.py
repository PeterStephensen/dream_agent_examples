# The Settings object
#---------------------------
class Settings: pass

Settings.number_of_workplaces = 500
Settings.number_of_workers_per_workplace = 20

Settings.worker_max_S = 5 # maximum number of job search
Settings.worker_min_S = 0.1 # maximum number of job search
Settings.worker_probability_job_init = 0.9 # Probability of having job when the model starts
Settings.worker_beta = 0.95 # Discounting factor
Settings.worker_delta = 0.05 # Probability of quitting job
Settings.worker_disutility = 5

Settings.workplace_max_gamma = 2.0 # maximum gamma
Settings.workplace_min_gamma = 0.2 # maximum gamma
Settings.workplace_beta = 0.95 # Discounting factor
Settings.workplace_alpha = 0.75 # Cobb-Douglas parameter in production function
Settings.workplace_sigma = 0.05 # Standard deviation of theta's distribution
Settings.workplace_kappa = 0.5 # Unit cost of vacancies

Settings.number_of_periods = 500

Settings.graphics_periods_per_pic = 10
