$PSDefaultParameterValues['Out-File:Encoding'] = 'ascii'

pyside6-rcc qt\resource.qrc -o gssex\uibase\resource_rc.py
pyside6-uic --from-imports qt\mainwindow.ui > gssex\uibase\mainwindow.py
pyside6-uic --from-imports qt\tabpalette.ui > gssex\uibase\tabpalette.py
