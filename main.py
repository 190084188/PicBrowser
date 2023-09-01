# 开发第一个基于PyQt5的桌面应用

import sys
import DEMO

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

def show_PicBrowser():
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建对象
    mainWindow = QMainWindow()

    # 创建ui，引用demo1文件中的Ui_MainWindow类
    ui = DEMO.Ui_MainWindow()
    # 调用Ui_MainWindow类的setupUi，创建初始组件
    ui.setupUi(mainWindow)
    # 创建窗口
    mainWindow.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())

if __name__ == '__main__':
    show_PicBrowser()

