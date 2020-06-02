# The Settings object
#---------------------------
class Settings: pass

Settings.number_of_workplaces = 1000
Settings.number_of_workers_per_workplace = 20

Settings.worker_max_S = 5 # maximum number of job search
Settings.worker_min_S = 0.1 # maximum number of job search
Settings.worker_probability_job_init = 0.9 # Probability of having job when the model starts
Settings.worker_beta = 0.80 # Discounting factor
Settings.worker_delta = 0.01 # Probability of quitting job
Settings.worker_eta = 0.2 # Disutility of searching
Settings.worker_rho = 2 # Risk aversion
Settings.worker_learn = True # Learn about S from others
Settings.worker_learn_n_points = 30 # Number of points in the local_mean
Settings.worker_learn_probabilily = 0.1 # Probabilily of update in learning
Settings.worker_learn_adjustment = 0.15 # Adjustment speed in learning process
Settings.worker_learn_probabilily_mutation = 0.0 # Probabilily of mutation


Settings.workplace_max_gamma = 2.5 # maximum gamma
Settings.workplace_min_gamma = 0.001 # maximum gamma
Settings.workplace_beta = 0.80 # Discounting factor
Settings.workplace_alpha = 0.75 # Cobb-Douglas parameter in production function
Settings.workplace_sigma = 0.001 # Standard deviation of theta's distribution
Settings.workplace_kappa = 0.5 # Unit cost of vacancies
Settings.workplace_learn = True # Learn about gamma from others
Settings.workplace_learn_n_points = 15 # Number of points in the local_mean
Settings.workplace_learn_probabilily = 0.1 # Probabilily of update in learning
Settings.workplace_learn_adjustment = 0.15 # Adjustment speed in learning process
Settings.workplace_learn_probabilily_mutation = 0.0 # Probabilily of mutation

Settings.statistics_update_learn = 10 # How often should learn-information be updated
Settings.statistics_update_learn_adjust = 0.25 # Adjustment speed in learning process

Settings.random_seed=0   # If 0, no seeding
# Settings.random_seed=123   # If 0, no seeding
Settings.graphics_periods_per_pic = 10

Settings.number_of_periods = 200
