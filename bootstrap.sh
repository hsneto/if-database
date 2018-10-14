sudo apt-get update

# set up enviroment
sudo apt install -y python3-pip
sudo apt install -y virtualenv

virtualenv --python='/usr/bin/python3' env

source env/bin/activate
pip install -r requirements.txt 

deactivate

# set up scritps
# chmod +x scripts/fer-emotions.sh
