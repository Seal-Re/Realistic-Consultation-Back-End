from flask import Blueprint, request, send_from_directory
from .utils import createAudio, getParameter

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/dealAudio', methods=['POST', 'GET'])
def dealAudio():
    text = getParameter(request, 'text')
    file_name = getParameter(request, 'file_name')
    voice = getParameter(request, 'voice')
    return createAudio(text, file_name, voice)

@audio_bp.route('/static/<path:filename>')
def serve_static(filename):
    from flask import current_app
    return send_from_directory(current_app.static_folder, filename)