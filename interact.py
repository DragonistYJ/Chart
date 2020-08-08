from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class DirListObj(QObject):
    sig_file_item_clicked = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot(str)
    def file_item_clicked(self, file_id):
        # 文件列表中的一个data文件被点击
        self.sig_file_item_clicked.emit(int(file_id.split("_")[1]))
