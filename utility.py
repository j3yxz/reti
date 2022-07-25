import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("(%(threadName)-10s) %(message)s")
out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.DEBUG)
out_handler.setFormatter(formatter)
log.addHandler(out_handler)