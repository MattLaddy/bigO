from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import io
import matplotlib.pyplot as plt
import matplotlib
import threading

# Use a backend that does not require a GUI (e.g., Agg)
matplotlib.use('Agg')

app = Flask(__name__)

def generate_graph():
    # This function is now thread-safe for Matplotlib
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])  # Example data; replace with actual performance metrics
    plt.title('Performance Graph')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    graph_stream = io.BytesIO()
    plt.savefig(graph_stream, format='png')
    plt.close()
    graph_stream.seek(0)
    return graph_stream

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code')
    
    try:
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, timeout=5)
        output = result.stdout + result.stderr

        # Use a thread to generate the graph to avoid blocking
        graph_stream = threading.Thread(target=generate_graph)
        graph_stream.start()
        graph_stream.join()

        return jsonify({
            'output': output,
            'graph_url': '/graph'
        })
    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = str(e)
    
    return jsonify({'output': output, 'graph_url': ''})

@app.route('/graph')
def graph():
    graph_stream = generate_graph()
    return send_file(graph_stream, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
