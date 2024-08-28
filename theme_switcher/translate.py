from qgis.PyQt.QtCore import QCoreApplication


class Translatable:
    """Class to add i18n capabilities.

    Subclass this class to be able to use the tr() method to translate strings. This way the caller's class
    will be correctly used as context, both while generating the translation files as well as finding the translation
    context at runtime.
    """
    def tr(self, message):
        """Translate the given message based on the installed locale.

        Uses the context based on the classname of the caller, similar to the behaviour of pylupdate5 when
        generating the .ts files.

        Parameters
        ----------
        message : str
            Message to translate.

        Returns
        -------
        str
            Translated message.
        """
        return QCoreApplication.translate(self.__class__.__name__, message)
