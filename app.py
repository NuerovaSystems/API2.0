from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

movies = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "year": 2010, "watched": True},
    {"id": 2, "title": "The Matrix", "director": "The Wachowskis", "year": 1999, "watched": True}
]

def make_error(status_text, message, status_code):
    return jsonify({
        "error": status_text,
        "message": message
    }), status_code

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies", methods=["GET"])
def list_movies():
    return jsonify(movies)

@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json() or {}

    # 1) Presence validation
    required_fields = ["title", "director", "year", "watched"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return make_error(
            "Bad Request",
            f"Missing required field(s): {', '.join(missing)}",
            400
        )

    # 2) Type validation
    if not isinstance(data.get("title"), str):
        return make_error("Bad Request", "Field 'title' must be a string.", 400)

    if not isinstance(data.get("director"), str):
        return make_error("Bad Request", "Field 'director' must be a string.", 400)

    if not isinstance(data.get("year"), int):
        return make_error("Bad Request", "Field 'year' must be an integer.", 400)

    if not isinstance(data.get("watched"), bool):
        return make_error("Bad Request", "Field 'watched' must be a boolean.", 400)

    # 3) If we get here, input is valid → create movie
    new_id = max(movie["id"] for movie in movies) + 1

    new_movie = {
        "id": new_id,
        "title": data.get("title"),
        "director": data.get("director"),
        "year": data.get("year"),
        "watched": data.get("watched", False)
    }

    movies.append(new_movie)
    return jsonify(new_movie), 201

@app.route("/echo-json", methods=["POST"])
def echo_json():
    print("Content-Type header:", request.headers.get("Content-Type"))
    data = request.get_json()
    return jsonify(data)

@app.route("/ping", methods=["GET"])
def ping():
    return "Server is running"

@app.route("/ping-write", methods=["POST"])
def ping_write():
    return "Write ping received"

if __name__ == "__main__":
    print(">>> ABOUT TO RUN FLASK APP <<<")
    app.run(debug=True)
