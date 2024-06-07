import multiprocessing


# Gunicorn configuration variables
bind = "0.0.0.0:9000"
daemon = False
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 3
debug = False
accesslog = "access.log"  # Access logs file
errorlog = "-"    # Disable gunicorn access logs
loglevel = "info"
# pidfile = "gunicorn.pid"
