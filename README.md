# Linux-LFTP-Backup-Tool

**Linux-LFTP-Backup-Tool** is a python based tool that compresses directories and MySql database to deploy to another server using LFTP. The tool keeps track of the files being added or removed using a Queue system to keep only a desired number of latest backups.

**NOTE:**
* This project is in an early stage. The protocol may change frequently.

# Pre-requisites
```sh
sudo apt-get update
sudo apt-get install python3
sudo apt-get install lftp
```

# Usage

## 1. Clone Project in Linux server
```sh
git clone https://github.com/Nakzz/Linux-LFTP-Backup-Tool.git
```

## 2. Configure config.json
1. Enter project directory

2. Add FTP credentials

3. Add MySql credentials

4. Add included and excluded dirs

## 3. Open terminal and run 
If multiple versions of python is installed
```sh
sudo python3 backupAndDeploy.py
```

If only Python3 is installed
```sh
sudo python backupAndDeploy.py
```

## 4. Schedule it to run on the weekends using crontab
```sh
sudo crontab -e
```

Add the following lines to run every Saturday night
```sh
0 0 * * 6 cd /*LOCATION OF THE PROJECT*/; python3/*LOCATION OF THE PROJECT*/backupAndDeploy.py > /var/ftpDeployment/systemOutput.log
```
Replace /*LOCATION OF THE PROJECT*/ with your project directory. For example: 
```sh
0 0 * * 6 cd /var/ftpDeployment/Auto-Linux-Server-Backup/; python3 /var/ftpDeployment/Auto-Linux-Server-Backup/backupAndDeploy.py > /var/ftpDeployment/systemOutput.log
```

## License

    Copyright [2018] [Ajmain Naqib]
