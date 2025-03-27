from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    quality = request.form['quality']

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    if format_type == 'video':
        ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        ydl_opts['merge_output_format'] = 'mp4'
    elif format_type == 'audio':
        ydl_opts['format'] = 'bestaudio'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        # Ensure the output template explicitly sets .mp3 for audio
        ydl_opts['outtmpl'] = 'downloads/%(title)s.mp3'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Get the final filename after download
            file_path = ydl.prepare_filename(info)
            if format_type == 'audio':
                # For audio, override with .mp3 extension after postprocessing
                file_path = os.path.splitext(file_path)[0] + '.mp3'
            elif format_type == 'video':
                file_path = os.path.splitext(file_path)[0] + '.mp4'

            # Verify the file exists before sending
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True)