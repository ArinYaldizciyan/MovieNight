import pkgutil
import inspect

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
    module = __import__(module_name, fromlist='dummy')
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module_name:
            globals()[name] = obj
