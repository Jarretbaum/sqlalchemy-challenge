#copying the code from the notebook over, unsure where the actual bulk code should be so its in both.


# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    station_data = [{"Station ID": station, "Station Name": name} for station, name in results]

    return jsonify(station_data)

# Temperature Observations route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results to a list of dictionaries
    tobs_data = [{"Date": date, "Temperature": tobs} for date, tobs in results]

    return jsonify(tobs_data)

# Start Date route
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Query the min, avg, and max temperatures from the start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Convert the query results to a list of dictionaries
    temperature_data = [{"Min Temperature": result[0], "Avg Temperature": result[1], "Max Temperature": result[2]} for result in results]

    return jsonify(temperature_data)

# Start and End Date route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Query the min, avg, and max temperatures from the start date to the end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert the query results to a list of dictionaries
    temperature_data = [{"Min Temperature": result[0], "Avg Temperature": result[1], "Max Temperature": result[2]} for result in results]

    return jsonify(temperature_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)