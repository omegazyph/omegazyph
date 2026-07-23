Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe src/vault_GUI.pyw", 0
Set WshShell = Nothing