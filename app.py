from flask import Flask, jsonify, render_template, request,redirect,url_for,session
from flask_cors import CORS, cross_origin
import os,json,time
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from twilio.rest import Client
from flask_mail import Mail, Message
import jwt
import requests
from time import time 
import config

app = Flask(__name__)
cors = CORS(app)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'agnal.vincent.paul@gmail.com',
    MAIL_PASSWORD = 'miyixqkithytckxi'
))

mail = Mail(app)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
# Enter your API key and your API secret
API_KEY = 'pal4fTacS2-Rz05uQenboQ'
API_SEC = 'ZcCxNEextZzyg7IHapeqZKzhIqY8hnuw4VM2'


class User:
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)

    def is_active(self):
        # Replace this with your own logic to determine if the user account is active
        return True
    def is_authenticated(self):
        # Replace this with your own logic to determine if the user is authenticated
        return True
# Replace this with your own user loading function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# create a function to generate a token
# using the pyjwt library
 
def generateToken(): 
    token = jwt.encode(
 
        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},
 
        # Secret used to generate token signature
        API_SEC,
 
        # Specify the hashing alg
        algorithm='HS256'
    )
    #print (token)
    #return token.decode('utf-8')
    return token
 
 # create json data for post requests
meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
 
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
 
# send a request with headers including
# a token and meeting details
 
def createMeeting():
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))
 
    #print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
 
    
    return [join_URL,meetingPassword]

def mailsend(mail_id,link):
        subject = "Environment Link"
        msg = Message(subject=subject, sender="agnal.vincent.paul@gmail.com", recipients=[mail_id])
        msg.body = "Hi!\nPlease Click on the following link to get inside the environment. " + str(link)
        mail.send(msg)
        return jsonify({"info":"success"})

@app.route('/send_message/', methods=['GET','POST'])
def send_message():
    num = request.args.get("wn")
    email = request.args.get("email")
    number = 'whatsapp:+91'+num
    res = createMeeting()
    if email != '':
        mailsend(email,res[0])
    account_sid = 'AC8ec7acac4b15a7b1e0c995742991e554'
    auth_token = '2b62961b7305d47df9abc77769335105'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
								  body='pls join the shop link! '+res[0],
								  from_='whatsapp:+14155238886',
								  to=number, 
							  )
    message = client.messages.create(from_='+13158123803',body='pls join the shop link! '+res[0],to='+91'+num)
    return json.dumps({'res':'http://127.0.0.1:8001/invite?data='+res[0]})
 

@app.route('/invite', methods=['GET','POST'])
@login_required
def invite():
        data=request.args.get("data")
        return render_template('invite.html',url=data)  



# Routes
@app.route('/')
def index():
    return render_template('index.html')


# Unauthorized handler
@login_manager.unauthorized_handler
def unauthorized_callback():
    # Store the original request URL in the session
    session['next_url'] = request.path + '?' + request.query_string.decode()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('protected'))

    if request.method == 'POST':
        # Replace this with your own login logic
        user = User(id=1)
        login_user(user)

        # Redirect the user back to the original request URL if available
        next_url = session.pop('next_url', None)
        if next_url:
            return redirect(next_url)

        return redirect(url_for('protected'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8001)
