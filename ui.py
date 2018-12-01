""" I M P O R T:  ###################################################################################################"""


import core
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import threading
import os
import subprocess
import time


""" G E T   I N T E R F A C E   I N S T A N C E:  ###################################################################"""


def get_interface(interface_core):
    """Returns the UI interface instance."""
    return InterfaceUI(interface_core)


""" I N T E R F A C E:  #############################################################################################"""


class InterfaceUI:
    """The interface of the UI module.

    This class contains methods for managing the graphical interface.
        The class allows to call an error message window.

    Attributes:
        _main_module_object: An instance of the main class.
        _interface_core: An instance of the core interface.
    """

    def __init__(self, interface_core: core.InterfaceCore):
        """Inits the interface instance."""
        self._main_module_object = _UI(interface_core)
        self._interface_core = interface_core

    def start_ui(self):
        """GUI launch in new thread."""
        self._main_module_object.start_ui()


""" M A I N   C L A S S:  ###########################################################################################"""


class _UI:
    """The main class of the UI module.

    The class creates and executes a graphical Qt5 application.
    
    Attribute:
        _interface_core: An instance of the core interface.
        _app: An instance of Qt5 Application.
        _main_window: An instance of Qt5 MainWindow.
        _main_tab_widget: An instance of the main widget.
    """

    def __init__(self, interface_core):
        """Inits the UI instance."""

        ###################
        # Initialization: #
        ###################
        self._interface_core = interface_core
        self._app = PyQt5.QtWidgets.QApplication([])
        self._main_window = PyQt5.QtWidgets.QMainWindow()
        self._my_tab_widget = _MyTabWidget(interface_core)

        #############
        # Settings: #
        #############
        self._main_window.setCentralWidget(self._my_tab_widget)
        self._main_window.setWindowTitle('FPGA')
        self._main_window.setFixedSize(600, 300)
        self._main_window.show()

    def start_ui(self):
        """GUI launch."""
        self._app.exec_()


""" S E C O N D A R Y   C L A S S:  #################################################################################"""


class _MyTabWidget(PyQt5.QtWidgets.QWidget):
    """The class of the main widget.

    The class consists all widgets in application and provides
        interaction between them.

    Attributes:
        layout: A layout of the main widget.
        interface_core: An instance of the core interface.
        interface_data: An instance of the data interface.
        palette: An instance of QPalette for color changing.
        tabs: An instance of the tab Qt widget.
        trn_...: Widgets on the 'Train' tab.
        fpga_...: Widgets on the 'FPGA' tab.
    """

    def __init__(self, interface_core):
        """Inits the main widget instance."""

        ###################
        # Initialization: #
        ###################
        PyQt5.QtWidgets.QWidget.__init__(self)
        self.layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.interface_core = interface_core
        self.interface_data = interface_core.get_interface_data()
        self.interface_train = interface_core.get_interface_train()
        self.palette = PyQt5.QtGui.QPalette()
        #################################
        # Initialization of 'info' tab: #
        #################################
        self.info_tab = PyQt5.QtWidgets.QWidget()
        ##################################
        # Initialization of 'train' tab: #
        ##################################
        self.tabs =                     PyQt5.QtWidgets.QTabWidget()
        self.trn_tab =                  PyQt5.QtWidgets.QWidget()
        self.trn_tab.layout =           PyQt5.QtWidgets.QGridLayout()
        self.trn_label_choose =         PyQt5.QtWidgets.QLabel('Choose training data:')
        self.trn_btn_choose =           PyQt5.QtWidgets.QPushButton('Browse...', self)
        self.trn_line_choose =          PyQt5.QtWidgets.QLineEdit(self)
        self.trn_label_spacer =         PyQt5.QtWidgets.QLabel('')
        self.trn_combobox_alg =         PyQt5.QtWidgets.QComboBox()
        self.trn_combobox_frmt =        PyQt5.QtWidgets.QComboBox()
        self.trn_combobox_delim =       PyQt5.QtWidgets.QComboBox()
        self.trn_label_alg =            PyQt5.QtWidgets.QLabel('Algorithm:')
        self.trn_label_frmt =           PyQt5.QtWidgets.QLabel('Data format:')
        self.trn_btn_start =            PyQt5.QtWidgets.QPushButton('Start training...', self)
        self.trn_label_delim =          PyQt5.QtWidgets.QLabel('Delimiter:')
        self.trn_label_training =       PyQt5.QtWidgets.QLabel('Please wait. Training...')
        self.trn_btn_show_model =       PyQt5.QtWidgets.QPushButton('Show model...', self)
        self.trn_label_status =         PyQt5.QtWidgets.QLabel('Status:')
        self.trn_line_status =          PyQt5.QtWidgets.QLineEdit(self)
        #################################
        # Initialization of 'fpga' tab: #
        #################################
        self.fpga_tab =                 PyQt5.QtWidgets.QWidget()

        #############
        # Settings: #
        #############
        self.trn_tab.setLayout(self.trn_tab.layout)
        self.setLayout(self.layout)
        self.palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)
        ############################
        # Settings of 'train' tab: #
        ############################
        self.trn_combobox_alg.addItems(['Naive bayesian classifier', 'Other1', 'Other2'])
        self.trn_combobox_alg.setToolTip(self.trn_combobox_alg.currentText())
        self.trn_combobox_frmt.addItems(['.csv', '.tsv', '.scsv'])
        self.trn_combobox_delim.addItems([',', ';', '\\t'])
        self.trn_btn_choose.setToolTip('Choose training data...')
        self.trn_btn_choose.clicked.connect(self.show_file_dialog)
        self.trn_tab.layout.setSpacing(10)
        self.trn_combobox_alg.setMaximumWidth(150)
        self.trn_combobox_delim.setMaximumWidth(70)
        self.trn_combobox_frmt.activated.connect(self.auto_set_delimiter)
        self.trn_line_choose.setDisabled(True)
        self.trn_btn_start.clicked.connect(self.start_training)
        self.trn_btn_start.setDisabled(True)
        self.trn_line_choose.textChanged.connect(self.check_line_choose)
        self.trn_btn_show_model.setDisabled(True)
        self.trn_btn_show_model.clicked.connect(self.show_model)
        self.trn_line_status.setDisabled(True)
        self.trn_line_status.setText('Choosing train data...')
        self.trn_line_status.setPalette(self.palette)
        self.trn_label_training.setVisible(False)

        ###################
        # Adding widgets: #
        ###################
        self.tabs.addTab(self.info_tab, 'Info')
        self.tabs.addTab(self.trn_tab, 'Training')
        self.tabs.addTab(self.fpga_tab, 'FPGA')
        self.layout.addWidget(self.tabs)
        ##################################
        # Adding widgets on 'train' tab: #
        ##################################
        self.trn_tab.layout.addWidget(self.trn_label_alg, 0, 0)
        self.trn_tab.layout.addWidget(self.trn_label_frmt, 0, 1)
        self.trn_tab.layout.addWidget(self.trn_label_delim, 0, 2)
        self.trn_tab.layout.addWidget(self.trn_label_status, 0, 3)
        self.trn_tab.layout.addWidget(self.trn_combobox_alg, 1, 0)
        self.trn_tab.layout.addWidget(self.trn_combobox_frmt, 1, 1)
        self.trn_tab.layout.addWidget(self.trn_combobox_delim, 1, 2)
        self.trn_tab.layout.addWidget(self.trn_line_status, 1, 3)
        self.trn_tab.layout.addWidget(self.trn_label_choose, 2, 0)
        self.trn_tab.layout.addWidget(self.trn_btn_choose, 2, 1)
        self.trn_tab.layout.addWidget(self.trn_line_choose, 2, 2, 1, 2)
        self.trn_tab.layout.addWidget(self.trn_btn_start, 3, 0)
        self.trn_tab.layout.addWidget(self.trn_label_training, 3, 1)
        self.trn_tab.layout.addWidget(self.trn_btn_show_model, 4, 0)
        self.trn_tab.layout.addWidget(self.trn_label_spacer, 5, 0, 6, 1)

    @PyQt5.QtCore.pyqtSlot()
    def start_training(self):
        """Starts training model."""

        # Changing delimiter in case of tabulation
        delim = self.trn_combobox_delim.currentText()
        if delim == '\\t':
            delim = '\t'

        # Settings for widgets during the training
        self.trn_btn_start.setDisabled(True)
        self.trn_line_status.setText('Training...')
        self.palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)
        self.trn_line_status.setPalette(self.palette)
        self.trn_btn_show_model.setDisabled(True)
        self.trn_label_training.setVisible(True)
        self.trn_btn_show_model.repaint()
        self.trn_btn_start.repaint()
        self.trn_label_training.repaint()

        #####################################
        # CALLING METHOD FROM OTHER MODULE! #
        self.interface_train.nbc_start_train(delim)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
        #####################################

        time.sleep(1)
        # Settings for widgets when the training is over
        self.trn_label_training.setVisible(False)
        self.trn_btn_start.setDisabled(False)
        self.trn_btn_show_model.setDisabled(False)
        self.trn_line_status.setText('Model is ready!')
        self.palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.green)
        self.trn_line_status.setPalette(self.palette)

    @PyQt5.QtCore.pyqtSlot()
    def show_model(self):
        """Shows new window with information about model."""

        # Opening file and get path
        file = open('model_data.txt', 'w')
        path = os.path.abspath('model_data.txt')

        #####################################
        # CALLING METHOD FROM OTHER MODULE! #
        model = self.interface_data.get_ready_model_nbc()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
        #####################################

        # Writing
        file.write('v = %s\n' % model['v'])
        for i in range(0, len(model['d_c'])):
            file.write('\nd_%d = %s' % (i, str(model['d_c'][i])))
            file.write('\nl_%d = %s' % (i, str(model['l_c'][i])))
            file.write('\nw_%d = %s\n' % (i, str(model['w_c'][i])))
        file.close()

        # Open file with 'gedit'
        subprocess.call(["gedit", path])

    @PyQt5.QtCore.pyqtSlot()
    def show_file_dialog(self):
        """Put training data file name in the choose line using the file dialog."""

        # Settings file dialog widget
        opt = PyQt5.QtWidgets.QFileDialog.Options()
        opt |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog

        # Calling file dialog widget in new window
        filt = '*%s' % self.trn_combobox_frmt.currentText()
        file_name, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, "Choose training data...", "",
                                                                   filt, options=opt)

        # Adding train file name in the choose line
        if file_name:
            self.trn_line_choose.setText(file_name)

    @PyQt5.QtCore.pyqtSlot()
    def check_line_choose(self):
        """Checks selected file, changes color of the text and set train file name in data module"""

        # Get train file name from the choose line
        text = self.trn_line_choose.text()

        # Init palette for changing color
        palette = PyQt5.QtGui.QPalette()

        # Checking file name
        if text is not None:

            # If file name is OK - widgets settings
            self.trn_btn_start.setDisabled(False)
            palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.green)
            self.trn_line_choose.setPalette(palette)
            self.trn_line_choose.setToolTip('OK')
            self.palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)
            self.trn_line_status.setPalette(self.palette)
            self.trn_line_status.setText('Ready for training...')

            #####################################
            # CALLING METHOD FROM OTHER MODULE! #
            self.interface_data.set_train_file_name(text)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
            #####################################

        else:

            # If file name is not OK - widgets settings
            self.trn_btn_start.setDisabled(True)
            self.trn_btn_show_model.setDisabled(True)
            palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)
            self.trn_line_choose.setPalette(palette)
            self.trn_line_choose.setToolTip('Cannot open file')
            self.palette.setColor(PyQt5.QtGui.QPalette.Text, PyQt5.QtCore.Qt.red)
            self.trn_line_status.setPalette(self.palette)
            self.trn_line_status.setText('Choosing train data...')

    @PyQt5.QtCore.pyqtSlot()
    def auto_set_delimiter(self):
        """Sets default delimiters for data formats."""
        d = {'.csv': ',',  '.tsv': "\\t", '.scsv': ';'}
        self.trn_combobox_delim.setCurrentText(d[self.trn_combobox_frmt.currentText()])


""" E N D   O F   F I L E.  #########################################################################################"""
