from ._base import WindowPage
from .start import PageStart
from .details import PageDetails
from .launcher import PageLauncher
from .compact import PageCompact
from .test import PageTest
from .publish import PagePublish
from .options import PageOptions
from .about import PageAbout


__all__ = ['pages', 'WindowPage', 'PageStart', 'PageDetails', 'PageLauncher',
        'PageCompact', 'PageTest', 'PagePublish', 'PageOptions', 'PageAbout']

pages = dict(start=PageStart, details=PageDetails, launcher=PageLauncher,
        compact=PageCompact, test=PageTest, publish=PagePublish,
        options=PageOptions, about=PageAbout)
