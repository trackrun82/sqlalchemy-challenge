import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    print("Server received request for 'welcome' page...")
    
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/*start: A date string in the format %Y-%m-%d<br/>"
        f"/api/v1.0/*start: A date string in the format %Y-%m-%d/*end: A date string in the format %Y-%m-%d<br/>"
        f"*Be sure to replace start and end dates with valid dates from 2010-01-01 to 2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and precipitation"""
    # Query Measurement for last year
    year_precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    
    session.close()

    # Create a dictionary using date as the key and prcp as the value
    all_precip = []
    for date, prcp in year_precip:
        precip_dict = {}
        precip_dict[date] = prcp
        all_precip.append(precip_dict)

    #Return the JSON representation of dictionary
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    stations = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures for most active station"""
    # Query the dates and temperature observations of the most active station for the last year of data
    station_temp = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    station_temps = list(np.ravel(station_temp))

    return jsonify(station_temps)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    print("Server received request for 'start' page...")
    
    session = Session(engine)

    temp_args = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    temp_list = list(np.ravel(temp_args))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):
    print("Server received request for 'start/end' page...")
    
    session = Session(engine)
   
    temp_args2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    temp_list2 = list(np.ravel(temp_args2))
    return jsonify(temp_list2)

if __name__ == '__main__':
    app.run(debug=True)    