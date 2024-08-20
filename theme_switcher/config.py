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

        self.mapThemeCollection.mapThemesChanged.connect(self.load)
        self.layerTreeRoot.visibilityChanged.connect(self.load)

    def load(self):
        self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
        self.layerTreeModel = self.main.iface.layerTreeView().layerTreeModel()
        self.mapThemeCollection = QgsProject.instance().mapThemeCollection()
        self.themes = sorted(self.mapThemeCollection.mapThemes())
        self.currentTheme = self._loadCurrentTheme()

        self.configChanged.emit()

    def _loadCurrentTheme(self):
        currentState = self.mapThemeCollection.createThemeFromCurrentState(
            self.layerTreeRoot, self.layerTreeModel)

        for theme in self.themes:
            if self.mapThemeCollection.mapThemeState(theme) == currentState:
                return theme
