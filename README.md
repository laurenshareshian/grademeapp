Instructions for setting up a simple grading app on OSU's server:

Make sure your OSU VPN is on.

Log in to flip2 by typing the command below or something with Putty? I'm not sure because I don't have a PC.

ssh {username}@flip2.engr.oregonstate.edu

Once you navigate to whatever directory you want this in on the OSU flip2 server, type the following into your terminal:

git clone https://github.com/laurenshareshian/gradeapp.git

cd gradeapp

bash

virtualenv venv -p $(which python3) 

source ./venv/bin/activate

pip3 install --upgrade pip

pip install -r requirements.txt


source ./venv/bin/activate

export FLASK_APP=main.py

Change 8042 to your favorite four digit number:

python -m flask run -h 0.0.0.0 -p 8042 --reload

Go to http://flip2.engr.oregonstate.edu:8042/ in your browser (change 8042 if necessary)

Type in "Jane Doe" or "John Doe" and you should see the classes they teach:

<img src="https://github.com/laurenshareshian/gradeapp/blob/master/pic.png">

Note: The main Python functions are located within main.py.

To create the database, type "python createdatabase.py"

The form template is located within templates.


(Note: I got most of my instructions from [here](https://github.com/knightsamar/CS340_starter_flask_app)).