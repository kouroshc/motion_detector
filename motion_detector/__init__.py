from flask import Flask

app = Flask(__name__ , template_folder='../templates' , static_folder='../static')

app.config['SECRET_KEY'] = '96df97d487f528a91fd22c10ef99a57b'
from motion_detector import routes