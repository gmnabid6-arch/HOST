import os
from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return "Backend is running successfully!"

@app.route('/download')
def download():
    url = request.args.get('url')
    fmt = request.args.get('format', 'mp4')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # yt-dlp configuration based on format type
    ydl_opts = {}
    if fmt in ['mp3', 'm4a', 'wav', 'ogg', 'flac', 'aac']:
        ydl_opts = {
            'format': 'bestaudio/best',
        }
    else:
        ydl_opts = {
            'format': 'best/bestvideo+bestaudio',
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            download_url = info.get('url')
            if download_url:
                return redirect(download_url)
            else:
                return jsonify({'error': 'Could not fetch direct video URL'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
