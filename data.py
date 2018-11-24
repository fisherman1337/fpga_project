########################################################################################################################
""" G E T   I N T E R F A C E   O B J E C T  ########################################################################"""


def get_interface(interface_core):
    return InterfaceData(interface_core)


########################################################################################################################
""" I N T E R F A C E  ##############################################################################################"""


class InterfaceData:

    def __init__(self, interface_core):
        self._main_module_object = Data(interface_core)

    def set_train_file(self, file_name: str):
        self._main_module_object.set_train_file(file_name)


########################################################################################################################
""" M A I N   C L A S S  ############################################################################################"""


class Data:

    def __init__(self, interface_core):
        self._train_file = None
        self._interface_core = interface_core

    def set_train_file(self, file_name):
        self._train_file = open(file_name, 'r')
        print(self._train_file)


########################################################################################################################