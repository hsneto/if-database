sudo apt-get update

# set up enviroment
sudo apt install python3-pip
sudo apt install virtualenv

virtualenv --python='/usr/bin/python3' env

source env/bin/activate
pip install -r requirements.txt 

# set up scritps
chmod +x scritps/fer-emotions.sh

