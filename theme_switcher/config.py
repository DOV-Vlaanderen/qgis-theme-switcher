from qgis.core import QgsProject
from qgis.PyQt import QtCore

from .translate import Translatable


class ThemeConfig(QtCore.QObject, Translatable):
    """Class to centralise all information regarding themes."""
    configChanged = QtCore.pyqtSignal()

    def __init__(self, main):
        """Initialise the theme configuration.

        Load current themes and connect signals to reload when changing project.

        Parameters
        ----------
        main : ThemeSwitcher
            Reference to main plugin instance.
        """
        super().__init__()

        self.main = main
        self.GROUP_OTHER_NAME = self.tr('Other')

        self.load()

        QgsProject.instance().cleared.connect(self.load)
        QgsProject.instance().readProject.connect(self.load)

    def load(self):
        """Connect project specific signals and load current themes."""
        self.layerTreeRoot = QgsProject.instance().layerTreeRoot()
        self.layerTreeModel = self.main.iface.layerTreeView().layerTreeModel()
        self.mapThemeCollection = QgsProject.instance().mapThemeCollection()

        self.mapThemeCollection.mapThemesChanged.connect(self.loadThemes)
        self.layerTreeRoot.visibilityChanged.connect(self.loadThemes)

        self.loadThemes()

    def loadThemes(self):
        """Load themes, theme groups and emit signal that config is updated."""
        self.themes = sorted(self.mapThemeCollection.mapThemes())
        self.themeGroups = self._parseGroups()
        self.currentTheme = self._loadCurrentTheme()
        self.configChanged.emit()

    def _parseGroupNameThemeName(self, theme):
        """Split the QGIS theme name into group name and theme name.

        If the QGIS theme name contains a ':', split the first part into the groupname and the other part
        into the themename.

        Parameters
        ----------
        theme : str
            QGIS theme name

        Returns
        -------
        groupName, themeName
            Group name (or None when no group found) and theme name
        """
        groupNameSeparator = ':'

        if groupNameSeparator in theme:
            groupName = theme[:theme.find(groupNameSeparator)].strip()
            themeName = theme[theme.find(groupNameSeparator) + 1:].strip()
            return groupName, themeName
        else:
            return None, theme

    def _parseGroups(self):
        """Parse all QGIS themes into theme groups.

        Returns
        -------
        dict(str, list((str, str)))
            Mapping with group names as keys, and a list of tuples with (theme name, QGIS theme name)
        """
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
        """Find the currently active theme, or None when no theme is active.

        Returns
        -------
        str or None
            QGIS theme name
        """
        currentState = self.mapThemeCollection.createThemeFromCurrentState(
            self.layerTreeRoot, self.layerTreeModel)

        for theme in self.themes:
            if self.mapThemeCollection.mapThemeState(theme) == currentState:
                return theme
