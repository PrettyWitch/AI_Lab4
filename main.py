from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QCheckBox
from PySide2.QtGui import QStandardItemModel, QStandardItem
import xlrd as xlrd
import utils


class Search:
    def __init__(self):
        # Load UI definition from file
        qfile_stats = QFile('search2.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.ui = QUiLoader().load(qfile_stats)
        self.model = QStandardItemModel(4, 10)
        self.model.setHorizontalHeaderLabels(['name', 'id', 'Import', 'weight', 'price',
                                              'discount', 'shelfLife', 'sweetness', 'hardness', 'food'])
        self.ui.button1.clicked.connect(self.search)
        self.ui.button2.clicked.connect(self.add_sub)
        self.model2 = QStandardItemModel()

        date = self.readData()
        values = date[0]
        nrows = date[1]
        ncols = date[2]

        for column in range(ncols - 3):
            self.ui.tableView.setColumnWidth(column, 60)

        self.ui.tableView.setModel(self.model)
        self.ui.listView.setModel(self.model2)

        dictImport = {0: 'false', 1: 'ture'}
        dictSweetness = {0: 'VerySweet', 1: 'GenerallySweet', 2: 'SweetAndSour', 3: 'Acid'}
        # 初始化price
        self.ui.comboBox.addItem(' ')
        for k, v in dictImport.items():
            self.ui.comboBox.addItem(v, k)
        # 初始化sweetness
        self.ui.comboBox_2.addItem(' ')
        for k, v in dictSweetness.items():
            self.ui.comboBox_2.addItem(v, k)

    def readData(self):
        # Read table data
        book = xlrd.open_workbook('fruit.xlsx')
        sheet1 = book.sheets()[0]
        nrows = sheet1.nrows
        ncols = sheet1.ncols
        values = []
        for row in range(nrows):
            row_values = sheet1.row_values(row)
            values.append(row_values)
        return values, nrows, ncols

    def search(self):
        global history
        data = self.readData()
        nrows = data[1]
        values = data[0]
        ncols = data[2]

        # 获取搜索值
        # name = self.ui.lineEdit.text()
        price = int(self.ui.lineEdit_3.text())
        import_index = self.ui.comboBox.currentIndex()
        sweet_index = self.ui.comboBox_2.currentIndex()
        import_name = self.ui.comboBox.itemText(import_index)
        sweet_name = self.ui.comboBox_2.itemText(sweet_index)
        search_input = [import_name, price, sweet_name]
        print(search_input)
        #     # Use dictionary to store line number and distance information
        dict = {}
        for row in range(1, nrows):
            c = utils.tra3(search_input, values[row])
            d = utils.tra4(values[row])
            name2 = values[row][1]
            row_num = values[row][0]
            # print(c, d, name2)
            distance = utils.Euclidean(c, d)
            dict[row_num] = distance
            # print(f"{name2} distance = {distance}")
            # print(dict)
        # Dictionary sort
        newDis = sorted(dict.items(), key=lambda d: d[1])
        print(newDis)
        print(newDis[0], newDis[1], newDis[2])
        index = {}
        for i in range(0, 6):
            index[i] = int(newDis[i][0])
        for row in range(len(index)):
            for col in range(1, ncols):
                item = QStandardItem('%s' % values[index[row]][col])
                self.model.setItem(row, col - 1, item)
                self.ui.tableView.resizeRowsToContents()
        return index


    def add_sub(self):
        data = self.readData()
        nrows = data[1]
        values = data[0]
        ncols = data[2]
        index = self.search()
        for row in range(len(index)):
            item = QStandardItem('%s' % values[index[row]][1])
            self.model2.setItem(row, item)

app = QApplication([])
search = Search()
search.ui.show()
app.exec_()