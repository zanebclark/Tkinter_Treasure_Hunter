from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="Tkinter_Treasure_Hunter",
    version="1.1",
    long_description="""
    A simple clicking game that was initially inspired by John Harper's Udemy Course "The Ultimate Tkinter Course: GUI 
    for Python Projects". Thanks to a great deal of architectural coaching from James A Crabb (Git:jacrabb), the game 
    became an exercise in developing apps using the MVC architecture.""",
    url="https://github.com/zanebclark/Tkinter_Treasure_Hunter",
    author="Zane Clark",
    author_email="zanebclark@gmail.com",
    packages=[find_packages()],
    zip_save=False,
)