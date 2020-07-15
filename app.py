import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/chinook.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Invoices = Base.classes.invoices

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
        f"/api/v1.0/countries<br/>"
        f"/api/v1.0/invoice-totals"
    )


@app.route("/api/v1.0/countries")
def countries():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all countries"""
    # Query all countries
    countries = session.query(Invoices.BillingCountry).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    all_countries = list(np.ravel(countries))

    return jsonify(all_countries)


@app.route("/api/v1.0/invoice-totals")
def invoice_totals():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of invoice data including the name and total of countries"""
    # Query all invoices
    results = session.query(Invoices.BillingCountry, func.sum(Invoices.Total)).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_invoices
    all_invoices = []
    for BillingCountry, Total in results:
        invoice_dict = {}
        invoice_dict["BillingCountry"] = BillingCountry
        invoice_dict["Total"] = Total
        all_invoices.append(invoice_dict)

    return jsonify(all_invoices)


if __name__ == '__main__':
    app.run(debug=True)
