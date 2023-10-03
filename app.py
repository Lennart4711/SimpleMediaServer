from flask import Flask, render_template, request, Response, jsonify
import os
import socket

app = Flask(__name__)

# Define the path to the directory containing movie folders
MOVIES_DIR = os.path.expanduser('~/Videos')

# Create a socket server for video streaming
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5678))
server_socket.listen(0)

def find_media_files(movie_folder):
    video_file = None
    subtitle_file = None

    for filename in os.listdir(movie_folder):
        if filename.endswith('.mp4'):
            video_file = os.path.join(movie_folder, filename)
        elif filename.endswith('.srt'):
            subtitle_file = os.path.join(movie_folder, filename)

    return video_file, subtitle_file

@app.route('/')
def index():
    # List all available movies
    movies = sorted(os.listdir(MOVIES_DIR))
    return render_template('index.html', movies=movies)

@app.route('/movie/<movie_name>')
def play_movie(movie_name):
    movie_folder = os.path.join(MOVIES_DIR, movie_name)
    video_file, subtitle_file = find_media_files(movie_folder)

    if video_file:
        return render_template('play_movie.html', movie_name=movie_name, video_file=video_file)
    else:
        return "Movie not found."

def video_generator(video_file, start_time=0):
    # Function to generate video stream starting from a specific timestamp
    with open(video_file, 'rb') as f:
        f.seek(start_time)
        print(start_time)
        while True:
            video_data = f.read(1024)
            if not video_data:
                break
            yield video_data

@app.route('/video/<movie_name>')
def video_stream(movie_name):
    movie_folder = os.path.join(MOVIES_DIR, movie_name)
    video_file, _ = find_media_files(movie_folder)

    if video_file:
        start_time = int(request.args.get('start_time', 0))
        return Response(video_generator(video_file, start_time), content_type='video/mp4')
    else:
        return "Movie not found."

@app.route('/get_video_length/<movie_name>')
def get_video_length(movie_name):
    movie_folder = os.path.join(MOVIES_DIR, movie_name)
    video_file, _ = find_media_files(movie_folder)

    if video_file:
        video_length = os.path.getsize(video_file)
        return jsonify({'video_length': video_length})
    else:
        return jsonify({'error': 'Movie not found'})

if __name__ == '__main__':
    app.run(host="localhost", port=5500, debug=True, threaded=True)
