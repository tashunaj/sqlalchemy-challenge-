import pandas as pd
import numpy as np
from flask import Flask, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine= create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request from 'Home' page.....")
    return(
        f"Welcome to the 'Home' page<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    annualprecp = session.query(measurement.date, masurement.prcp).\
                    filter(measurement.date >= year_ago).all()
    precp ={date: prcp for date, prcp in annualprecp}
    return jsonify(precp)


@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of all stations"""
    results = session.query(station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
   """Returns a list of the dates and temperature observations from a year from last data point"""
   year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

   annual_temps = session.query(measurement.tobs).\
                   filter(measurement.station == 'USC00519281').\
                   filter(measurement.date >= year_ago).all()

   temps = list(np.ravel(annual_temps))

   return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    return jsonify(results)
    session.close()
if __name__ == "__main__":
    app.run(debug=True)
