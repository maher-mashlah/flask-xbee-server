import eventlet
eventlet.monkey_patch()
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(
    app,
    async_mode='eventlet',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

latest_data = "Waiting for data..."

@app.route('/')
def index():
    return render_template('index.html', data=latest_data)

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    content = request.json or {}
    latest_data = content.get("data", "No data")
    print("📥 Received:", latest_data)
    socketio.emit("xbee_data", {"data": latest_data})
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
