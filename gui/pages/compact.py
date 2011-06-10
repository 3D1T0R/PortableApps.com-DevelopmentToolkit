from ._base import WindowPage
from ..ui.pagecompact import Ui_PageCompact
from paf import AppCompactor
from PyQt4.QtCore import Slot


class PageCompact(WindowPage, Ui_PageCompact):
    def enter(self):
        self.appcompactor = AppCompactor(self.window.package)
        self.appcompactor.load()
        self.files_excluded.setText('|'.join(self.appcompactor.files_excluded))
        self.additional_extensions_included.setText('|'.join(self.appcompactor.additional_extensions_included))
        self.additional_extensions_excluded.setText('|'.join(self.appcompactor.additional_extensions_excluded))
        self.compression_file_size_cut_off.setValue(self.appcompactor.compression_file_size_cut_off)

    def leave(self, closing=True):
        self.save()

    @Slot()
    def on_start_button_clicked(self):
        if self.window.page_options.find_appcompactor_path():
            self.save()  # Necessary while running an external process
            self.appcompactor.compact(block=False)
        # If not, the user was told about it in find_appcompactor_path

    def save(self):
        self.appcompactor.files_excluded = self.files_excluded.text().split('|')
        if self.appcompactor.files_excluded == ['']:
            del self.appcompactor.files_excluded[0]

        self.appcompactor.additional_extensions_included = self.additional_extensions_included.text().split('|')
        if self.appcompactor.additional_extensions_included == ['']:
            del self.appcompactor.additional_extensions_included[0]

        self.appcompactor.additional_extensions_excluded = self.additional_extensions_excluded.text().split('|')
        if self.appcompactor.additional_extensions_excluded == ['']:
            del self.appcompactor.additional_extensions_excluded[0]

        self.appcompactor.compression_file_size_cut_off = self.compression_file_size_cut_off.value()

        self.appcompactor.save()
