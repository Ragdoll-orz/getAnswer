import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QCheckBox, QLineEdit, QLabel, QPushButton, \
    QHBoxLayout


class MainWindow(QWidget):
    titles = ['第一', '第二', '第三', '第四', '第五', '第六', '第七', '第八', '第九']
    levels = ['1-7', '7-24', '24-55', '55-63', '63-70', '70-75', '75-81', '81-98', '98-111']
    result = []
    flag = True

    def __init__(self):
        super().__init__()
        self.tip = None
        self.layouts = None
        self.pwd = None
        self.button = None
        self.name = None
        self.checkBoxes = None
        self.comboBox = None
        self.layout = None
        self.ui()

    def ui(self):
        self.setWindowTitle('这是窗口名')
        self.setGeometry(800, 400, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name = QLabel('Enter 账号:')
        self.name.setFixedSize(100, 40)
        self.layout.addWidget(self.name)
        self.name = QLineEdit()
        self.layout.addWidget(self.name)

        self.pwd = QLabel('Enter 密码:')
        self.pwd.setFixedSize(100, 40)
        self.layout.addWidget(self.pwd)
        self.pwd = QLineEdit()
        self.layout.addWidget(self.pwd)

        self.comboBox = QComboBox()  # 下拉框
        for title in self.titles:
            self.comboBox.addItem(title)
        self.comboBox.currentIndexChanged.connect(self.update_combobox)
        self.layout.addWidget(self.comboBox)

        self.checkBoxes = []

        for i in range(int(self.levels[0].split('-')[1])):
            checkbox = QCheckBox(f"Level {i + 1}")
            self.checkBoxes.append(checkbox)
            self.layout.addWidget(checkbox)

        self.button = QPushButton('提交')
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.submit)

        self.name.setText('账号')
        self.pwd.setText('密码')

        self.show()

    def submit(self):
        # print(self.comboBox.currentIndex())
        if not self.name.text():
            self.name.setPlaceholderText('输入账号')
            self.create_submit('输入账号')
            self.result.clear()
            return
        if not self.pwd.text():
            self.pwd.setPlaceholderText('输入密码')
            self.create_submit('输入密码')
            self.result.clear()
            return
        rs = self.get_selected()
        if not rs:
            self.create_submit('勾选levels')
            self.result.clear()
            return
        if self.flag:
            self.result.append(self.name.text())
            self.result.append(self.pwd.text())
            self.result.append(rs)
            self.create_submit('提交成功\n请等待拉启浏览器窗口\n当前窗口将进入未响应状态,不要关闭!')
            self.flag = False
            import get
            get.GetAnswer(self.name.text(), self.pwd.text(), self.comboBox.currentIndex()+1, rs)
            self.layout.addWidget(QLabel('答题结束'))
            end = QPushButton('退出')
            self.layout.addWidget(end)
            end.clicked.connect(self.app_exit)
        print(self.result)

    @staticmethod
    def app_exit():
        app.quit()

    def get_selected(self):
        temp = []
        for checkbox in self.checkBoxes:
            if checkbox.isChecked():
                temp.append(self.checkBoxes.index(checkbox)+1)
        return temp

    def update_combobox(self):
        # 移除存在的checkbox
        for checkbox in self.checkBoxes:
            checkbox.setParent(None)
        self.button.setParent(None)

        self.checkBoxes = []

        num_str = self.levels[self.comboBox.currentIndex()].split('-')
        num_start = int(num_str[0])
        num_end = int(num_str[1])
        flag = False
        # 创建水平布局用于左列和右列的控件
        horizontal_layout = QHBoxLayout()
        for i in range(4):
            # 创建左列的垂直布局
            left_layout = QVBoxLayout()
            for j in range(8):
                checkbox = QCheckBox(f"Level {num_start}")
                self.checkBoxes.append(checkbox)
                left_layout.addWidget(checkbox)
                num_start += 1
                if num_start == num_end:
                    flag = True
                    break
            horizontal_layout.addLayout(left_layout)
            if flag:
                break
        self.layout.addLayout(horizontal_layout)

        self.create_submit()

    def create_submit(self, text=None):
        if text is not None:
            if self.tip:
                self.tip.setText(text)
            else:
                self.tip = QLabel(text)
                self.layout.addWidget(self.tip)
        self.button.setParent(None)

        self.button = QPushButton('提交')
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.submit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

