# Parser for finding all emails address on web page with command-line interface

[![Python version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)

# Installation
```
git clone https://github.com/lerdem/parser_email.git
```
# Example
make file executable
```
chmod +x parser_email.py
```
for start parsing url run
```
./parser_email.py http://example.com
```
for start parsing current url and all urls on that page set --deep value to 2
```
./parser_email.py --deep 2 http://example.com
```
param --deep means deeping of your search at that url, default value 1.
# Uninstallation
For running project
```
rm -r parser_email/
```
