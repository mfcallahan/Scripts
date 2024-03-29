# Delete all files in a folder which are older than the specified number days.

import os
import logging
import datetime
from types import SimpleNamespace

cleanupFolders = [
    SimpleNamespace(path = '/home/matt/Temp', days = 7, errors = []),
    SimpleNamespace(path = '/home/matt/Downloads', days = 30, errors = []),
    SimpleNamespace(path = '/home/matt/Desktop', days = 1, errors = [])
]

def main():
    # name the log file as "{this_filename}.log"
    logFileName = f'{os.path.splitext(os.path.basename(__file__))[0]}.log'
    logFilePath = os.path.join(os.path.dirname(__file__), logFileName)
    
    if os.path.exists(logFilePath):        
        os.remove(logFilePath)
    
    configureLogger(logFilePath)

    for folder in cleanupFolders:
        deleteFilesInFolder(folder)
        deleteEmptyFolders(folder)

        if len(folder.errors) > 0:
            for error in folder.errors:
                logging.error(error)

    logging.info('Folder cleanup complete.')

def configureLogger(logFilePath):
    logging.basicConfig(
        filename=logFilePath,
        filemode='w', # overwrite the log file contents each time
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.DEBUG
    )

def deleteFilesInFolder(cleanupFolder):
    now = datetime.datetime.now()
    for root, dirs, files in os.walk(cleanupFolder.path):
        for file in files:
            currentFilePath = os.path.join(root, file)
            currentFileModifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(currentFilePath))
            
            if now - currentFileModifiedTime > datetime.timedelta(days=cleanupFolder.days):
                try:
                    os.remove(currentFilePath)
                except OSError as e:
                    cleanupFolder.errors.append(f'File "{currentFilePath}" - {e.strerror}')
                    

def deleteEmptyFolders(cleanupFolder):
    for root, dirs, files in os.walk(cleanupFolder.path, topdown = False):
        for dir in dirs:
            fullDirPath = os.path.join(root, dir)
            if os.path.isdir(fullDirPath) and len(os.listdir(fullDirPath)) == 0:
                try:
                    os.rmdir(fullDirPath)
                except OSError as e:
                    cleanupFolder.errors.append(f'Folder "{fullDirPath}" - {e.strerror}')

if __name__ == "__main__":
    main()

