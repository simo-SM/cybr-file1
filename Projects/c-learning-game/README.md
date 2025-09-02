C Learning Game (CLG)
=====================

CLG is a terminal-based learning game for C programming that runs offline.
It includes:
- Learn: short topic pages
- Quizzes: multiple-choice questions from JSON
- Code Challenges: small C exercises with an auto-grader using MinGW GCC
- Progress: local save file in JSON
- Settings: choose a workspace directory

Build
-----
Prereqs:
- MinGW-w64 GCC at C:\\MinGW\\bin
- Visual Studio Community cmake.exe (or cmake in PATH)
- PowerShell 5.1 on Windows

Commands:
  set CC and CXX to C:\\MinGW\\bin\\gcc.exe and g++.exe
  cmake -G "MinGW Makefiles" -S . -B build -DCMAKE_BUILD_TYPE=Release
  cmake --build build --config Release -j

Run
---
The compiled executable is build\\clg.exe during development.
After packaging, use dist\\clg.exe or the installed C:\\Users\\Administrator\\c-learning-game\\clg.exe

License
-------
MIT. See LICENSE.

