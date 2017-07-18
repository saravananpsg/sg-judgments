"""
Python script to truncate original file name down to id number

Initalize folder name to the folder containing the html files
"""
import os

folder = 'html-files'

for file in os.listdir(folder):
    try:
        os.rename(os.path.join(folder, file), 
            os.path.join(folder, file.split('-')[0] + '.html'))
    except Exception as e:
        raise e