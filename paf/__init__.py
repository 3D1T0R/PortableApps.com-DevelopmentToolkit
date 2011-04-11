# -*- coding: utf-8 -*-

FORMAT_VERSION = '2.0'

CATEGORIES = ('Accessibility', 'Development', 'Education', 'Games',
        'Graphics & Pictures', 'Internet', 'Music & Video', 'Office',
        'Security', 'Utilities')

LANGUAGES = ('Multilingual', 'Afrikaans', 'Albanian', 'Arabic', 'Armenian',
        'Basque', 'Belarusian', 'Bosnian', 'Breton', 'Bulgarian', 'Catalan',
        'Cibemba', 'Croatian', 'Czech', 'Danish', 'Dutch', 'Efik', 'English',
        'Estonian', 'Farsi', 'Finnish', 'French', 'Galician', 'Georgian',
        'German', 'Greek', 'Hebrew', 'Hungarian', 'Icelandic', 'Igbo',
        'Indonesian', 'Irish', 'Italian', 'Japanese', 'Khmer', 'Korean',
        'Kurdish', 'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian',
        'Malagasy', 'Malay', 'Mongolian', 'Norwegian', 'NorwegianNynorsk',
        'Pashto', 'Polish', 'Portuguese', 'PortugueseBR', 'Romanian',
        'Russian', 'Serbian', 'SerbianLatin', 'SimpChinese', 'Slovak',
        'Slovenian', 'Spanish', 'SpanishInternational', 'Swahili', 'Swedish',
        'Thai', 'TradChinese', 'Turkish', 'Ukranian', 'Uzbek', 'Valencian',
        'Vietnamese', 'Welsh', 'Yoruba')


class PAFException(Exception):
    pass

from paf.package import *
from paf.appinfo import *
from paf.installer import *
from paf.launcher import *
