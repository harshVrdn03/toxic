from flask import Flask, request, jsonify
from picpurify.api import PicPurifyImage, PicPurifyException
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)
# Replace these placeholder values with your actual API keys and workflow
PICPURIFY_API_KEY = os.environ.get('PICPURIFY_API_KEY')
PICPURIFY_MODERATION_CLASSES = ['porn_moderation', 'weapon_moderation']

SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER')
SIGHTENGINE_API_SECRET = os.environ.get('SIGHTENGINE_API_SECRET')
SIGHTENGINE_WORKFLOW = os.environ.get('SIGHTENGINE_WORKFLOW')

# Initialize PicPurifyImage client
image_client = PicPurifyImage(PICPURIFY_API_KEY, PICPURIFY_MODERATION_CLASSES)

@app.route('/check_moderation', methods=['POST'])
def check_moderation():
    try:
        # Get the image URL from the request
        image_url = request.json.get('image_url')

        # Check if the 'image_url' parameter is present in the request
        if not image_url:
            return jsonify({'error': 'Image URL is required'}), 400

        # Analyze the image using PicPurify API
        response = image_client.analyse(image_url)

        # Check the moderation decision
        if response['final_decision'] == 'OK':
            return jsonify({'status': 'Image Accepted', 'details': response}), 200
        else:
            return jsonify({'status': 'Image Rejected', 'reject_criteria': response['reject_criteria']}), 403

    except PicPurifyException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/video_moderation', methods=['POST'])
def video_moderation():
    try:
        # Get the video URL from the request
        video_url = request.json.get('video_url')

        # Check if the 'video_url' parameter is present in the request
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # Set up parameters for Sightengine API
        sightengine_params = {
            'stream_url': video_url,
            'workflow': SIGHTENGINE_WORKFLOW,
            'api_user': SIGHTENGINE_API_USER,
            'api_secret': SIGHTENGINE_API_SECRET
        }

        # Make a request to Sightengine API
        sightengine_response = requests.get('https://api.sightengine.com/1.0/video/check-workflow-sync.json', params=sightengine_params)

        # Parse the Sightengine API response
        sightengine_output = json.loads(sightengine_response.text)

        # Video accepted
        return jsonify({'status': 'Video Accepted', 'details': sightengine_output}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
