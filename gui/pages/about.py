from ._base import WindowPage
from ..ui.pageabout import Ui_PageAbout
from utils import _
from config import padt_version_info


class PageAbout(WindowPage, Ui_PageAbout):
    def __init__(self, *args, **kwargs):
        super(PageAbout, self).__init__(*args, **kwargs)
        self.about_version.setText(_('Version %s') % padt_version_info)
