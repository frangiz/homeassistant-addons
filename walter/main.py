import base64
import glob
import os

from flask import Flask
from flask import jsonify
from flask import request
from flask import send_from_directory

from errors import bad_request
from errors import error_response


app = Flask(__name__)

ROOT_DIR = os.getenv("ROOT_DIT", ".")


@app.route("/api/firmware/updates", methods=["GET"])
def get_new_firmware():
    ver = request.args.get("ver", default=None)
    if ver is None or not ver.isdigit():
        return bad_request("Required parameter 'ver' is missing or not an int.")

    dev_type = request.args.get("dev_type", default=None)
    if dev_type is None:
        return bad_request("Required parameter 'dev_type' is missing.")
    dev_type = dev_type.lower()

    dev_id = request.args.get("dev_id", default=None)
    if dev_id is None:
        return bad_request("Required parameter 'dev_id' is missing.")

    app.logger.debug("ver: " + ver + ", dev: " + dev_type + " dev_id: " + dev_id)

    latest_firmware = find_latest_firmware(ver, dev_type)
    if latest_firmware is None:
        app.logger.debug("Device already up to date")
        return error_response(304, "Device already up to date")

    app.logger.debug("Found firmware version: " + latest_firmware)
    return send_from_directory(
        directory=os.path.join(ROOT_DIR, "firmwares"),
        filename=latest_firmware,
        as_attachment=True,
        mimetype="application/octet-stream",
        attachment_filename=latest_firmware,
    )


@app.route("/api/firmware/updates", methods=["POST"])
def save_new_firmware():
    req = request.json
    app.logger.debug(req)

    data = base64.urlsafe_b64decode(req["data"])
    with open(os.path.join(ROOT_DIR, "firmwares", req["filename"]), "wb") as f:
        f.write(data)

    return jsonify({"msg": "ok"}), 201


def find_latest_firmware(ver, dev_type):
    if not os.path.exists(os.path.join(ROOT_DIR, "firmwares")):
        os.makedirs(os.path.join(ROOT_DIR, "firmwares"))
    firmwares = sorted(
        glob.glob(os.path.join(ROOT_DIR, "firmwares") + "/" + dev_type + "-*.bin"),
        reverse=True,
    )
    if len(firmwares) > 0:
        _, firmware_filename = os.path.split(firmwares[0])
        if firmware_filename != dev_type + "-" + str(ver) + ".bin":
            return firmware_filename
    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
