#!C:\Github\ebinezerApi\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyinstaller==5.13.0','console_scripts','pyi-bindepend'
__requires__ = 'pyinstaller==5.13.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyinstaller==5.13.0', 'console_scripts', 'pyi-bindepend')()
    )
