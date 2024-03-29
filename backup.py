import os

# backup.py by Abd-afeez Abd-hamid dent4real@yahoo.com
# The Backup class provides a wrapper around the rsync cli command allowing:
# - The directory to exclude can be configured
# - The dry run option is available to ensure a preview is available for files/directories to be backed up
# - Their is a cron option for automating the daily process
# - Ability to view the backup log file if it exists
#
# Assumptions and usage defaults:
# - run backup.py at the root of the user's home directory, ie 'python3 ~/backup.py'
# - backs up the user's home directory minus the excluded directories
# - new ~/backup/ folder will contain the most recent backup
# - excludes directories with backup in the name, and hidden files and directories
# - the -azv switches with use the archive, compressed, and verbose modes of rsync
# - the human readable, progress, and log file rsync options are enabled
#
# The os library is used to execute the cli commands from within python

class Backup_Manager:

    def __init__(self):
        self.default_exclusions = "--exclude '~/backup/***' --exclude 'backup*' --exclude '.*'"
        # edit these as needed:
        self.optional_exclusions = "--exclude '/Dropbox/***' --exclude '/Pictures/***' --exclude '/Movies/***' --exclude '/Examples/***' --exclude 'zsh*'"
        self.src_dir = "/"
        self.dest_dir = "/backup"
        self.base_rsync_options = "--human-readable --progress --log-file='backup.log'"
        self.rsync_run_command = "rsync -avz"
        self.rsync_dry_run_command = "rsync -avzn"
    

    #run rsync commands
    def run(self, mode):
        # mode string should be either "dryrun", "normal", or "cron"
        
        #build list of file and directory and exclusions string
        excludes = self.default_exclusions + " " + self.optional_exclusions
        
        #build rsync cli command string
        cli = self.base_rsync_options + " " + excludes + " " + self.src_dir + " " + self.dest_dir
        if mode == "dryrun":
            cli = self.rsync_dry_run_command + " " + cli
        else:
            cli = self.rsync_run_command + " " + cli
        
        #execute backup or cron with cli
        if mode == "cron":
            self.set_cron_job(cli)
        else:
            self.run_backup(cli)

    #perform manual backup or dry run
    def run_backup(self, cli):
        print("performing backup using: ")
        print(cli)
        os.system(cli)
  

    #set up cron job
    def set_cron_job(self, cli):
        print("setting up daily cron job...")
        print(cli)
        os.system("(echo '* 0 * * * {}') | crontab -".format(cli))


    #view log file
    def view_log(self):
        try:
            os.system("cat ~/backup.log")
        except IOError:
            print("Log file not read")
            return

#main

bm = Backup_Manager()

#get home directory path for this user
home = os.popen('pwd').read()
home = "{}".format(home[:-1]) #strip return character
bm.src_dir = home + bm.src_dir
bm.dest_dir = home + bm.dest_dir

#menu and prompts
command = ""
while command != "q":
    print("")
    print("'d' for a dry run backup to see what will be backed up.")
    print("'b' to execute the backup.")
    print("'v' to view the log file.")
    print("'c' to set up automatic daily backups.")
    print("'q' to quit.")
    command = input("Enter d, b, c, v,  or q: ")
    
    if command == 'q':
        break
    elif command == 'd':
        print("Performing dry run.")
        bm.run("dryrun")
    elif command == 'b':
        print("Running backup.")
        bm.run("normal")
    elif command == 'c':
        print("Adding daily backup cron job.")
        bm.run("cron")
    elif command == 'v':
        print("Viewing log file.")
        bm.view_log()
    else:
        print("Please enter a valid command.")
    

print("Thank you. Backup Manager ended.")
