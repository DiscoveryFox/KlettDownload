# LubaProject  

## Introduction

This is a project I'm currently working on for my english teacher. This project also owes its name to him. It's 
delivered with an interface which main focus was to provide ease-of-use and being expandable. To create your own 
Webscraping Book downloaders have a look [here](#coding).

## Installation

1. Make sure you have python3.11 or newer installed. If you don't have it installed you can download it from
[here](https://www.python.org/downloads/) and if you need help setting everything up I can highly recommend 
you [this](https://www.youtube.com/watch?v=YKSpANU8jPE) tutorial.
2. When you're done setup up python and everything is working you should clone this repository from GitHub using
```shell
git clone https://github.com/DiscoveryFox/KlettDownload.git
```
3. Now cd into that directory and create a new [virtual environment](https://docs.python.org/3/library/venv.html).(You theoretically can skip the virtual environment, 
but I would highly encourage you to do not since it will make managing your python in the future a lot easier, and it's just good practice)
```shell
cd KlettDownload
python -m venv .venv
```
5. Now you can install all requirements for the project:
```shell
python -m pip install -r requirements.txt
```
6. And then to start the script you can simply run:
```shell
python ui.py
```

## Usage

If you want to activate your virtual environment in the future its depending on your operating system. On Windows you type
```shell
# Windows
cd .venv/Scripts
.\activate.ps1
# Linux
source .venv/bin/activate
```



## Coding
The BookProvider class provides a common interface for accessing and downloading ebooks from various online stores. It provides a set of methods for interacting with an ebook store's API, such as getting authentication credentials, fetching book content, and downloading books.

To create your own BookProvider class, you need to create a new Python file and define a class that inherits from the BookProvider class. In this new class, you can override any of the methods defined in the BookProvider class to customize its behavior for the specific ebook store.

Here are the steps to create your own BookProvider class:

Step 1: Import the necessary packages

To create a new BookProvider class, start by importing the packages that are needed for your implementation. For example, if you need to use the Selenium package to interact with a web-based ebook store, you would import it at the beginning of your file:
### coming soon...
