from qgis.PyQt.QtCore import QCoreApplication


class Translatable:
    def tr(self, message):
        return QCoreApplication.translate(self.__class__.__name__, message)
