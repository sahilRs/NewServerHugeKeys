from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

valid_keys = {
    "TEST1": {"is_used": False, "device_id": None, "last_verified": None},
    "TEST2": {"is_used": False, "device_id": None, "last_verified": None},
    "TEST3": {"is_used": False, "device_id": None, "last_verified": None},
    "TEST4": {"is_used": False, "device_id": None, "last_verified": None}
}

@app.route('/keys', methods=['GET'])
def verify_key():
    key = request.args.get('key')
    device_id = request.args.get('device_id')
    
    if not key or not device_id:
        return jsonify({"error": "Missing key or device ID"}), 400

    if key not in valid_keys:
        return jsonify({"error": "Invalid key"}), 401

    key_data = valid_keys[key]
    
    if key_data["is_used"] and key_data["device_id"] != device_id:
        return jsonify({"error": "Key already in use by another device"}), 403
        
    valid_keys[key] = {
        "is_used": True,
        "device_id": device_id,
        "last_verified": datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "message": "Key verified successfully"
    })

@app.route('/ids', methods=['GET', 'POST'])
def manage_device_ids():
    if request.method == 'GET':
        # Return list of registered devices with their keys
        devices = {
            key: data["device_id"] 
            for key, data in valid_keys.items() 
            if data["is_used"]
        }
        return jsonify(devices)
    
    elif request.method == 'POST':
        device_id = request.data.decode('utf-8')
        key = request.args.get('key')
        
        if not device_id or not key:
            return jsonify({"error": "Missing device ID or key"}), 400
            
        if key not in valid_keys:
            return jsonify({"error": "Invalid key"}), 401
            
        key_data = valid_keys[key]
        
        if key_data["is_used"] and key_data["device_id"] != device_id:
            return jsonify({"error": "Key already in use"}), 403
            
        valid_keys[key]["device_id"] = device_id
        valid_keys[key]["is_used"] = True
        valid_keys[key]["last_verified"] = datetime.now().isoformat()
        
        return jsonify({
            "message": "Device registered successfully",
            "key": key
        }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
