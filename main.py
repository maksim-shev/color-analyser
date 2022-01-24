import sys
import threading
import time
import cv2
import photoMaker
import color_analyzer
import banana_finder
import visualization
import configurator
import glob
from cutting import createSpecial
from core_color import coreColor
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QFileDialog, QMenu, \
    QLineEdit, QLabel, QVBoxLayout, QPushButton, QWidget, QTextEdit, QCheckBox, QHBoxLayout, QMessageBox, \
    QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout, QComboBox
from PyQt5.QtGui import QIcon, QPixmap, QBrush
from PyQt5.Qt import Qt
from PyQt5 import QtCore
import os


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.build()

    def build(self):

        self.cuontOfColumns = int(
            configurator.get_setting(path, 'core', 'count'))
        self.currentCuontOfColumns = 0

        grid = QGridLayout()
        a = QVBoxLayout()
        grid.blockSignals(True)
        grid.addWidget(self.createGroupStand(), 0, 0, -1, 1)
        grid.addWidget(self.createScanGroup(), 0, 1, 1, 1)
        grid.addWidget(self.createTableGroup(), 1, 1, 1, 1)
        grid.blockSignals(False)
        self.setLayout(grid)

        # размер формы
        self.setGeometry(350, 50, 785, 430)
        self.setWindowTitle('Налаштування')

    def createScanGroup(self):
        groupBox = QGroupBox("Фотореєстрація")
        # кнопки
        btn1 = QPushButton("Зареєструвати підставку", self)
        btn1.setGeometry(20, 60, 130, 30)
        btn1.clicked.connect(self.createStand("stands\\"))

        btn2 = QPushButton("Зареєструвати еталон", self)
        btn2.setGeometry(20, 60, 130, 30)
        btn2.clicked.connect(self.createStand("reference\\"))

        btn3 = QPushButton("Зареєструвати особливі області", self)
        btn3.setGeometry(20, 60, 130, 30)
        btn3.clicked.connect(self.special)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createGroupStand(self):
        groupBox = QGroupBox("Налаштування підставки")

        # кнопки
        btn2 = QPushButton("Обрати підставку", self)
        btn2.clicked.connect(self.changeStand)

        # изображение подставки
        self.label = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(btn2)
        vbox.addWidget(self.label)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox
    # функция для теста

    def createTableGroup(self):
        groupBox = QGroupBox("Список обраних еталонів")

        btn4 = QPushButton("Видалити", self)
        btn4.setGeometry(300, 60, 130, 30)
        btn4.clicked.connect(self.deleteRow)

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.setGeometry(340, 120, 600, 300)
        self.table.setColumnCount(4)     # Устанавливаем три колонки
        self.table.setRowCount(5)        # и одну строку в таблице

        self.table.cellChanged.connect(self.setData)
        self.table.setHorizontalHeaderLabels(
            ["Колір", "Lab уявлення", "                  Назва ознаки                    ", "Дельта Е"])

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем таблицу
        if(self.cuontOfColumns == 0):
            self.table.blockSignals(True)
            self.table.setItem(0, 0, QTableWidgetItem(""))
            self.table.blockSignals(False)
        else:
            for i in range(1, self.cuontOfColumns):
                names = configurator.get_setting(path, "core", "names")
                nameofsection = names.split(",")[i]
                imagePath = 'special\\'+nameofsection
                lab = configurator.get_setting(path, nameofsection, 'lab')
                name = configurator.get_setting(path, nameofsection, 'name')
                delta = configurator.get_setting(path, nameofsection, 'delta')
                self.addReference(imagePath, lab, name, delta)

        # кнопка поверх таблицы
        btn3 = QPushButton("Додати", self)
        btn3.setGeometry(340, 390, 130, 30)
        btn3.clicked.connect(self.createReference)

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addWidget(btn4)
        vbox.addWidget(btn3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def special(self):
        createSpecial()

    def createStand(self, path):
        def calluser():
            QMessageBox.warning(
                self, 'Увага!', "Створіть необхідні умови для фотореєстрації та натисніть \"ОК\"")
            photoMaker.photo(path)
        return calluser

    # выбор подставки
    def changeStand(self):
        image = QFileDialog.getOpenFileName(
            None, 'Обрати підставку', 'stands', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        pixmap1 = pixmap.scaled(300, 300)
        self.label.setPixmap(pixmap1)
        configurator.update_setting(
            path, 'core', 'stand', str(coreColor(imagePath)))

    def createReference(self):
        image = QFileDialog.getOpenFileName(
            None, 'OpenFile', 'special', "Image file(*.jpg)")
        imagePath = image[0]
        if imagePath == '':
            return
        lab = coreColor(imagePath)
        imageName = imagePath.split("/")[-1]
        configurator.update_setting(
            path, "core", "names", configurator.get_setting(path, "core", "names")+","+str(imageName))
        configurator.update_setting(
            path, imageName, "color", imagePath)
        configurator.update_setting(
            path, imageName, "lab", lab)
        configurator.update_setting(
            path, imageName, "name", "                         ")
        configurator.update_setting(path, imageName, "delta", "20")
        self.addReference(imagePath, lab, "Введіть назву", "20")
        self.cuontOfColumns += 1
        configurator.update_setting(
            path, 'core', 'count', str(self.cuontOfColumns))

    def addReference(self, imagePath, lab, name, delta):
        if(self.cuontOfColumns == 8):
            return
        else:
            qb = QBrush(QPixmap(imagePath))
            self.table.setItem(self.currentCuontOfColumns,
                               0, QTableWidgetItem(""))
            self.table.item(self.currentCuontOfColumns, 0).setBackground(qb)
            self.table.setItem(self.currentCuontOfColumns, 1,
                               QTableWidgetItem(lab))
            self.table.setItem(self.currentCuontOfColumns, 2,
                               QTableWidgetItem(name))
            self.table.setItem(self.currentCuontOfColumns, 3,
                               QTableWidgetItem(delta))
            self.currentCuontOfColumns += 1

    def setData(self):
        curCol = self.table.currentColumn()
        if(curCol == 3 or curCol == 2):
            value = self.table.item(self.table.currentRow(),
                                    curCol).text()
            names = configurator.get_setting(path, "core", "names")
            names = configurator.get_setting(path, "core", "names")
            nameofsection = names.split(",")[self.table.currentRow()+1]
            if(curCol == 2):
                configurator.update_setting(path, nameofsection, 'name', value)
            if(curCol == 3):
                configurator.update_setting(
                    path, nameofsection, 'delta', value)
        else:
            return

    def deleteRow(self):
        if(self.cuontOfColumns == 0):
            return
        for i in range(5):
            self.table.setItem(self.currentCuontOfColumns -
                               1, i, QTableWidgetItem(""))
        names = configurator.get_setting(path, "core", "names")
        nameofsection = names.split(",")[self.currentCuontOfColumns]
        newnames = names.replace(","+nameofsection, "")
        configurator.update_setting(path, "core", "names", newnames)
        configurator.delete_setting(path, nameofsection)
        self.currentCuontOfColumns -= 1
        self.cuontOfColumns -= 1
        configurator.update_setting(
            path, 'core', 'count', str(self.cuontOfColumns))


class Example(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.secondWin = None
        self.initUI()

    def initUI(self):

        self.result_mass = []    

        btn2 = QPushButton("Колориметричний аналіз", self)
        btn2.setGeometry(20, 180, 150, 30)
        btn2.clicked.connect(self.analyse)


        btn4 = QPushButton("Фотореєстрація", self)
        btn4.setGeometry(20, 100, 150, 30)
        btn4.clicked.connect(self.monitoring)

        btn5 = QPushButton("Візуалізація результатів", self)
        btn5.setGeometry(20, 220, 150, 30)
        btn5.clicked.connect(self.result)

        btn6 = QPushButton("Налаштування", self)
        btn6.setGeometry(20, 360, 150, 30)
        btn6.clicked.connect(self.openSecondWin)

        self.text = QTextEdit("", self)
        self.text.setGeometry(250, 0, 350, 400)

        self.statusBar()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowIcon(QIcon('icons/icon.jpg'))
        self.setWindowTitle('Система визначення колориметричних характеристик')
        self.show()

    def analyse(self):
        for img in glob.glob('src\\*.jpg'):
            strStand = configurator.get_setting(path, "core", "stand")
            stand = []
            for i in range(3):
                intStand = strStand.split(" ")[i]
                stand.append(int(intStand))
            names = configurator.get_setting(path, "core", "names")
            names_of_section = names.split(",")
            reference_mass = []
            reference_delta_mass = []
            for name in names_of_section:
                if name == '':
                    continue
                str_reference = configurator.get_setting(path, name, 'lab')
                str_delta = configurator.get_setting(path, name, 'delta')
                int_reference = []
                for i in range(3):
                    for_int_reference = str_reference.split(" ")[i]
                    int_reference.append(int(for_int_reference))
                int_delta = int(str_delta)
                reference_mass.append(int_reference)
                reference_delta_mass.append(int_delta)
            result_mass = color_analyzer.colorAnalysis(
                reference_mass, reference_delta_mass, stand, img)
            self.result_mass.append(result_mass)
            for i in range(len(result_mass)):
                title = configurator.get_setting(
                    'settings.ini', names_of_section[i+1], 'name')
                self.text.append((str(result_mass[i])+'% '+title))
            self.text.append('---------------------------')

    def monitoring(self):
        photoMaker.photo('src\\')

    def result(self):
        print(self.result_mass)
        visualization.visualization(self.result_mass)

    def openSecondWin(self):
        if not self.secondWin:
            self.secondWin = SecondWindow(self)
        self.secondWin.show()


if __name__ == '__main__':

    path = "settings.ini"
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
