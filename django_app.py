import sys
sys.path.insert(0, '.')
from helloworld import wsgi

app = wsgi.application