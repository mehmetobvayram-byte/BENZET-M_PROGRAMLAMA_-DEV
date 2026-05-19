from flask import Flask, render_template, jsonify, request
import webbrowser
import threading
import carwash_sim
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate')
def simulate():
    try:
        # Yeni parametreleri al (6 tip personel + 2 tip kabin)
        params = {
            'small_bays': int(request.args.get('small_bays', 2)),
            'large_bays': int(request.args.get('large_bays', 1)),
            'service_bays': int(request.args.get('service_bays', 1)),
            'small_wash_staff': int(request.args.get('small_wash_staff', 2)),
            'small_dry_staff': int(request.args.get('small_dry_staff', 2)),
            'large_wash_staff': int(request.args.get('large_wash_staff', 1)),
            'large_dry_staff': int(request.args.get('large_dry_staff', 1)),
            'service_wash_staff': int(request.args.get('service_wash_staff', 1)),
            'service_dry_staff': int(request.args.get('service_dry_staff', 1)),
            'arrival_rate': float(request.args.get('arrival_rate', 10.0)),
            'sim_time': int(request.args.get('sim_time', 480))
        }
        
        result = carwash_sim.run_carwash_sim(**params)
        return jsonify(result)
    except Exception as e:
        print(f"HATA OLUŞTU: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(port=5000, debug=True)
