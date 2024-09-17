from flask import Flask,request,jsonify
from flask_restful import Resource, Api
import load_credentials
from os_info import OSInfo
from loadconfig import Config,Dotenv
import logg3r
from prepare import SignalSum

from multipass import Serverside,ClientSide


app = Flask(__name__)
api = Api(app)

@auth.verify_password
def verify_password(username, password):
    if username in load_credentials.users.credentials and \
            check_password_hash(users.get(username), password):
        return username





@app.route(
    "/installible-images",
    methods = ["GET"]
    )
def installibleImages():
    ""
    #TODO: burada "multipass find --format json" seklinde ciktilar verilecek



@app.route(
    rule="/create-instance",
    methods = ["GET","POST"]
    )
def createInstance():


@app.route(rule="/instances",
           methods = ["GET"]
           )
def instances():
    #TODO burada "multipass list" komutu calisacak ve gelen body return edilecek


@app.route("/about/<uri:str>", methods=["GET"])
def about(uri):
    match uri:
        case "machine-info":
            return jsonify(OSInfo.commoninfo)
        case "multipass-status":
            return jsonify(SignalSum.multipassOk())
        case "multipass-version":
            return jsonify(Serverside.version())
        case "appversion":
            return jsonify(Dotenv.appversion())
        case "errors":



if __name__ == "__main__" and SignalSum:

    app.run(
        debug=Config.SERVER_DEBUG,
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT
        )