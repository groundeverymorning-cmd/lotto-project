<# :
@echo off
powershell -noprofile "iex (${%~f0} | out-string)"
goto :EOF
: #>

$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
$logPath = Join-Path $PSScriptRoot "lotto_result.txt"

$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"====== 시간: $now ======" | Out-File -FilePath $logPath -Encoding utf8 -Append

# Python 
$pyOut = python -c "import random; nums=sorted(random.sample(range(1, 46), 6)); print(f'오늘의 추천 로또 번호: {nums}')"
$pyOut | Out-File -FilePath $logPath -Encoding utf8 -Append

"===================================" | Out-File -FilePath $logPath -Encoding utf8 -Append

# Sound and Popup
(New-Object Media.SoundPlayer 'C:\Windows\Media\tada.wav').PlaySync()
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show('로또 번호 자동 추천이 완료되었습니다! lotto_result.txt 파일을 확인하세요.', '로또 알리미', 'OK', 'Information')
