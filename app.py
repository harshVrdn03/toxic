from flask import Flask, request, jsonify
from picpurify.api import PicPurifyImage, PicPurifyException
import os

PICPURIFY_API_KEY = os.environ.get('PICPURIFY_API_KEY')
PICPURIFY_MODERATION_CLASSES = ['porn_moderation', 'weapon_moderation']

# Initialize PicPurifyImage client
image_client = PicPurifyImage(PICPURIFY_API_KEY, PICPURIFY_MODERATION_CLASSES)
app = Flask(__name__)
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
        
