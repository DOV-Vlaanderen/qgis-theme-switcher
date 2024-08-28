from qgis.PyQt import QtWidgets, QtGui, QtCore

from .translate import Translatable


class ThemeSwitchAction(Translatable):
    def __init__(self, main):
        self.main = main

        self.main.themeConfig.configChanged.connect(self.populate)

    def run(self):
        self.main.dialog.show()
        self.main.dialog.exec_()

    def populate(self):
        self.setEnabled(
            len(self.main.themeConfig.themes) > 0
        )

class ToolbarButton(ThemeSwitchAction, QtWidgets.QToolButton):
    def __init__(self, main, parent=None):
        ThemeSwitchAction.__init__(self, main)
        QtWidgets.QToolButton.__init__(self, parent)

        self.main = main
        self.iconPath = ':/plugins/theme_switcher/map.png'

        self.setIcon(QtGui.QIcon(self.iconPath))
        self.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.clicked.connect(self.run)

        self.populate()

    def populate(self):
        super().populate()

        if self.main.themeConfig.currentTheme is not None:
            self.setText(self.main.themeConfig.currentTheme)
        else:
            self.setText(self.tr('Choose theme'))

        if not self.isEnabled():
            self.setToolTip(
                self.tr('No map themes found in project, add a theme first.'))
        else:
            self.setToolTip('')
