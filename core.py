from importlib import import_module
from importlib.util import find_spec


########################################################################################################################
""" I N T E R F A C E  ##############################################################################################"""


class InterfaceCore:

    def __init__(self, module_list: list):
        self._main_module_object = Core(self)
        self._main_module_object.load_interface_list(module_list)

    def get_interface_ui(self):
        return self._main_module_object.get_interface('ui')

    def get_interface_train(self):
        return self._main_module_object.get_interface('train')

    def get_interface_data(self):
        return self._main_module_object.get_interface('data')

    def get_interface_by_name(self, name: str):
        return self._main_module_object.get_interface(name)


########################################################################################################################
""" M A I N   C L A S S  ############################################################################################"""


class Core:

    def __init__(self, interface_core):
        self._interface_dict = {}
        self._interface_core = interface_core

    def _check_module(self, module):
        if module in self._interface_dict:
            return False
        elif find_spec(module) is None:
            return False
        else:
            return True

    def _load_interface(self, module_name):
        self._interface_dict[module_name] = import_module(module_name).get_interface(self._interface_core)

    def show_error(self, text_error):
        print(text_error)

    def load_interface_list(self, module_list):
        for mod in module_list:
            if self._check_module(mod):
                self._load_interface(mod)
            else:
                self.show_error('Interface loading error!')

    def get_interface(self, interface_name):
        return self._interface_dict[interface_name]


########################################################################################################################
""" E N T R Y   P O I N T  ##########################################################################################"""


if __name__ == '__main__':
    core = InterfaceCore(['data', 'train', 'ui'])


########################################################################################################################


