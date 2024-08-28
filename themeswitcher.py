# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThemeSwitcher
                                 A QGIS plugin
 This plugin adds a popup to easily switch between layer themes
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-07-23
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Roel Huybrechts
        email                : roel@huybrechts.re
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .theme_switcher.config import ThemeConfig
from .theme_switcher.dialog import ThemeSwitcherDialog
from .theme_switcher.toolbar import ThemeSwitcherToolbar
from .theme_switcher.translate import Translatable
import os.path


class ThemeSwitcher(Translatable):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Initialise the plugin.

        Setup the translation and create the ThemeConfig instance.

        Parameters
        ----------
        iface : QGisInterface
            Link to the main QGIS interface.
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ThemeSwitcher_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Theme Switcher')

        self.toolbar = None
        self.themeConfig = ThemeConfig(self)

    def initGui(self):
        """Create the dialog and the toolbar."""
        self.dialog = ThemeSwitcherDialog(self)
        self.toolbar = self.iface.addToolBar(self.tr('Theme switcher'))
        ThemeSwitcherToolbar(self.toolbar, self)

    def unload(self):
        """Called when disabling the plugin or exiting QGIS.

        Remove the toolbar and close the dialog.
        """
        self.toolbar.parentWidget().removeToolBar(self.toolbar)
        self.dialog.close()
