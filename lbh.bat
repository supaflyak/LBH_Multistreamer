echo on
net use /delete X:
net use X: \\10.0.0.8\projects\temp\lbh
X:
cd \codeBase
python.exe lbh.py
pause