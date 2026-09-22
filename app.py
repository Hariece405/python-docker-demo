from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book-flight", methods=["POST"])
def book_flight():
    origin = request.form.get("from")
    destination = request.form.get("to")
    departure = request.form.get("departure")
    return_date = request.form.get("return")
    passengers = request.form.get("passengers")
    travel_class = request.form.get("class")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flight Search</title>
        <style>
            body {{
                font-family: Arial;
                background: #eef4f8;
                padding: 40px;
            }}

            .result {{
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,.15);
            }}

            h1 {{
                color: #0077cc;
            }}
        </style>
    </head>

    <body>
        <div class="result">

            <h1>✈️ Flight Search</h1>

            <p><strong>From:</strong> {origin}</p>
            <p><strong>To:</strong> {destination}</p>
            <p><strong>Departure:</strong> {departure}</p>
            <p><strong>Return:</strong> {return_date or "One way"}</p>
            <p><strong>Passengers:</strong> {passengers}</p>
            <p><strong>Class:</strong> {travel_class}</p>

            <hr>

            <h2>Search received successfully ✅</h2>

            <a href="/">Search another flight</a>

        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
