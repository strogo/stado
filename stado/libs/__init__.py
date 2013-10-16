import pkgutil

# Support for pystache package.
for loader, module_name, is_pkg in pkgutil.iter_modules(['stado/libs']):
    if module_name == 'pystache':
        pystache = loader.find_module(module_name).load_module(module_name)