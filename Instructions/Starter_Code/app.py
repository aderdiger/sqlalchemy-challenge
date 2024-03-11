# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
# base = automap_base()
metadata = MetaData(bind=engine)
metadata.reflect()
print(metadata.tables)

# Use the Base class to reflect the database tables
# base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and the station class to a variable called `Station`
# Measurement = base.classes.measurement
# Station = base.classes.station

# The session is created and closed for each API route query instead of opening the session here and closing it at the end
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)




# #################################################
# # Flask Routes
# #################################################

# Home page with all available API routes
@app.route("/")
def welcome():
    
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation | Returns jsonified precipitation(in) data for the last year<br/>"
        f"/api/v1.0/stations | Returns jsonified list of stations<br/>"
        f"/api/v1.0/tobs | Returns jsonified temp(F) data for the last year<br/>"
        f"/api/v1.0/startdate | returns min, max, and avg temp(F) after this date. startdate must be in format yyyy/mm/dd<br/>"
        f"/api/v1.0/startdate/enddate | returns min, max, and avg temp for this range. startdate and enddate must be in format yyyy/mm/dd"
    )
    
# Page with precipitation data
@app.route("/api/v1.0/precipitation")
def prcpdata():
    
    """Return a list of all precipitation data for the last year"""
    # Query for most recent year of precipitation data
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                      filter(Measurement.date >= dt.datetime(2016, 8, 23)).\
                      order_by(Measurement.date).all()

    session.close()

    # Create empty list
    prcp_data = []  	
	
    # Append each datapoint to the list
    for date, prcp in results:
        prcp_data.append({date: prcp})	
	
    # Return jsonified precipitation data
    return jsonify(prcp_data)
	

# Page with station data    
@app.route("/api/v1.0/stations")
def stationinfo():
    
    """Return a list of all station data"""
    # Query for all stations and their ID
    session = Session(engine)
    results = session.query(Station.station, Station.id).all()
    session.close()

    # Create empty list
    station_data = []
	
    # Append each datapoint to the list
    for station, station_id in results:
        station_data.append({'station': station, 'id': station_id})

    # Return jsonified precipitation data
    return jsonify(station_data)
    

# Page with temperature data
@app.route("/api/v1.0/tobs")
def tobsdata():

    """Return a list of all temperature data for the last year"""
    # Query for all temperature data within the last year
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                           filter(Measurement.date >= dt.datetime(2016, 8, 23)).\
                           order_by(Measurement.date).all()
    session.close()

    # Create empty list
    tobs_data = []

    # Append each datapoint to the list
    for date, tobs in results:
        tobs_data.append({'date': date, 'temperature': tobs})

    # Return jsonified temperature data
    return jsonify(tobs_data)


# Page for finding temperature data after the given start date    
@app.route("/api/v1.0/<start>")
def startinfo(start):

    """Return a list of the temperature statistics after the provided date"""
    
    session = Session(engine)

    # Define functions for min, max, and avg
    sel = [Measurement.station, 
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    
    # Query for all temperatures after the provided start date
    temperature_stats = session.query(*sel).\
                        filter(Measurement.date >= start).all()	
    
    session.close() 

    # Create empty list     
    temp_stats_data = []
	
    # Append the statistics from the query to the list
    for min_temp, max_temp, avg_temp in temperature_stats:
        temp_stats_data.append({'start_date': start,
                                'min_temperature': min_temp,
                                'max_temperature': max_temp,
                                'avg_temperature': avg_temp})	

    # Return jsonified statistics
    return jsonify(temp_stats_data)
	

# Page for finding temperature data between the given dates
@app.route("/api/v1.0/<start>/<end>")
def startendinfo(start, end):

    """Return a list of the temperature statistics between the provided dates"""
    
    session = Session(engine)

    # Define functions for min, max, and avg
    sel = [Measurement.station, 
           func.min(Measurement.tobs), 
           func.max(Measurement.tobs), 
           func.avg(Measurement.tobs)]
    
    # Query for all temperatures between the provided dates
    temperature_stats_2 = session.query(*sel).\
                        filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).all()	
    
    session.close()

    # Create empty list   
    temp_stats_data_2 = []

    # Append the statistics from the query to the list
    for min_temp, max_temp, avg_temp in temperature_stats_2:
        temp_stats_data_2.append({'start_date': start,
                                'end_date': end,
                                'min_temperature': min_temp,
                                'max_temperature': max_temp,
                                'avg_temperature': avg_temp})	

    # Return jsonified statistics
    return jsonify(temp_stats_data_2)

# Debugging
if __name__ == '__main__':
    app.run(debug=True)