# Copy all files from a specified source folder to a specified destination folder for backup
# purposes. If a file exists in the destination folder but not the source folder, it is deleted.

# Deploy:
# cp -u home_folder_backup.py /home/matt/Scripts

import os
import logging
from types import SimpleNamespace
from shutil import copyfile

foldersToBackup = [
    SimpleNamespace(sourcePath = '/home/matt/Documents', backupPath = '/mnt/XtraDisk/OneDrive/Mint_Backup/Documents', errors = []),
    SimpleNamespace(sourcePath = '/home/matt/Pictures', backupPath = '/mnt/XtraDisk/OneDrive/Mint_Backup/Pictures', errors = [])
]

def main():
    # name the log file as "{this_filename}.log"
    logFileName = f'{os.path.splitext(os.path.basename(__file__))[0]}.log'
    configureLogger(logFileName)

    for folder in foldersToBackup:
        syncFolders(folder)

        # log each error to file
        [logging.error(error) for error in folder.errors if len(folder.errors) > 0]

    logging.info('Folder backup complete.')

def configureLogger(logFileName):
    logging.basicConfig(
        filename=logFileName,
        filemode='w', # overwrite the log file contents each time
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.DEBUG
    )

    if os.path.exists(logFileName):
        os.remove(logFileName)
 
def syncFolders(folderToBackup):
    sourceFiles = getAllFilesInFolder(folderToBackup.sourcePath)
    destFiles = getAllFilesInFolder(folderToBackup.backupPath)

    # delete any files in the destination folder which do not exist in the source folder
    for file in destFiles:
        if (sourceFiles.count(file.replace(folderToBackup.backupPath, folderToBackup.sourcePath)) == 0):
            try:
                os.remove(file)
            except OSError as e:
                folderToBackup.errors.append(f'File "{file}" - {e.strerror}')

    # delete any empty folders left inside the destination folder
    try:
        deleteEmptyFolders(folderToBackup.backupPath)
    except OSError as e:
        folderToBackup.errors.append(f'Error deleting empty folders: ({folderToBackup.backupPath}) error: {e.strerror}')

    # copy all files from source folder to destination folder
    for sourceFile in sourceFiles:
        destFile = os.path.join(folderToBackup.backupPath, sourceFile.replace(folderToBackup.sourcePath, '').lstrip('/'))
        try:
            os.makedirs(os.path.dirname(destFile), exist_ok=True)
            copyfile(sourceFile, destFile)
        except OSError as e:
            folderToBackup.errors.append(f'Error copying "{sourceFile}" to "{destFile}" - {e.strerror}')

def getAllFilesInFolder(folder):
    allFiles = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            allFiles.append(os.path.abspath(os.path.join(root, file)))
    
    return allFiles

def deleteEmptyFolders(folder):
    for root, dirs, files in os.walk(folder, topdown = False):
        for dir in dirs:
            fullDirPath = os.path.join(root, dir)
            if os.path.basename(os.path.normpath(fullDirPath)) == folder:
                continue
            if os.path.isdir(fullDirPath) and len(os.listdir(fullDirPath)) == 0:
                os.rmdir(fullDirPath) 

if __name__ == "__main__":
    main()
