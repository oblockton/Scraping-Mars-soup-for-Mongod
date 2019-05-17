from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_flask")


@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_content = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_content)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_news():

    # Run the scrape function
    scrape_return = mars_scrape.scrape_mars()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, scrape_return, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
