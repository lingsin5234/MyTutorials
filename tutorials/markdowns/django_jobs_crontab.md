In order to run django jobs with crontab:
1.  declare environment variables prior to each run
2.  call the virtual environment
3.  run the job
4.  deactivate the virtual environment once completed

To do this, set up a bash script to run everything, this make crontab easier to read
```bash
#! /bin/bash
cd ~/django
source my_env/bin/activate && set -a; source .env; set +a;
python manage.py runjob processTeam
deactivate
```

In the crontab:
```cron
# Mon-Fri every 4 hours at 00 and 30 minutes
#   run processTeam and generateStats respectively
0 */4 * * 1-5 ~/processTeam.sh >> ~/django/crontab.log 2>&1   
30 */4 * * 1-5 ~/generateStats.sh >> ~/django/crontab.log 2>&1
# Sundays at 6:45 AM, run importYear
45 06 * * 0 ~/importYear.sh >> ~/django/crontab.log 2>&1
```

The `2>&1` will also record any error messages into the log file.

## Links
[Instructions](https://askubuntu.com/questions/1119526/how-to-run-django-cron-in-crontab)  
[Current Server Time](https://askubuntu.com/questions/27528/how-can-i-display-the-current-time-date-setting)  