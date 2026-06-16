from flask import Flask, request, jsonify
import threading
import database_handler  # Imports YOUR database_handler.py file seamlessly!

app = Flask(__name__)

# OS Mechanism: Track active threads for monitoring/Expo justification purposes
active_connections_counter = 0
counter_lock = threading.Lock() #[cite: 3]

# Fungsi tambahan untuk membenarkan Dashboard (CORS) membaca API ini tanpa disekat browser
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response

@app.route('/api/safety', methods=['POST'])
def handle_safety_payload():
    """
    This route intercepts incoming JSON payloads from the ESP32.[cite: 3]
    """
    global active_connections_counter
    
    # OS Concept: Simulate spawning/tracking a unique concurrent task process[cite: 3]
    with counter_lock:
        active_connections_counter += 1
        current_thread_id = threading.get_ident()
        print(f"\n[SERVER] New Client Request incoming! Assigned to OS Thread ID: {current_thread_id}")
        print(f"[SERVER] Concurrent connections handled by system: {active_connections_counter}")

    try:
        # Extract the raw JSON structure sent by the IoT team's ESP32[cite: 3]
        payload = request.get_json()
        
        if not payload:
            return jsonify({"status": "error", "message": "Malformed or empty JSON data"}), 400

        # CRITICAL COUPLING: Safely pass the data into YOUR database thread-safe file[cite: 3]
        database_handler.save_safety_data(payload)

        # OS Feature: Prioritized background log notifications[cite: 3]
        if payload.get("emergency_sos") is True:
            print(f"!!! [CRITICAL INTERRUPT] EMERGENCY SOS RECEIVED FROM RUNNER: {payload.get('runner_id')} !!!")

        # Reduce the active connection count once processing finishes[cite: 3]
        with counter_lock:
            active_connections_counter -= 1
            
        return jsonify({"status": "success", "message": "Telemetry logged safely"}), 200

    except Exception as e:
        print(f"[SERVER ERROR] Exception thrown during execution: {str(e)}")
        with counter_lock:
            active_connections_counter -= 1
        return jsonify({"status": "internal_error", "message": str(e)}), 500


@app.route('/api/safety/live', methods=['GET'])
def expose_live_dashboard_feed():
    """
    API Integration Window for Component 5 (Central Dashboard).[cite: 3]
    When they run a request here, it pulls data directly via your data locks.[cite: 3]
    """
    print("\n[SERVER] Centralized Dashboard fetching latest updates...")
    logs = database_handler.get_all_logs() #[cite: 3]
    return jsonify(logs), 200


if __name__ == "__main__":
    print("==================================================")
    print("      SMART FUN RUN MULTITHREADED OS SERVER       ")
    print("==================================================")
    print("[OS SETUP] Exposing server across all local interfaces...")
    print("[OS SETUP] Listening on Port: 5000")
    print("[OS SETUP] Target Endpoint URL: http://localhost:5000/api/safety")
    print("==================================================")
    
    # Menjalankan server pada Port 5000 dengan sokongan multithreading aktif
    app.run(host="0.0.0.0", port=5000, threaded=True)
