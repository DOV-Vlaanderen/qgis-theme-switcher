from qgis.core import QgsProject


from qgis.PyQt import QtCore


class ThemeConfig(QtCore.QObject):
    configChanged = QtCore.pyqtSignal()

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.load()

        QgsProject.instance().cleared.connect(self.load)
        QgsProject.instance().readProject.connect(self.load)

    def load(self):
        self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
        self.layerTreeModel = self.main.iface.layerTreeView().layerTreeModel()
        self.mapThemeCollection = QgsProject.instance().mapThemeCollection()
        self.mapThemeCollection.mapThemesChanged.connect(self.load)
        self.themes = sorted(self.mapThemeCollection.mapThemes())

        self.configChanged.emit()
