@echo off
:a
color 2
echo 1 5 9 8 6 3 4 7 8 5 
ping localhost -n 1> nul
echo 7 8 6 3 4 9 8 5 7 4
echo 4 8 6 3 7 8 9 6 3 2
ping localhost -n 1> nul
echo 9 6 3 8 5 2 7 4 4 1
ping localhost -n 1> nul
echo 7 5 3 9 5 1 8 5 2 3
ping localhost -n 1> nul
echo 3 5 7 9 5 1 2 5 8 4
goto a