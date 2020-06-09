In order to run an rqworker, it requires the `os.fork()` function, but this will **NOT** be available on Windows OS systems. Thus, if testing the Django app on Windows, a Linux subsystem is required. Windows Subsystem for Linux (WSL)

## Setup
The basic setup in detailed in the instructions at the bottom. The remaining aspects are to setup the rqworker in the subsystem for `django-rq` to work.

### Windows
In Programs and Features, click *Turn Windows features on or off* to open the pop-up. Then make sure the *Virtual Machine Platform* is ticked. Click Ok and then restart PC.
![image](/static/img/markdowns/ubuntu_subsystem_installation.jpg)

Once the PC has restarted, open Powershell and run: `wsl --set-default-version 2` to set the WSL version to 2. Restart PC again.

After PC has restarted, navigate to *Ubuntu 18.04 LTS* subsystem [installation page](https://www.microsoft.com/en-ca/p/ubuntu-1804-lts/9n9tngvndl3q?rtc=1&activetab=pivot:overviewtab) Follow the prompts and your PC will need to be restarted again.

Finally, the PC has restarted again and Ubuntu subsystem can be loaded -- this may take longer as it is the first time. Follow the prompts to create a username and password (keep this handy for future use)!

### Ubuntu Subsystem
Once user setup is completed, now the django project needs to be loaded to the subsystem. But first, need to run an apt-get update, then install python3 and redis server.

#### Python Virtual Environment Setup
```
sudo apt-get update
sudo apt-get install python3 python3-pip redis-server
pip install virtualenv
python -m virtualenv venv
```

Create a `.env` file as needed for including environment variables. 

#### Get the Django App from Repo
```
mkdir [app name]
cd [app name]
git init
git remote add [repo name] [repo link]
git pull [repo name] master
source ../venv/bin/activate && set -a; source ../.env; set +a;
python -m pip install -r requirements.txt
```

#### Setup Redis Server
`sudo nano /etc/redis/redis.conf`, find `# requirepass yourpassword` and replace `yourpassword` with your password; these instructions will keep it as `yourpassword`

Note that below the `redis-cli` opens up the redis terminal.
```
sudo service redis-server restart
redis-cli
CONFIG SET requirepass "yourpassword"
AUTH yourpassword
exit
```

*NOTE: Make sure **yourpassword** is set up in the *settings.py* file as well.*

#### Run rqworker
Once back in the ubuntu terminal, run: `python manage.py rqworker` and the queue should be ready to accept tasks.

## Links
[Installation](https://docs.microsoft.com/en-us/windows/wsl/install-win10)  
[Ubuntu 18.04 WSL](https://www.microsoft.com/en-ca/p/ubuntu-1804-lts/9n9tngvndl3q?rtc=1#activetab=pivot:overviewtab)  
[Redis Server](https://medium.com/@umutuluer/resolving-the-err-client-sent-auth-but-no-password-is-set-error-b81438d10843)  