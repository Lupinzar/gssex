$PSDefaultParameterValues['Out-File:Encoding'] = 'ascii'

pyside6-rcc qt\resource.qrc -o resource_rc.py
pyside6-uic qt\mainwindow.ui -o gssex\uibase\mainwindow.py
pyside6-uic qt\tabpalette.ui -o gssex\uibase\tabpalette.py
pyside6-uic qt\tabvram.ui -o gssex\uibase\tabvram.py
pyside6-uic qt\tabraw.ui -o gssex\uibase\tabraw.py
pyside6-uic qt\tabtilemap.ui -o gssex\uibase\tabtilemap.py
pyside6-uic qt\tabsprite.ui -o gssex\uibase\tabsprite.py
