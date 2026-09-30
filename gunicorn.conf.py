import multiprocessing
import os

# Unique bind port to prevent conflicts with existing sites on the VPS
bind = os.getenv('GUNICORN_BIND', '127.0.0.1:8001')
pythonpath = '/home/ecomnpits'
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 5))

# Logging configuration
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '/var/log/gunicorn/ecomnpits_access.log')
errorlog = os.getenv('GUNICORN_ERROR_LOG', '/var/log/gunicorn/ecomnpits_error.log')
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
capture_output = True
