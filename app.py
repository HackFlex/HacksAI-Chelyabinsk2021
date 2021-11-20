import sys
from PySide6 import QtCore, QtWidgets

class Dispatcher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout_left = QtWidgets.QVBoxLayout()
        self.layout_right = QtWidgets.QVBoxLayout()
        self._init_loader()
        self._init_params()
        self._init_stream()
        
        self.layout_out = QtWidgets.QHBoxLayout()
        self.layout_out.addLayout(self.layout_left)
        self.layout_out.addLayout(self.layout_right)
        self.setLayout(self.layout_out)

    def _init_loader(self):
        self.lbl_path = QtWidgets.QLabel()
        self.line_path = QtWidgets.QLineEdit('')
        # self.line_path.setDisabled(True)

        self.btn_browse = QtWidgets.QPushButton('ОБЗОР')
        self.btn_browse.setToolTip("Open Image/Video File")
        self.btn_browse.setStatusTip("Open Image/Video File")
        # self.btn_browse.setFixedHeight(24)
        self.btn_browse.clicked.connect(self.setPathFile)

        self.btn_load = QtWidgets.QPushButton('ЗАГРУЗИТЬ')
        self.btn_load.clicked.connect(self.openFile)

        self.layout_left.addWidget(self.line_path)
        self.layout_left.addWidget(self.btn_browse)
        self.layout_left.addWidget(self.btn_load)
        self.layout_left.addWidget(self.lbl_path)

    def _init_params(self):
        self.lbl_params = QtWidgets.QLabel()
        self.lbl_params.setText('Parameters')

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(1)
        self.table.setRowCount(6)
        self.table.horizontalHeader().hide()
        self.table.setVerticalHeaderLabels(['X', 'Y', 'Z', 'крен', 'тангаж', 'рыскание'])
        self.table.setDisabled(True)
        
        self.layout_left.addWidget(self.lbl_params)
        self.layout_left.addWidget(self.table)

    def _init_stream(self):
        self.lbl_stream = QtWidgets.QLabel()
        self.lbl_stream.setText('STREAM')

        self.layout_right.addWidget(self.lbl_stream)

    @QtCore.Slot()
    def setPathFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie",
                QtCore.QDir.homePath())
        filename = str(filename)
        if filename != '':
            self.line_path.setText(filename)

    @QtCore.Slot()
    def openFile(self):
        filename = self.line_path.text()
        if filename != '':
            file = filename.split('/')[-1]
            self.lbl_path.setText(f'File: {file}')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Dispatcher()
    widget.resize(1000, 800)
    widget.show()

    sys.exit(app.exec())
