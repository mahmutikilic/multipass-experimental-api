from flask import Flask, request, jsonify
from flask_restful import Api

from load_credentials import Users
from os_info import OSInfo
from loadconfig import Config, Dotenv
from multipass import list_instances, find_images, launch_instance, get_version
import logg3r

app = Flask(__name__)
api = Api(app)

logger = logg3r.setup_logging()
config = Config()
users = Users()


@app.route("/installable-images", methods=["GET"])
def installable_images():
    try:
        return jsonify(find_images())
    except Exception as exc:
        logger.error(exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/create-instance", methods=["POST"])
def create_instance():
    data = request.json or {}
    name = data.get("name")
    cpu = data.get("cpu")
    disk = data.get("disk")
    mem = data.get("mem")
    image = data.get("image")
    try:
        new_name = launch_instance(name, cpu, disk, mem, image)
        return jsonify({"name": new_name})
    except Exception as exc:
        logger.error(exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/instances", methods=["GET"])
def instances():
    try:
        return jsonify(list_instances())
    except Exception as exc:
        logger.error(exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/about/<string:uri>", methods=["GET"])
def about(uri):
    info = OSInfo()
    if uri == "machine-info":
        return jsonify(info.commoninfo)
    if uri == "multipass-status":
        try:
            ver = get_version()
            return jsonify({"multipass": ver})
        except Exception:
            return jsonify({"multipass": "not available"}), 503
    if uri == "multipass-version":
        try:
            return jsonify({"version": get_version()})
        except Exception as exc:
            return jsonify({"error": str(exc)}), 500
    if uri == "appversion":
        return jsonify(Dotenv().appversion())
    return jsonify({"error": "unknown"}), 404


if __name__ == "__main__":
    logger.info("Starting server")
    app.run(debug=config.SERVER_DEBUG, host=config.SERVER_HOST, port=config.SERVER_PORT)
