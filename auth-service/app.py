from flask import Flask, request, jsonify
import secrets
import os

app = Flask(__name__)
SALT = os.getenv("SALT", "default_salt_12345")

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    p1 = data.get('pass1', '')
    p2 = data.get('pass2', '')
    p3 = data.get('pass3', '')
    
    # أي 3 كلمات مرور غير فارغة تعمل (للاختبار)
    if p1 and p2 and p3:
        session_token = secrets.token_hex(32)
        return jsonify({
            "status": "ok",
            "token": session_token,
            "message": "تم المصادقة بنجاح"
        })
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)