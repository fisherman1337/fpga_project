from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QMainWindow, QLabel, QGridLayout, \
    QPushButton, QLineEdit, QFileDialog, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPalette


########################################################################################################################
""" G E T   I N T E R F A C E   O B J E C T  ########################################################################"""


def get_interface(interface_core):
    return InterfaceUI(interface_core)


########################################################################################################################
""" I N T E R F A C E  ##############################################################################################"""


class InterfaceUI:

    def __init__(self, interface_core):
        self._main_module_object = UI(interface_core)


########################################################################################################################
""" M A I N   C L A S S  ############################################################################################"""


class UI:
    def __init__(self, interface_core):

        self._interface_core = interface_core
        self._app =                 QApplication([])
        self._main_window =         QMainWindow()
        self._my_tab_widget =       MyTabWidget(interface_core)

        self._main_window.setCentralWidget(self._my_tab_widget)
        self._main_window.setWindowTitle('FPGA')
        self._main_window.setFixedSize(600, 300)
        self._main_window.show()

        self._app.exec_()


########################################################################################################################
""" S E C O N D A R Y   C L A S S  ##################################################################################"""


class MyTabWidget(QWidget):

    def __init__(self, interface_core):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.interface_core = interface_core
        self.interface_data = interface_core.get_interface_data()

        self.tabs =                     QTabWidget()
        self.trn_tab =                  QWidget()
        self.trn_tab.layout =           QGridLayout()
        self.trn_label_choose =         QLabel('Choose training data:')
        self.trn_btn_choose =           QPushButton('Browse...', self)
        self.trn_line_choose =          QLineEdit(self)
        self.trn_label_spacer =         QLabel('')
        self.trn_combobox_alg =         QComboBox()
        self.trn_combobox_frmt =        QComboBox()
        self.trn_label_alg =            QLabel('Algorithm:')
        self.trn_label_frmt =           QLabel('Data format:')
        self.trn_btn_start =            QPushButton('Start training...', self)
        
        self.fpga_tab =                 QWidget()

        self.trn_combobox_alg.addItems(['Naive bayesian classifier', 'Other1', 'Other2'])
        self.trn_combobox_alg.setToolTip(self.trn_combobox_alg.currentText())
        self.trn_combobox_frmt.addItems(['.csv', 'Other1', 'Other2'])
        self.trn_btn_choose.setToolTip('Choose training data...')
        self.trn_btn_choose.clicked.connect(self.show_file_dialog)  # PyCharm bug
        self.trn_tab.layout.setSpacing(5)
        self.trn_combobox_alg.setMaximumWidth(150)
        self.trn_btn_start.clicked.connect(self.start_training)
        self.trn_btn_start.setDisabled(True)
        self.trn_line_choose.textChanged.connect(self.check_line_choose)

        self.trn_tab.layout.addWidget(self.trn_label_alg, 0, 0)
        self.trn_tab.layout.addWidget(self.trn_label_frmt, 0, 1)
        self.trn_tab.layout.addWidget(self.trn_combobox_alg, 1, 0)
        self.trn_tab.layout.addWidget(self.trn_combobox_frmt, 1, 1)
        self.trn_tab.layout.addWidget(self.trn_label_choose, 2, 0)
        self.trn_tab.layout.addWidget(self.trn_btn_choose, 2, 1)
        self.trn_tab.layout.addWidget(self.trn_line_choose, 2, 2)
        self.trn_tab.layout.addWidget(self.trn_btn_start, 3, 0)
        self.trn_tab.layout.addWidget(self.trn_label_spacer, 4, 0, 6, 1)

        self.tabs.addTab(self.trn_tab, "Training")
        self.tabs.addTab(self.fpga_tab, "FPGA")

        self.layout.addWidget(self.tabs)
        self.trn_tab.setLayout(self.trn_tab.layout)
        self.setLayout(self.layout)

    @pyqtSlot()
    def start_training(self):
        print(1)

    @pyqtSlot()
    def show_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose training data...", "", "", options=options)
        if file_name:
            self.trn_line_choose.setText(file_name)

    @pyqtSlot()
    def check_line_choose(self):
        palette = QPalette()
        if self.trn_line_choose.text() is not None:
            self.trn_btn_start.setDisabled(False)
            palette.setColor(QPalette.Text, Qt.green)
            self.trn_line_choose.setPalette(palette)
            self.interface_data.set_train_file(self.trn_line_choose.text())

########################################################################################################################
