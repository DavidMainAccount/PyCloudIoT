pip install adafruit-ampy

#Upload files
Write-Host 'Puting Files : #                                       (0%)\r'
ampy.exe --port COM4 put ../../src/Libraries
Write-Host 'Puting Files : ##################                     (50%)\r'
ampy.exe --port COM4 put ../../src/Scripts
Write-Host 'Puting Files : ##############################         (80%)\r'
ampy.exe --port COM4 put ../../src/Results
Write-Host 'Puting Files : ##################################     (90%)\r'
ampy.exe --port COM4 put ../../src/main.py
Write-Host 'Puting Files : ######################################(100%)\r'
ampy.exe --port COM4 reset
