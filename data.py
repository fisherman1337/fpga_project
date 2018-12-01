""" I M P O R T:  ###################################################################################################"""


import core
import copy


""" G E T   I N T E R F A C E   I N S T A N C E:  ###################################################################"""


def get_interface(interface_core):
    """Returns the Data interface instance."""
    return InterfaceData(interface_core)


""" I N T E R F A C E:  #############################################################################################"""


class InterfaceData:
    """The interface of the Data module.

    This class contains methods for storing and retrieving
        data necessary for the entire program.

    Attributes:
        _main_module_object: An instance of the main class.
        _interface_core: An instance of the core interface.
    """

    def __init__(self, interface_core: core.InterfaceCore):
        """Inits the interface instance."""
        self._main_module_object = _Data(interface_core)
        self._interface_core = interface_core

    def set_train_file_name(self, file_name: str):
        """Sets the name of file with training data."""
        self._main_module_object.set_train_file_name(file_name)

    def get_train_file_name(self):
        """Returns the name of file with training data."""
        return self._main_module_object.get_train_file_name()

    def set_ready_model_nbc(self, model: dict):
        """Sets the variable with NBC model parameters."""
        self._main_module_object.set_ready_model_nbc(model)

    def get_ready_model_nbc(self):
        """Returns a copy of variable with NBC model parameters.
        Keys in model: 'v': _v, 'd_c': _d_c, 'l_c': _l_c, 'w_c': _w_c."""
        return self._main_module_object.get_ready_model_nbc()


""" M A I N   C L A S S:  ###########################################################################################"""


class _Data:
    """The main class of the Data module.

    This class contains methods for storing and retrieving
        data necessary for the entire program.

    Attributes:
        _interface_core: An instance of the core interface.
        _train_file_name: Name of file with training data.
        _ready_model_nbc: A variable with NBC model parameters.
    """

    def __init__(self, interface_core):
        """Inits the main class instance."""
        self._interface_core = interface_core
        self._train_file_name = None
        self._ready_model_nbc = None

    # TODO: Make LOCK in case of more then one thread calling this method.
    def set_train_file_name(self, file_name):
        """Sets the name of file with training data."""
        self._train_file_name = file_name

    def get_train_file_name(self):
        """Returns the name of file with training data."""
        return copy.deepcopy(self._train_file_name)

    # TODO: Make LOCK in case of more then one thread calling this method.
    def set_ready_model_nbc(self, model):
        """Sets the variable with NBC model parameters."""
        self._ready_model_nbc = model

    def get_ready_model_nbc(self):
        """Returns a copy of variable with NBC model parameters."""
        return copy.deepcopy(self._ready_model_nbc)


""" E N D   O F   F I L E.  #########################################################################################"""
