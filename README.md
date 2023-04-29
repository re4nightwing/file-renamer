# File-Renamer

This a simple desktop application created using __[flaskwebgui](https://github.com/ClimenteA/flaskwebgui)__ module. As the name suggests it has the ability to rename files of a directory according to a given rename pattern.

## Install

__Option 01__
- Download the latest [release](https://github.com/re4nightwing/file-renamer/releases/) and extract and use the application as a portable application.

__Option 02__
1. Clone the repository,
2. Create a virtualenv and install the required dependencies.
3. Run using `python3 main.py`

## Build
- _First, complete the steps of Install>Option 02._
- Install pyvan on your venv and run `pyvan main.py -nc --icon .\static\file_icon.ico`

## Features

- [x] Scan a directory for files.
- [x] Custom directory browsing system using js. (Since the application is a web application, it does not have access to path of a file)
- [x] Make files are sortable using drag 'n drop.
- [x] Add a remove button for each file to avoid specific files from renaming.
- [x] Add rename pattern. (Ex: `Horimiya <ep>` => `Horimiya 01`, `Horimiya 02`, etc)
- [ ] More customization over rename pattern. (Starting number (\<ep:02>) and make that work with multiple variables. (\<ep:02> of \<series:15>))
- [x] Make browser menu directory list collapsible.
- [x] Create a custom right-click context menu.
- [ ] Create counter measures for browser specific things like f5,f1 keys.
- [ ] Add themes. (dark, light, dracula, nord) 
- [x] Check for updates on the start up.
- [x] Add notification toasts.


__Submit any questions/issues you have! Feel free to fork it and improve it!__ 