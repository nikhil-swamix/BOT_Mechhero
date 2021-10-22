cd %~dp0
set PROGTITLE='Mechhero Super BOT'
start powershell -noexit "$host.UI.RawUI.WindowTitle = %PROGTITLE%; for ($x=0;$x -lt 1;$x+=1) {python main.py} " >> console.log
