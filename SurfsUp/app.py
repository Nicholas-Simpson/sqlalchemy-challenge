# Import the dependencies.
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite",echo=False)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Set required variables needed for the session query
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # query session using filter information to obtain results
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= str(year_ago)).all()
    
    # close Session link
    session.close()

    # Take results and turn into a json format for web use
    all_prec_dates = {date:prcp for date, prcp in results}
    return jsonify(all_prec_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query session using filter information to obtain results
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results))

    # close Session link
    session.close()

    # Take results and turn into a json format for web use
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Set required variables needed for the session query
    active_station = 'USC00519281'
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # query session using filter information to obtain results
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == active_station).\
            filter(Measurement.date >= year_ago).all()
    active_station = list(np.ravel(results))

    # close Session link
    session.close()

    # Take results and turn into a json format for web use
    return jsonify(active_station)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start = None, end = None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Set required variables needed for the session query
    select = [func.min(Measurement.tobs),func.max(Measurement.tobs),
              func.avg(Measurement.tobs)]
    
    # Set up an if statement to account for the route user input when end date is not present
    if not end:
        # Set up the string input into an actual date/time format
        start = dt.datetime.strptime(start,'%Y-%m-%d')
        # query session using filter information to obtain results
        results = session.query(*select).filter(Measurement.date >= start).all()
        # close Session link
        session.close()
        # Take results and turn into a json format for web use
        query_results = list(np.ravel(results))
        return jsonify(query_results)
    
    # Set up the string input into an actual date/time format
    start = dt.datetime.strptime(start,'%Y-%m-%d')
    end = dt.datetime.strptime(end,'%Y-%m-%d')
    # query session using filter information to obtain results
    results = session.query(*select).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # close Session link
    session.close()
    # Take results and turn into a json format for web use
    query_results = list(np.ravel(results))
    return jsonify(query_results)


if __name__ == '__main__':
    app.run(debug=True)