# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
    """List all available api routes."""
    return (
        f"Available Routes:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link
    session = Session(engine)

    # Query precipitation 
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= str(year_ago)).all()
    all_prec_dates = []
    for date, inches in results:
        date_dict = {}
        date_dict['Date'] = date
        date_dict['prcp'] = inches
        all_prec_dates.append(date_dict)

    return jsonify(all_prec_dates)

@app.route("/api/v1.0/stations")
def stations():


@app.route("/api/v1.0/tobs")
def tobs():


@app.route("/api/v1.0/<start>")
def start_date():


@app.route("/api/v1.0/<start>/<end>")
def end_date():
    

if __name__ == '__main__':
    app.run(debug=True)