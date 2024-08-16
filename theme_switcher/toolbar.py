from .actions import ToolbarButton


class ThemeSwitcherToolbar:
    def __init__(self, toolbar, main):
        self.toolbar = toolbar
        self.main = main

        self.toolbar.addWidget(ToolbarButton(self.main, self.toolbar))
