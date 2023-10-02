import os
from flask import Flask, render_template, send_from_directory, request, Response

app = Flask(__name__)
media_folder = os.path.expanduser("~/Videos")

@app.route('/')
def index():
    movies = os.listdir(media_folder)
    return render_template('index.html', movies=movies)

@app.route('/movie/<movie_name>')
def serve_movie(movie_name):
    movie_folder = os.path.join(media_folder, movie_name)
    movie_file = os.path.join(movie_folder, "movie.mp4")
    return send_from_directory(movie_folder, "movie.mp4")

@app.route('/subtitles/<movie_name>')
def serve_subtitles(movie_name):
    movie_folder = os.path.join(media_folder, movie_name)
    subtitles_file = os.path.join(movie_folder, "subtitles.srt")
    return send_from_directory(movie_folder, "subtitles.srt")

def generate_movie(movie_path):
    chunk_size = 1024 * 1024  # 1MB chunks, adjust as needed

    with open(movie_path, 'rb') as video_file:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break
            yield chunk

@app.route('/stream_movie/<movie_name>')
def stream_movie(movie_name):
    movie_folder = os.path.join(media_folder, movie_name)
    movie_file = os.path.join(movie_folder, "movie.mp4")

    return Response(generate_movie(movie_file), mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
