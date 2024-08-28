from .actions import ToolbarButton


class ThemeSwitcherToolbar:
    def __init__(self, toolbar, main):
        """Initialise the toolbar.

        Add the ToolbarButton to the toolbar.

        Parameters
        ----------
        toolbar : QToolBar
            Reference to toolbar.
        main : ThemeSwitcher
            Reference to main ThemeSwitcher instance.
        """
        self.toolbar = toolbar
        self.main = main

        self.toolbar.addWidget(ToolbarButton(self.main, self.toolbar))
