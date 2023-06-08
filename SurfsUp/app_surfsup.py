######################################
#  Keivn Krause
#  Surfsup JSON
#  June 12, 2023
# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################

# Main Route
app = Flask(__name__)
@app.route("/")
def home():
    return (
        f"Welcome to the SurfsUp Weather and Weather Station Data <br>"
        f"Here are your available routes to choose from: <br>"
        f"Precipitation Information:  /api/v1.0/precipitation <br>"
        f"Station Information:        /api/v1.0/stations <br>"
        f"Temperature Information:    /api/v1.0/tobs"
    )
#
#################################################
#                    Flask Routes               #
#################################################
#
#
#
#######################################################
### The precipitation route was entered               #
#######################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all Measurement
    #query = text("SELECT DATE(date) as date, prcp FROM measurement where DATE(date) > '2016-08-23' and prcp <> 'None' ORDER BY date")
    precipitation_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    top_one_year_precip = list(np.ravel(precipitation_data))

    return jsonify(top_one_year_precip)
#    return "Hi - You are at the Precipitation Page"
# End of Precipitation
#
#
#
                        I  L E F T   R I G H T    H E R E

#######################################################
### The station route was entered                     #
#######################################################
@app.route("/api/v1.0/stations")
def Stations():
    return "Hi - You are at the Stations Page"
# End of Stations
#
#######################################################
### The temperature route was entered                 #
#######################################################
@app.route("/api/v1.0/tobs")
def Temperature():
    return "Hi - You are at the Temperature Page"
# End of Stations
#
if __name__ == "__main__":
    app.run(debug=True)