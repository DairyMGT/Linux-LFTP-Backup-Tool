import json
import os
from datetime import date
from backupTracker import backupTracker
import logging

#logging object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('log.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
logger.info('')
logger.info('Starting logging!')

#helper methods
def executeCommand(command, filename=None):

    logger.info("executing: "+ command)

    os.system(command)

    if (filename !=None and os.path.exists( filename)):  # If filename parameter was passed
        deployFiles.append(filename)    # add to deployment list
        return True
    else:
        return False


# read from config
with open('config.json') as json_data_file:
    configData = json.load(json_data_file)

backupMySql = (configData["backupMySql"])
backupDir = (configData["backupDir"])
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
neededDirectories = [deploymentDir, deploymentDir + "sqlDumps", deploymentDir + "compressedDirs"]

# create folders if doesn't exist
for dir in neededDirectories:
    if((os.path.exists(dir)) != True):
        logger.info("creating dir: " + dir)
        os.mkdir(dir)


if (os.path.exists(deploymentDir)):  # if folder exists, start packaging

    # package directory tars
    if(backupDir == "True"):
        filename = deploymentDir + "compressedDirs/"+ dateFormat + "_site.tar.gz"  # format filename and command
        command = "tar -czf " + filename

        for x in excludeDir:  # excluded directories
            command += " --exclude=" + x

        for x in includeDir:  # included directories
            command += " " + x

        print("COMAND: "+ command)

        if (executeCommand(command, filename)):  # Executing command
            readyToDeploy = True
            logger.info("Directory Compression: SUCCEEDED: " )

        else:
            readyToDeploy = False
            print("::LOG:: Directory Compression: FAILED")

    # package database dumps
    if(backupMySql == "True"):
        filename =  deploymentDir +"sqlDumps/" + dateFormat+ "_mysqlDump.sql"
        command = "mysqldump -u " + mysqlUsername + " -p'" + mysqlPassword + "' --all-databases >" + deploymentDir + filename

        if (executeCommand(command, filename)):  # Executing command
            readyToDeploy = True
            logger.info(" MySql Dump: SUCCEEDED")
        else:
            readyToDeploy = False
            logger.warning(" MySql Dump: FAILED")

    # deploying to box and managing:
    command = "lftp -u '"+ftpUsername+","+ftpPassword+"' "+ftpHost+" -e 'mkdir"+ftpDir+"; cd "+ftpDir+"; "
    #cd /DairyMgt_Backups; put /var/boxBackupDeployment/20181107_initialMySQL.sql; '"

    #add deployment files
    if(len(deployFiles) > 0):
        for package in deployFiles:
            command += "put " + package + "; "
    else:
        logger.warning(" Deployment List is empty! Something went wrong")

    removeFiles = backupTracker(deployFiles)

    if (len(deployFiles) > 0):
        for removeFile in removeFiles:
            command += "rm "+ removeFile+"; "
    else:
        logger.warning(" Remove File List is empty")
    command += "'"

    if(readyToDeploy):
        if(executeCommand(command)):
            logger.info(" LFTP Deployment: SUCCEEDED")
        else:
            logger.warning(" LFTP Deployment: FAILED")
    else:
        logger.warning(" LFTP Deployment: FAILED")


else:
    print()
    logger.warning(deploymentDir+ " does not exist nor was created. Something went wrong. "
                                  "Check permission and location of deployentDir in config.json")
# deploy files to host
if (readyToDeploy):
    print("Deploying")
    logger.debug("Reached Deployment Stage. Can execute now.")
    #TODO: deploy command
