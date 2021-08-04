set PROGTITLE='Mechhero Super BOT'
start powershell "$host.UI.RawUI.WindowTitle = %PROGTITLE%; for ($x=0;$x -lt 10;$x+=1) {python main.py}"
