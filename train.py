""" I M P O R T:  ###################################################################################################"""


import core
import pandas
import copy


""" G E T   I N T E R F A C E   I N S T A N C E:  ###################################################################"""


def get_interface(interface_core):
    """Returns the Train interface instance."""
    return InterfaceTrain(interface_core)


""" I N T E R F A C E:  #############################################################################################"""


class InterfaceTrain:
    """The interface of the Train module.

    This class contains methods for calculating model parameters.

    Attributes:
        _main_module_object: An instance of the main class.
        _interface_core: An instance of the core interface.
        _interface_data: An instance of the data interface.
    """

    def __init__(self, interface_core: core.InterfaceCore):
        """Inits the interface instance."""
        self._main_module_object = None
        self._interface_core = interface_core
        self._interface_data = interface_core.get_interface_data()

    def nbc_start_train(self, delimiter: str):
        """Calculates parameters for naive bayesian classifier model."""
        self._main_module_object = _NBC(self._interface_core, self._interface_data.get_train_file_name(), delimiter)

        #####################################
        # CALLING METHOD FROM OTHER MODULE! #
        self._interface_data.set_ready_model_nbc(self._main_module_object.get_ready_model())
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
        #####################################


""" M A I N   C L A S S:  ###########################################################################################"""


class _NBC:
    """The main class of the Data module.

    This class contains methods for calculating parameters
        for naive bayesian classifier model.

    Attributes:
        _interface_core: An instance of the core interface.
        _data_frame: A table with training data.
        _v, _d_c, _l_c, _w_c: Parameters for model: log(_d_c/d)+sum(log((_w_c+1)/(_v+_l_c)))
        _model: A dict with all parameters.
            Keys: 'v': _v, 'd_c': _d_c, 'l_c': _l_c, 'w_c': _w_c.
    """

    def __init__(self, interface_core, file_name, delimiter):
        """Inits the interface instance."""
        self._interface_core = interface_core
        self._data_frame = pandas.read_csv(file_name, sep=delimiter, header=None)
        self._v = None
        self._d_c = []
        self._l_c = []
        self._w_c = []
        self._model = {}

    def _count_v(self):
        """Calculates _v."""
        self._v = self._data_frame.iloc[:, 1:].stack().nunique()

    def _count_d_c(self):
        """Calculates _d_c."""
        values = self._data_frame.groupby([0]).size()
        for i in range(0, self._data_frame[0].nunique()):
            self._d_c.append(values[i])

    def _count_l_c(self):
        """Calculates _l_c."""
        for i in range(0, self._data_frame[0].nunique()):
            self._l_c.append(self._data_frame.groupby([0]).count().sum(axis=1)[i])

    def _count_w_c(self):
        """Calculates _w_c."""
        classes = self._data_frame[0].unique()
        for i in range(0, self._data_frame[0].nunique()):
            stacked = self._data_frame.loc[self._data_frame[0] == classes[i]].iloc[:, 1:].stack()
            stacked = stacked.apply(str)
            self._w_c.append(stacked.value_counts().to_dict())

    def get_ready_model(self):
        """Returns variable with all NBC model parameters."""
        self._count_w_c()
        self._count_d_c()
        self._count_v()
        self._count_l_c()
        self._model = {'w_c': self._w_c, 'd_c': self._d_c, 'l_c': self._l_c, 'v': self._v}
        return copy.deepcopy(self._model)


""" E N D   O F   F I L E.  #########################################################################################"""
