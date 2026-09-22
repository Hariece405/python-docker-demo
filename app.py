from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import uuid

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Demo flight database
FLIGHTS = [
    {
        "id": "AI101",
        "airline": "Air India",
        "from": "Hyderabad",
        "to": "Delhi",
        "departure": "08:30",
        "arrival": "10:45",
        "price": 5200
    },
    {
        "id": "6E205",
        "airline": "IndiGo",
        "from": "Hyderabad",
        "to": "Delhi",
        "departure": "11:15",
        "arrival": "13:30",
        "price": 4800
    },
    {
        "id": "UK810",
        "airline": "Vistara",
        "from": "Hyderabad",
        "to": "Mumbai",
        "departure": "14:00",
        "arrival": "15:40",
        "price": 4500
    },
    {
        "id": "6E401",
        "airline": "IndiGo",
        "from": "Mumbai",
        "to": "Bengaluru",
        "departure": "17:30",
        "arrival": "19:15",
        "price": 3900
    }
]

BOOKINGS = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()
    departure_date = request.form.get("departure_date", "").strip()
    passengers = request.form.get("passengers", "1")

    try:
        passengers = int(passengers)
    except ValueError:
        passengers = 1

    if passengers < 1 or passengers > 9:
        flash("Passengers must be between 1 and 9.")
        return redirect(url_for("home"))

    if not origin or not destination or not departure_date:
        flash("Please fill in all required fields.")
        return redirect(url_for("home"))

    try:
        selected_date = date.fromisoformat(departure_date)

        if selected_date < date.today():
            flash("Departure date cannot be in the past.")
            return redirect(url_for("home"))

    except ValueError:
        flash("Invalid departure date.")
        return redirect(url_for("home"))

    results = [
        flight for flight in FLIGHTS
        if flight["from"].lower() == origin.lower()
        and flight["to"].lower() == destination.lower()
    ]

    return render_template(
        "results.html",
        flights=results,
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        passengers=passengers
    )


@app.route("/book/<flight_id>", methods=["POST"])
def book(flight_id):
    flight = next(
        (f for f in FLIGHTS if f["id"] == flight_id),
        None
    )

    if not flight:
        flash("Flight not found.")
        return redirect(url_for("home"))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    departure_date = request.form.get("departure_date", "")
    passengers = request.form.get("passengers", "1")

    if not name or not email or not phone:
        flash("Please enter your name, email and phone number.")
        return redirect(url_for("home"))

    try:
        passengers = int(passengers)
        if passengers < 1 or passengers > 9:
            raise ValueError
    except ValueError:
        flash("Invalid passenger count.")
        return redirect(url_for("home"))

    booking_id = "BK-" + uuid.uuid4().hex[:8].upper()

    total_price = flight["price"] * passengers

    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "flight": flight,
        "name": name,
        "email": email,
        "phone": phone,
        "departure_date": departure_date,
        "passengers": passengers,
        "total_price": total_price
    }

    return render_template(
        "confirmation.html",
        booking=BOOKINGS[booking_id]
    )


if __name__ == "__main__":
    app.run(debug=True)
