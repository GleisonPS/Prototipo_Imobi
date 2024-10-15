from flask import *

from proprietario.propriatario import propriatario
import sqlite3


app = Flask(__name__)
app.register_blueprint(propriatario, url_prefix="/propriatario")


@app.route('/')
def index():
    
    return redirect("/propriatario")


if __name__=="__main__":
    app.run(debug= True)