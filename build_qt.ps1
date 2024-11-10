$PSDefaultParameterValues['Out-File:Encoding'] = 'ascii'

pyside6-uic --from-imports qt\mainwindow.ui > gssex\uibase\mainwindow.py
pyside6-rcc qt\resource.qrc -o gssex\resource_rc.py