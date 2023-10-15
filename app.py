from flask import Flask, request, jsonify
from detoxify import Detoxify
app = Flask(__name__)
model = Detoxify('original')
@app.route('/')
def hello_world():
    return 'Hello, World! from Harsh Vardhan'
@app.route('/analyze', methods=['POST'])
def analyze_toxicity():
    data = request.get_json()  # Get the JSON data from the request body
    text = data.get('text')    # Get the 'text' field from the JSON data
    results = model.predict(text)

    # Extract the specific toxicity scores you want to return
    toxicity_score = results.get('toxicity')
    severe_toxicity_score = results.get('severe_toxicity')
    toxicity = results['toxicity']
    severe_toxicity = results['severe_toxicity']
    obscene = results['obscene']
    threat = results['threat']
    insult = results['insult']
    identity_attack = results['identity_attack']
    print(results)
    results = {key: float(value) for key, value in results.items()}
    return results 
