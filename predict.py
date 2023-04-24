import pickle
from flask import Flask, request, jsonify

with open('reports/train_pipe.joblib', 'rb') as f_in:
    (model)= pickle.load(f_in)

app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    ride = request.get_json()

    result = {
        'duration': pred
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)