from qgis.core import QgsProject
from qgis.PyQt import QtCore

from .translate import Translatable


class ThemeConfig(QtCore.QObject, Translatable):
    configChanged = QtCore.pyqtSignal()

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.GROUP_OTHER_NAME = self.tr('Other')

        self.load()

        QgsProject.instance().cleared.connect(self.load)
        QgsProject.instance().readProject.connect(self.load)

    def load(self):
        self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
        self.layerTreeModel = self.main.iface.layerTreeView().layerTreeModel()
        self.mapThemeCollection = QgsProject.instance().mapThemeCollection()

        self.mapThemeCollection.mapThemesChanged.connect(self.loadThemes)
        self.layerTreeRoot.visibilityChanged.connect(self.loadThemes)

        self.loadThemes()

    def loadThemes(self):
        self.themes = sorted(self.mapThemeCollection.mapThemes())
        self.themeGroups = self._parseGroups()
        self.currentTheme = self._loadCurrentTheme()
        self.configChanged.emit()

    def _parseGroupNameThemeName(self, theme):
        groupNameSeparator = ':'

        if groupNameSeparator in theme:
            groupName = theme[:theme.find(groupNameSeparator)].strip()
            themeName = theme[theme.find(groupNameSeparator) + 1:].strip()
            return groupName, themeName
        else:
            return None, theme

    def _parseGroups(self):
        groups = {self.GROUP_OTHER_NAME: []}

        for theme in self.themes:
            groupName, themeName = self._parseGroupNameThemeName(theme)

            if groupName is not None:
                if groupName not in groups:
                    groups[groupName] = []

                groups[groupName].append((themeName, theme))
            else:
                groups[self.GROUP_OTHER_NAME].append((theme, theme))

        if len(groups[self.GROUP_OTHER_NAME]) == 0:
            del (groups[self.GROUP_OTHER_NAME])

        return groups

    def _loadCurrentTheme(self):
        currentState = self.mapThemeCollection.createThemeFromCurrentState(
            self.layerTreeRoot, self.layerTreeModel)

        for theme in self.themes:
            if self.mapThemeCollection.mapThemeState(theme) == currentState:
                return theme
