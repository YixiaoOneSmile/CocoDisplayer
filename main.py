from PIL.ImageQt import ImageQt
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QListWidgetItem
from main_win.main import Ui_MainWindow
from PyQt6.QtGui import QImage, QPixmap, QPainter, QIcon

from utils.parse import *
import sys
import os
from PIL import Image
from CocoHelper import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 变量定义
        self.coco_helper = None
        self.images = []
        self.annotation_path = 'D:/2022/ap10k/ap10k/annotations/ap10k-test-split1.json'
        self.images_path = 'D:/2022/ap10k/ap10k/data'
        self.image_begin = 0
        self.image_end = 0

        # 信号与连接
        self.show_image_button.clicked.connect(self.images_list_init)
        self.images_listWidget.itemSelectionChanged.connect(self.image_show)
        self.select_image_path_button.clicked.connect(self.select_image_path)
        self.select_annotation_path_button.clicked.connect(self.select_annotation_path)
        self.main_image = None
        self.main_pixmap = None

    def images_list_init(self):
        # self.annotation_path = self.annotation_path_lineEdit.text()
        # self.images_path = self.image_path_lineEdit.text()

        self.image_begin = try_int(self.image_begin_lineEdit.text())
        self.image_end = try_int(self.image_end_lineEdit.text())

        self.coco_helper = CocoHelper(annotation_file=self.annotation_path, images_path=self.images_path)

        self.images = self.coco_helper.load_coco_images_list(image_begin_index=self.image_begin,
                                                             image_end_index=self.image_end)[:101]

        # set image information
        self.total_image_count_label.setText(str(len(self.images)))

        for image in self.images:
            if os.path.isfile(image['image_path']):
                img_name = os.path.basename(image['image_path'])
                item = QListWidgetItem(QIcon(image['image_path']), img_name)
                self.images_listWidget.addItem(item)

    def image_show(self):

        # get user's current selected image
        current_image_index = self.images_listWidget.currentIndex().row()

        # set image information
        self.current_image_index_label.setText(str(current_image_index + 1))
        # load image
        if self.bbox_checkBox.isChecked():
            main_image = self.coco_helper.image_bbox_pillow(image_id=self.images[current_image_index]['image_id'])
        elif self.keypoint__checkBox.isChecked():
            main_image = self.coco_helper.image_keypoint_pillow(image_id=self.images[current_image_index]['image_id'])
        else:
            main_image = self.coco_helper.image_pillow(image_id=self.images[current_image_index]['image_id'])
        # convert to pixmap
        qt_image = ImageQt(main_image).copy()
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        # draw pixmap to ui
        self.main_show_image_label.setPixmap(pixmap)

    def select_annotation_path(self):
        self.annotation_path = \
            QtWidgets.QFileDialog.getOpenFileName(self, "选取annotation文件", '.', 'annotation  file(*.json)')[0]
        self.annotation_path_lineEdit.setText(self.annotation_path)

    def select_image_path(self):
        self.images_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取存放图片的文件夹")
        self.image_path_lineEdit.setText(self.images_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec())
