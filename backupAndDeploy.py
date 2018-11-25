# import packages
import json
import os
from datetime import date
from backupTracker import backupTracker


#helper methods
def executeCommand(command, filename=None):
    command += "sudo " + command
    print("executing: ", command)

    os.system(command)

    if (filename !=None & os.path.exists( filename)):  # If filename parameter was passed
        deployFiles.append(filename)    # add to deployment list
        return True
    else:
        return False


# read from config
with open('config.json') as json_data_file:
    configData = json.load(json_data_file)

ftpHost = configData["ftp"]["host"]
ftpUsername = configData["ftp"]["username"]
ftpPassword = configData["ftp"]["password"]
ftpDir = configData["ftp"]["password"]
mysqlUsername = configData["mysql"]["username"]
mysqlPassword = configData["mysql"]["password"]
excludeDir = configData["excludeDir"]
includeDir = configData["includeDir"]
deploymentDir = configData["deploymentDir"]
backupMySql = configData["backupMySql"]

# initialize variables
command = ""
filename = ""
deployFiles = []
dateFormat = str(date.today().year) + str(date.today().month) + str(date.today().day)
readyToDeploy = True
removeFiles=[]

# create folders if doesn't exist
# if((os.path.isdir(deploymentDir)) != True):
#     os.mkdir(deploymentDir)
#     os.mkdir(deploymentDir + "/sqlDumps")
#     os.mkdir(deploymentDir + "/compressedDirs")


if (deploymentDir):  # if folder exists, start packaging

    # package directory tars
    filename = deploymentDir + "compressedDirs/"+ dateFormat + "_site.tar.gz"  # format filename and command
    command = "tar -czvf " + filename

    for x in excludeDir:  # excluded directories
        command += " --exclude=" + x

    for x in includeDir:  # included directories
        command += " " + x

    if (executeCommand(command, filename)):  # Executing command
        readyToDeploy = True
        print("::LOG:: Directory Compression: SUCCEEDED")
    else:
        readyToDeploy = False
        print("::LOG:: Directory Compression: FAILED")

    # package database dumps
    filename =  deploymentDir +"sqlDumps/" + dateFormat+ "_mysqlDump.sql"
    command = "mysqldump -u " + mysqlUsername + " -p'" + mysqlPassword + "' --all-databases >" + deploymentDir + filename

    if (executeCommand(command, filename)):  # Executing command
        readyToDeploy = True
        print("LOG:: MySql Dump: SUCCEEDED")
    else:
        readyToDeploy = False
        print("LOG:: MySql Dump: FAILED")

    # deploying to box and managing:
    command = "lftp -u '"+ftpUsername+","+ftpPassword+"' "+ftpHost+" -e 'mkdir"+ftpDir+"; cd "+ftpDir+"; "
    #cd /DairyMgt_Backups; put /var/boxBackupDeployment/20181107_initialMySQL.sql; '"

    #add deployment files
    if(len(deployFiles) > 0):
        for package in deployFiles:
            command += "put " + package + "; "
    else:
        print("LOG:: Deployment List is empty! Something went wrong")

    removeFiles = backupTracker(deployFiles)

    if (len(deployFiles) > 0):
        for removeFile in removeFiles:
            command += "rm "+ removeFile+"; "
    else:
        print("LOG:: Remove File List is empty")
    command += "'"

    if(readyToDeploy):
        if(executeCommand(command)):
            print("LOG:: LFTP Deployment: SUCCEEDED")
        else:
            print("LOG:: LFTP Deployment: FAILED")
    else:
        print("LOG:: LFTP Deployment: FAILED")


else:
    print(deploymentDir, " does not exist nor was created. Something went wrong. Check permission and location of deployentDir in config.json")

# deploy files to host
if (readyToDeploy):
    print("Deploying")
