######################################
#  Keivn Krause
#  Surfsup JSON
#  June 12, 2023
#
# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify



#################################################
# Database Setup to Connect To the hawaii.sqllite DB
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
        f"Temperature Information:    /api/v1.0/tobs <br>"
        f"Add a start date           /api/v1.0/precipenter/YYYY-MM-DD   <br>"
        f"Add a start and end date   /api/v1.0/precipenterse/YYYY-MM-DD/YYYY-MM-DD  <br>"
        "where YYYY-MM-DD = a valid start and end date"
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
# Query all Measurement    
    precipitation_data = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    
 #.order_by(Measurement.date)

    session.close()

    # Convert list of tuples into normal list
    top_one_year_precip = list(np.ravel(precipitation_data))

    return jsonify(top_one_year_precip)
#    return "Hi - You are at the Precipitation Page"
# End of Precipitation
#
#
#
#                        I  L E F T   R I G H T    H E R E

#######################################################
### The station route was entered                     #
#######################################################
@app.route("/api/v1.0/stations")
def Stations():
    session = Session(engine)
    station_data = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    station_list = list(np.ravel(station_data))
    session.close()

    return jsonify(station_list)

#    return "Hi - You are at the Stations Page"
    

# End of Stations
#
#######################################################
### The temperature route was entered                 #
#######################################################
@app.route("/api/v1.0/tobs")
def Temperature():
    session = Session(engine)


# Query all Measurement    
    tobs_data = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-23').all()
    
 #.ORDER_by(Measurement.date)

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_data))

    return jsonify(tobs_list)
#    return "Hi - You are at the Temperature Page"
# End of Stations

###########################################################################################
#
#            I N T E R A C T I V E     S E C T I O N
#
###########################################################################################

############################################################################
### The precipitation route with date  was entered  by the user            #
###########################################################################
@app.route("/api/v1.0/precipenter/<dtentry>")
def precip_pass_dt(dtentry):
    
    session = Session(engine)
    query = "SELECT MIN(tobs), MAX(tobs),AVG(tobs)  FROM measurement where DATE(date) >= '%s'" %dtentry
    mma_data = engine.execute(query)
    mma_data_df = pd.DataFrame(mma_data,columns =['min', 'max','avg'])
    mma_data_json = mma_data_df.to_json(orient = 'records')

    session.close()

    return mma_data_json

#

#######################################################
### The precipitation route with start and end date  was entered               #
#######################################################
@app.route("/api/v1.0/precipenterse/<dtstart>/<dtend>")
def precip_passse_dt(dtstart,dtend):

    session = Session(engine)
    btwncls = f"'{dtstart}' AND '{dtend}'"
    query = "SELECT MIN(tobs), MAX(tobs),AVG(tobs)  FROM measurement where DATE(date) BETWEEN %s" %btwncls
    mma_data_2 = engine.execute(query)
    mma_data_2_df = pd.DataFrame(mma_data_2,columns =['min', 'max','avg'])
    mma_data_2_json = mma_data_2_df.to_json(orient = 'records')
    session.close()


    return mma_data_2_json

#
if __name__ == "__main__":
    app.run(debug=True)