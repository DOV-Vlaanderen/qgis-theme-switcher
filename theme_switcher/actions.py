from qgis.PyQt import QtWidgets, QtGui, QtCore


class ThemeSwitchAction:
    def __init__(self, main):
        self.main = main

        self.main.themeConfig.configChanged.connect(self.populateEnabled)

    def run(self):
        self.main.dialog.show()
        self.main.dialog.exec_()

    def populateEnabled(self):
        self.setEnabled(
            len(self.main.themeConfig.themes) > 0
        )


class ToolbarButton(ThemeSwitchAction, QtWidgets.QToolButton):
    def __init__(self, main, parent=None):
        ThemeSwitchAction.__init__(self, main)
        QtWidgets.QToolButton.__init__(self, parent)

        self.main = main
        self.iconPath = ':/plugins/theme_switcher/map.png'

        self.setText('Choose theme')
        self.setIcon(QtGui.QIcon(self.iconPath))
        self.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.clicked.connect(self.run)
