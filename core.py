""" I M P O R T:  ###################################################################################################"""


import importlib
import importlib.util


""" I N T E R F A C E:  #############################################################################################"""


class InterfaceCore:
    """The interface of the core module.

    This class contains methods, which provide access to the interfaces of any other
        loaded modules. To obtain the interface of a dynamically loaded module,
        it is supposed to use the method get_interface_by_name. Also the class
         allows to call an error message window, using the UI interface.

    Attributes:
        _main_module_object: An instance of the main class.
    """

    def __init__(self, module_list: list):
        """Inits the interface instance."""
        self._main_module_object = _Core(self)
        self._main_module_object.load_interface_list(module_list)

    def get_interface_ui(self):
        """Returns the UI interface instance."""
        return self._main_module_object.get_interface('ui')

    def get_interface_train(self):
        """Returns the Train interface instance."""
        return self._main_module_object.get_interface('train')

    def get_interface_data(self):
        """Returns the Data interface instance."""
        return self._main_module_object.get_interface('data')

    def get_interface_by_name(self, name: str):
        """Returns any loaded interface instance by name."""
        return self._main_module_object.get_interface(name)

    def show_error(self, text_error: str):
        """Shows error message in UI."""
        self._main_module_object.show_error(text_error)


""" M A I N   C L A S S:  ###########################################################################################"""


class _Core:
    """The main class of the core module.

    This class contains methods, which provide check module loading,
       loading modules in the list, showing error window.

    Attributes:
        _interface_dict: Consists instances of interfaces
            of the all loaded modules.
        _interface_core: An instance of the core interface.
    """

    def __init__(self, interface_core):
        """Inits the core instance."""
        self._interface_dict = {}
        self._interface_core = interface_core

    def _check_module(self, module):
        """Checks if module can be loaded."""
        if module in self._interface_dict:
            return False
        elif importlib.util.find_spec(module) is None:
            return False
        else:
            return True

    def _load_interface(self, module_name):
        """Imports module and adds interface."""
        self._interface_dict[module_name] = importlib.import_module(module_name).get_interface(self._interface_core)

    # TODO: Make error message in separate window.
    def show_error(self, text_error):
        """Shows error message in UI."""
        print(text_error)

    def load_interface_list(self, module_list):
        """Loads modules in the list."""
        for mod in module_list:
            if self._check_module(mod):
                self._load_interface(mod)
            else:
                self.show_error('Interface loading error!')

    def get_interface(self, interface_name):
        """Returns any loaded interface instance by name."""
        return self._interface_dict[interface_name]


""" E N T R Y   P O I N T:  #########################################################################################"""


if __name__ == '__main__':
    core = InterfaceCore(['data', 'train', 'ui'])
    interface_ui = core.get_interface_ui()
    #####################################
    # CALLING METHOD FROM OTHER MODULE! #
    interface_ui.start_ui()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    #####################################


""" E N D   O F   F I L E.  #########################################################################################"""
