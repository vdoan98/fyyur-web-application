#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func, case, or_
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# DONE: connect to a local postgresql database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:DataPass98@localhost:5432/fyyur'

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:DataPass98@localhost:5432/fyyur'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#Notes on data model
#Venue and Artist have location_id stored in Location table.
#Genre table store all available genre
#VenueGenre link Venue with Genre
#ArtistGenre link Artist with Genre
#Show contains artist_id and venue_id linking the table to Artist and Venue

#For Venue and Artist, the following information are required:
#Name, city, state, image_link, facebook_link. Constraints on form to create
#new venue and artist require that venue and artist have genres.


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #city = db.Column(db.String(120), nullable=False)
    #state = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False) #For now
    facebook_link = db.Column(db.String(120), nullable=True)

    # [DONE]: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)
    genre = db.relationship('VenueGenre', backref='venue', lazy=True)




class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    #city = db.Column(db.String(120), nullable=True)
    #state = db.Column(db.String(120), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)

    # [DONE]: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)
    genre = db.relationship('ArtistGenre', backref='artist', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    venue = db.relationship('Venue', backref='location', lazy=True)
    artist = db.relationship('Artist', backref='location', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    artist = db.relationship('ArtistGenre', backref='genre', lazy=True)
    venue = db.relationship('VenueGenre', backref='genre', lazy=True)

class ArtistGenre(db.Model):
    __tablename__ = 'artistGenre'
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

class VenueGenre(db.Model):
    __tablename__ = 'venueGenre'
    id = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
# [DONE] Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

#Look for location in Location table. If exists, return id. If not, create new
#location and return id
def get_or_create_loc(city, state, data_type):
    location_id = 0
    # location_query = db.session.query(Location.id, Location.city, Location.state).join(Venue, Location.id == Venue.location_id).filter(or_(Location.city.ilike(city), Location.city.ilike(city + " "))).filter(or_(Location.state.ilike(state), Location.state.ilike(state + " "))).all()
    # if data_type == "venue":
    #     location_query = db.session.query(Location.id, Location.city, Location.state)\
    #     .join(Venue, Location.id == Venue.location_id)\
    #     .filter(_or(Location.city.ilike(city), Location.city.ilike(city + " ")))\
    #     .filter(_or(Location.state.ilike(state), Location.state.ilike(state + " "))).all()
    # elif data_type == "artist":
    #     location_query = db.session.query(Location.id, Location.city, Location.state)\
    #     .join(Artist, Location.id == Artist.location_id)\
    #     .filter(_or(Location.city.ilike(city), Location.city.ilike(city + " ")))\
    #     .filter(_or(Location.state.ilke(state), Location.state.ilke(state + " ")))\
    #     .all()


    if data_type == "venue":
        location_query = db.session.query(Location.id, Location.city, Location.state)\
        .join(Venue, Location.id == Venue.location_id, isouter=True)\
        .filter(Location.city.ilike(city.rstrip(" ").lstrip(" ")), Location.state == state).all()

    elif data_type == "artist":
        location_query = db.session.query(Location.id, Location.city, Location.state)\
        .join(Artist, Location.id == Artist.location_id, isouter=True)\
        .filter(Location.city.ilike(city.rstrip(" ").lstrip(" ")), Location.state == state).all()

    #or_((Location.city.ilike(city), Location.state.ilike(city )), (Location.city.ilike(city), Location.city.ilike(city))))
    if (len(location_query) <= 0):
        print("Create New")
        new_location = Location(city=city.rstrip(" ").lstrip(" "), state=state)
        db.session.add(new_location)
        db.session.flush()
        location_id = new_location.id
        db.session.commit()
    else:
        print("Found in table")
        location_id = location_query[0].id

    return location_id

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues = []
  artists = []

  recent_venue = db.session.query(Venue.id, Venue.name).order_by(Venue.id.desc()).limit(10).all()

  recent_artist = db.session.query(Artist.id, Artist.name).order_by(Artist.id.desc()).limit(10).all()

  for i in recent_venue:
      venue = {}
      venue['id'] = i.id
      venue['name'] = i.name
      venues.append(venue)

  for i in recent_artist:
      artist = {}
      artist['id'] = i.id
      artist['name'] = i.name
      artists.append(artist)

  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # [DONE]: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

  locations = []
  data = []

  #get venue information
  try:
      join_table = db.session.query(Venue, Location).join(Venue, Venue.location_id == Location.id).with_entities(Venue.id.label("venue_id"), Venue.name, Location.id.label("location_id"), Location.city, Location.state).all()
      #count upcoming show
      join_show = db.session.query(Venue.id.label('venue_id'), func.count(Show.start_time).label('upcoming_shows')).join(Venue, Venue.id == Show.venue_id).filter(Show.start_time >= datetime.now()).group_by(Venue.id).all()

      #get all unique state + city combination
      for i in join_table:
          if (i.city, i.state) not in locations:
              locations.append((i.city, i.state))

      #populate list of unique state + city combination
      for (i, j) in locations:
          new_loc = {}
          new_loc["city"] = i
          new_loc["state"] = j
          new_loc["venues"] = []
          data.append(new_loc)

      #fill in information for venues sort by state + city
      for i in join_table:
          for k in data:
              if i.city == k["city"] and i.state == k["state"]:
                  new_venue = {}
                  new_venue["id"] = i.venue_id
                  new_venue["name"] = i.name
                  new_venue["num_upcoming_shows"] = 0
                  for j in join_show:
                      if j.venue_id == i.venue_id:
                          new_venue["num_upcoming_shows"] = j.upcoming_shows

                  k["venues"].append(new_venue)
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # [DONE]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  try:
      search_term=request.form.get('search_term', '')

      response = {
        "count" : 0,
        "data": []
      }

      count_case = case(
          [
              (Show.start_time >= datetime.now(), 1),
              (Show.start_time < datetime.now(), 0)
          ]
      )

      # Query search for venue name, city or state using keyword
      search_query = db.session.query(Location.id, Venue.id.label('venue_id'), Venue.name, func.sum(count_case).label('upcoming_shows'))\
      .join(Venue, Location.id == Venue.location_id)\
      .join(Show, Venue.id == Show.venue_id, isouter=True)\
      .filter(or_(Location.state.ilike('%' + search_term + '%'), Location.city.ilike('%' + search_term + '%'), Venue.name.ilike('%' + search_term + '%')))\
      .group_by(Location.id,Venue.id, Venue.name).all()

      # If query return 0, then look for keyword in city and name.
      #"San Francisco, CA" works. "San Francisco CA" will not work as it will
      #split on the comma
      if (len(search_query) == 0):
          city = search_term.split(",")[0].lstrip(" ")
          city = city.rstrip(" ")
          print(city)
          state = search_term.split(",")[1].lstrip(" ")
          state = state.rstrip(" ")
          print(state)
          search_query = db.session.query(Location.id, Venue.id.label('venue_id'), Venue.name, func.sum(count_case).label('upcoming_shows'))\
          .join(Venue, Location.id == Venue.location_id)\
          .join(Show, Venue.id == Show.venue_id, isouter=True)\
          .filter(Location.state.ilike('%' + state + '%'), Location.city.ilike('%' + city + '%'))\
          .group_by(Location.id,Venue.id, Venue.name).all()



      for i in search_query:
          response["count"] += 1
          next = {}
          next["id"] = i.venue_id
          next["name"] = i.name
          if (i.upcoming_shows == None):
              next["num_upcoming_shows"] = 0
          else:
              next["num_upcoming_shows"] = i.upcoming_shows
          response["data"].append(next)

  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # [DONE]: replace with real venue data from the venues table, using venue_id


  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }

  all_venues = []
  try:
      join_table = db.session.query(Venue, Location).join(Venue, Venue.location_id == Location.id).order_by(Venue.id).all()
      #count upcoming show
      show_case = case (
          [
              (Show.start_time >= datetime.now(), 0),
              (Show.start_time < datetime.now(), 1)
          ]
      )
      join_upcoming_show = db.session.query(Venue.id.label('venue_id'), Show.start_time, show_case.label('has_passed'), Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link.label("artist_link")).join(Venue, Venue.id == Show.venue_id).join(Artist, Show.artist_id == Artist.id).order_by(Venue.id).all()

      genre_query = db.session.query(VenueGenre.venue_id, Genre.name).join(VenueGenre, VenueGenre.genre_id == Genre.id).all()


      for (i,j) in join_table:
          data = {}
          data["id"] = i.id
          data["name"] = i.name
          data["genres"] = []
          for k in genre_query:
              if k.venue_id == i.id:
                  data["genres"].append(k.name)
          data["address"] = i.address
          data["city"] = j.city
          data["state"] = j.state
          data["phone"] = i.phone
          if (i.website != None):
              data["website"] = i.website #can be empty
          if (i.facebook_link != None):
              data["facebook_link"] = i.facebook_link
              data["seeking_talent"] = i.seeking_talent
          if (i.seeking_talent == True):
              data["seeking_description"] = i.seeking_description#can be empty
          data["image_link"] = i.image_link
          data["past_shows"] = []
          data["upcoming_shows"] = []
          data["past_shows_count"] = 0
          data["upcoming_shows_count"] = 0
          all_venues.append(data)

      for i in all_venues:
          for k in join_upcoming_show:
              if(k.venue_id == i["id"] and k.has_passed == 1):
                  a_show = {}
                  a_show["artist_id"] = k.artist_id
                  a_show["artist_name"] = k.artist_name
                  a_show["artist_image_link"] = k.artist_link
                  #a_show["start_time"] = "2019-05-21T21:30:00.000Z"
                  a_show["start_time"] = k.start_time.strftime("%Y-%m-%d %H:%M:%S")

                  i["past_shows"].append(a_show)
                  i["past_shows_count"] += 1
              elif k.venue_id == i["id"]:
                  a_show = {}
                  a_show["artist_id"] = k.artist_id
                  a_show["artist_name"] = k.artist_name
                  a_show["artist_image_link"] = k.artist_link
                  #a_show["start_time"] = "2019-05-21T21:30:00.000Z"
                  a_show["start_time"] = k.start_time.strftime("%Y-%m-%d %H:%M:%S")

                  i["upcoming_shows"].append(a_show)
                  i["upcoming_shows_count"] += 1


      data = list(filter(lambda d: d['id'] == venue_id, all_venues))[0]
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # [DONE]: insert form data as a new Venue record in the db, instead
  # [DONE]: modify data to be the data object returned from db insertion

  #data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }]

  form = VenueForm(request.form)
  #print(request.form['genres'])
  #print(request.form['name'])
  if form.validate_on_submit():
      try:
          error = False
          name = request.form['name']
          genres = request.form.getlist('genres')
          address = request.form['address']
          city = request.form['city']
          state = request.form['state']
          phone = None
          if 'phone' in request.form:
              phone = request.form['phone']
          website = None
          if 'website' in request.form:
              website = request.form['website']
          facebook_link = request.form['facebook_link']
          image_link = request.form['image_link']
          seeking_talent = False
          if 'seeking_talent' in request.form:
              seeking_talent = True
          seeking_description = " "
          if 'seeking_description' in request.form:
              seeking_description = request.form['seeking_description']
          image_link = request.form['image_link']


        #if location does not exist in Location based on city and state,
        #create new record, return id then insert to table
          location_id = get_or_create_loc(city, state, data_type="venue")


          new_venue = Venue(name = name, location_id = location_id, phone = phone , image_link = image_link, facebook_link = facebook_link, address = address, website = website , seeking_talent = seeking_talent, seeking_description = seeking_description)
          db.session.add(new_venue)
          db.session.flush()

          #Insert VenueGenre based on venue_id and genre from form options.
          for i in genres:
              genres_query = db.session.query(Genre.id, Genre.name).filter(Genre.name.ilike(i)).all()[0]
              newVenueGenre = VenueGenre(venue_id = new_venue.id , genre_id = genres_query.id)
              #VenueGenre.insert(newVenueGenre)
              db.session.add(newVenueGenre)
          db.session.commit()

          #location_query = db.session.query(Location.id, Location.city, Location.state).join(Venue, Location.id == Venue.location_id).filter(Location.city.ilike(city)).filter(Location.state.ilike(state)).limit(1).all()[0]

          #new_venue = Venue(name = name, location_id = location_query.id, phone = phone , image_link = image_link, facebook_link = facebook_link, address = address, website = website , seeking_talent = seeking_talent, seeking_description = seeking_description)

          #website

          flash('Venue ' + request.form['name'] + ' was successfully listed!')
      except:
          db.session.rollback()
      finally:
          db.session.close()
          index()
  else:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      flash(request.form.getlist('genres'))


  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g.,
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # [DONE]: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: [DONE] Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage


  #1. Delete Genre from Genre table
  #2. Delete Show from Show table
  #3. Delete Venue
  error = False

  try:
      delete_genre = db.session.query(VenueGenre).filter_by(venue_id=venue_id).delete()
      delete_show = db.session.query(Show).filter_by(venue_id=venue_id).delete()
      delete_venue = db.session.query(Venue).filter_by(id=venue_id).delete()

      db.session.commit()


  except Exception as e:
      error = True
      print(f'Error ==> {e}')
      db.session.rollback()
  finally:
      db.session.close()
      if error:
          flash(f'An error occurred. Venue {venue_id} could not be deleted.')
          abort(400)
      else:
           flash('Venue was successfully deleted!')

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # [DONE]: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  data = []

  try:
      artist_query = db.session.query(Artist.id, Artist.name).order_by(Artist.id).all()

      for i in artist_query:
          new_artist = {}
          new_artist["id"] = i.id
          new_artist["name"] = i.name
          data.append(new_artist)
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # [DONE]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  try:
      search_term=request.form.get('search_term', '')
      response={
          "count": 0,
          "data": []
      }
      count_case = case(
          [
              (Show.start_time >= datetime.now(),1),
              (Show.start_time < datetime.now(), 0)
          ]
      )

      # artist_query = db.session.query(Artist.id, Artist.name, func.sum(count_case).label("num_shows")).join(Artist, Artist.id == Show.artist_id).filter(Artist.name.ilike('%' + search_term + '%')).group_by(Artist.id, Artist.name).order_by(Artist.id).all()

      artist_query = db.session.query(Artist.id.label("id"), Artist.name.label("name"), func.sum(count_case).label("num_shows")).join(Location, Location.id == Artist.location_id).join(Show, Artist.id == Show.artist_id).filter(or_(Location.state.ilike('%' + search_term + '%'), Location.city.ilike('%' + search_term + '%'), Artist.name.ilike('%' + search_term + '%'))).group_by(Artist.id, Artist.name).order_by(Artist.id).all()

      if (len(artist_query) == 0):
          city = search_term.split(",")[0].lstrip(" ")
          city = city.rstrip(" ")
          print(city)
          state = search_term.split(",")[1].lstrip(" ")
          state = state.rstrip(" ")
          print(state)
          artist_query = db.session.query(Artist.id.label("id"), Artist.name.label("name"), func.sum(count_case).label("num_shows")).join(Location, Location.id == Artist.location_id).join(Show, Artist.id == Show.artist_id).filter(Location.city.ilike('%' + city + '%'), Location.state.ilike('%' + state + '%')).group_by(Artist.id, Artist.name).order_by(Artist.id).all()




      for i in artist_query:
          response["count"] += 1
          new_artist = {}
          new_artist["id"] = i.id
          new_artist["name"] = i.name
          new_artist["num_upcoming_shows"] = i.num_shows
          response["data"].append(new_artist)
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # [DONE]: replace with real venue data from the venues table, using venue_id


  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }


  all_artist = []

  try:
      join_table = db.session.query(Artist, Location).join(Artist, Artist.location_id == Location.id).order_by(Artist.id).all()

      print(join_table[0])
      #count upcoming show
      show_case = case (
          [
              (Show.start_time >= datetime.now(), 0),
              (Show.start_time < datetime.now(), 1)
          ]
      )
      join_upcoming_show = db.session.query(Artist.id.label('artist_id'), Show.start_time, show_case.label('has_passed'), Venue.id.label("venue_id"), Venue.name.label("venue_name"), Venue.image_link.label("venue_link"),Artist.name.label("artist_name")).join(Artist, Artist.id == Show.artist_id).join(Venue, Show.venue_id == Venue.id).order_by(Artist.id).all()

      genre_query = db.session.query(ArtistGenre.artist_id, Genre.name).join(ArtistGenre, ArtistGenre.genre_id == Genre.id).all()


      for (i,j) in join_table:
          data = {}
          data["id"] = i.id
          data["name"] = i.name
          data["genres"] = []
          for k in genre_query:
              if k.artist_id == i.id:
                  data["genres"].append(k.name)
          data["city"] = j.city
          data["state"] = j.state
          data["phone"] = i.phone
          if (i.website != None):
              data["website"] = i.website #can be empty
          if (i.facebook_link != None):
              data["facebook_link"] = i.facebook_link
              data["seeking_venue"] = i.seeking_venue
          if (i.seeking_venue == True):
              data["seeking_description"] = i.seeking_description#can be empty
          data["image_link"] = i.image_link
          data["past_shows"] = []
          data["upcoming_shows"] = []
          data["past_shows_count"] = 0
          data["upcoming_shows_count"] = 0
          all_artist.append(data)

      for i in all_artist:
          for k in join_upcoming_show:
              if(k.artist_id == i["id"] and k.has_passed == 1):
                  a_show = {}
                  a_show["venue_id"] = k.venue_id
                  a_show["venue_name"] = k.venue_name
                  a_show["venue_image_link"] = k.venue_link
                  #a_show["start_time"] = "2019-05-21T21:30:00.000Z"
                  a_show["start_time"] = k.start_time.strftime("%Y-%m-%d %H:%M:%S")

                  i["past_shows"].append(a_show)
                  i["past_shows_count"] += 1
              elif k.artist_id == i["id"]:
                  a_show = {}
                  a_show["venue_id"] = k.venue_id
                  a_show["venue_name"] = k.venue_name
                  a_show["venue_image_link"] = k.venue_link
                  #a_show["start_time"] = "2019-05-21T21:30:00.000Z"
                  a_show["start_time"] = k.start_time.strftime("%Y-%m-%d %H:%M:%S")

                  i["upcoming_shows"].append(a_show)
                  i["upcoming_shows_count"] += 1
  except:
      db.session.rollback()
  finally:
      db.session.close()

  data = list(filter(lambda d: d['id'] == artist_id, all_artist))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()


  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # [DONE]: populate form with fields from artist with ID <artist_id>
  try:
      artist = {}
      artist_query = db.session.query(Artist, Location).join(Artist, Artist.location_id == Location.id)\
      .filter(Artist.id == artist_id).limit(1).all()

      for (i,j) in artist_query:
          artist['id'] = i.id
          artist['name'] = i.name
          artist['genres'] = []
          artist['city'] = j.city
          artist['state'] = j.state
          artist['phone'] = 'xxx-xxx-xxxx'
          if i.phone != None:
              artist['phone'] = i.phone
          artist['website'] = 'https://'
          if i.website != None:
              artist['website'] = i.website
          artist['facebook_link'] = i.facebook_link
          artist['seeking_venue'] = False
          artist['seeking_description'] = ' '
          if i.seeking_venue == True:
              artist['seeking_venue'] = True
              artist['seeking_description'] = i.seeking_description
          artist['image_link'] = i.image_link
  except:
      db.session.rollback()
  finally:
      db.session.close()


  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # [DONE]: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes


  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  new_artist_id = artist_id
  form = ArtistForm(request.form)
  # 1. Grab Venue on id
  if form.validate_on_submit():

      try:

          artist = db.session.query(Artist).filter(Artist.id == new_artist_id).all()[0]

          genres_delete = db.session.query(ArtistGenre)\
          .filter(ArtistGenre.artist_id == new_artist_id).delete()


          genres = request.form.getlist('genres')

          for i in genres:
              genres_query = db.session.query(Genre.id, Genre.name).filter(Genre.name.ilike(i)).all()[0]
              newArtistGenre = ArtistGenre(artist_id = new_artist_id, genre_id = genres_query.id)
              #VenueGenre.insert(newVenueGenre)
              db.session.add(newArtistGenre)

          city = request.form['city']
          state = request.form['state']
          location_id = get_or_create_loc(city, state, data_type="artist")
          print(location_id)

          #edit data
          error = False
          artist.name = request.form['name']
          artist.location_id = location_id
          artist.phone = None
          if 'phone' in request.form:
              artist.phone = request.form['phone']
          artist.website = None
          if 'website' in request.form:
              artist.website = request.form['website']
          artist.facebook_link = request.form['facebook_link']
          artist.image_link = request.form['image_link']
          artist.seeking_venue = False
          if 'seeking_venue' in request.form:
              artist.seeking_venue = True
          artist.seeking_description = None
          if 'seeking_description' in request.form:
              artist.seeking_description = request.form['seeking_description']
          artist.image_link = request.form['image_link']
          db.session.commit()

      except:
          db.session.rollback()
      finally:
          db.session.close()



      flash('Artist ' + request.form['name'] + ' was successfully updated!')
  else:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
      flash(request.form.getlist('genres'))



  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # [DONE]: populate form with values from venue with ID <venue_id>
  venue = {}
  try:

      venue_query = db.session.query(Venue, Location).join(Venue, Venue.location_id == Location.id)\
      .filter(Venue.id == venue_id).limit(1).all()

      for (i,j) in venue_query:
          venue['id'] = i.id
          venue['name'] = i.name
          venue['genres'] = []
          venue['address'] = i.address
          venue['city'] = j.city
          venue['state'] = j.state
          venue['phone'] = 'xxx-xxx-xxxx'
          if i.phone != None:
              venue['phone'] = i.phone
          venue['website'] = 'https://'
          if i.website != None:
              venue['website'] = i.website
          venue['facebook_link'] = i.facebook_link
          venue['seeking_talent'] = False
          venue['seeking_description'] = ' '
          if i.seeking_talent == True:
              venue['seeking_talent'] = True
              venue['seeking_description'] = i.seeking_description
          venue['image_link'] = i.image_link

      genre_query = db.session.query(Venue.id, VenueGenre.genre_id, Genre.name)\
      .join(Venue, Venue.id == VenueGenre.venue_id)\
      .join(Genre, VenueGenre.genre_id == Genre.id)\
      .filter(Venue.id == venue_id).all()

      for i in genre_query:
          venue['genres'].append(i.name)
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # [DONE]: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  new_venue_id = venue_id
  form = VenueForm(request.form)
  # 1. Grab Venue on id
  if form.validate_on_submit():
      try:
          venue = db.session.query(Venue).filter(Venue.id == new_venue_id).all()[0]

          #2. Drop genre records. Create new
          genres_delete = db.session.query(VenueGenre)\
          .filter(VenueGenre.venue_id == new_venue_id).delete()

          genres = request.form.getlist('genres')
          for i in genres:
              genres_query = db.session.query(Genre.id, Genre.name).filter(Genre.name.ilike(i)).all()[0]
              newVenueGenre = VenueGenre(venue_id = new_venue_id, genre_id = genres_query.id)
              #VenueGenre.insert(newVenueGenre)
              db.session.add(newVenueGenre)

          #3. Change Location record
          #if location does not exist in Location based on city and state,
          #create new record, return id then insert to table
          city = request.form['city']
          state = request.form['state']
          location_id = get_or_create_loc(city, state, data_type="venue")
          print(location_id)

          #edit data
          error = False
          venue.name = request.form['name']
          venue.address = request.form['address']
          venue.location_id = location_id
          venue.phone = None
          if 'phone' in request.form:
              venue.phone = request.form['phone']
          venue.website = None
          if 'website' in request.form:
              venue.website = request.form['website']
          venue.facebook_link = request.form['facebook_link']
          venue.image_link = request.form['image_link']
          venue.seeking_talent = False
          if 'seeking_talent' in request.form:
              venue.seeking_talent = True
          venue.seeking_description = None
          if 'seeking_description' in request.form:
              venue.seeking_description = request.form['seeking_description']
          venue.image_link = request.form['image_link']



                #4. Update Venue

          db.session.commit()
      except:
          db.session.rollback()
      finally:
          db.session.close()


      flash('Venue ' + request.form['name'] + ' was successfully updated!')
  else:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
      flash(request.form.getlist('genres'))


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():

  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # [DONE]: insert form data as a new Venue record in the db, instead
  # [DONE]: modify data to be the data object returned from db insertion


  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }

  form = ArtistForm(request.form)

  #print(request.form['genres'])
  #print(request.form['name'])
  if form.validate_on_submit():
      try:
          error = False
          name = request.form['name']
          genres = request.form.getlist('genres')
          city = request.form['city']
          state = request.form['state']
          phone = None
          if 'phone' in request.form :
              phone = request.form['phone']
          website = None
          if 'website' in request.form:
              website = request.form['website']
          facebook_link = request.form['facebook_link']
          image_link = request.form['image_link']
          seeking_venue = False
          if 'seeking_venue' in request.form:
              seeking_venue = True
          seeking_description = ''
          if 'seeking_description' in request.form:
              seeking_description = request.form['seeking_description']


        #if location does not exist in Location based on city and state,
        #create new record, return id then insert to table
          location_id = get_or_create_loc(city, state, data_type="artist")


          new_artist = Artist(name = name, location_id = location_id, phone = phone , image_link = image_link, facebook_link = facebook_link, website = website , seeking_venue = seeking_venue, seeking_description = seeking_description)
          db.session.add(new_artist)
          db.session.flush()

          for i in genres:
              genres_query = db.session.query(Genre.id, Genre.name).filter(Genre.name.ilike(i)).all()[0]
              newArtistGenre = ArtistGenre(artist_id = new_artist.id , genre_id = genres_query.id)
              #VenueGenre.insert(newVenueGenre)
              db.session.add(newArtistGenre)

          db.session.commit()
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
      except:
          db.session.rollback()
      finally:
          db.session.close()
          index()

  else:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      flash(request.form['seeking_venue'])

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # [DONE]: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]

  data = []
  try:

      join_table = db.session.query(Show.id, Venue.id.label("venue_id"), Venue.name.label("venue_name"), Artist.id.label("artist_id"), Artist.name.label("artist_name"), Artist.image_link, Show.start_time).join(Show, Venue.id == Show.venue_id).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time >= datetime.now()).order_by(Show.id).all()

      for i in join_table:
           show = {}
           show["venue_id"] = i.venue_id
           show["venue_name"] = i.venue_name
           show["artist_id"] = i.artist_id
           show["artist_name"] = i.artist_name
           show["artist_image_link"] = i.image_link
           show["start_time"] = i.start_time.strftime("%Y-%m-%d %H:%M:%S")
           data.append(show)
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # [DONE]: insert form data as a new Show record in the db, instead

  #{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }
  form = ShowForm(request.form)

  #print(request.form['genres'])
  #print(request.form['name'])
  if form.validate_on_submit():
      try:
          error = False
          artist_id = request.form['artist_id'].rstrip(" ")
          venue_id = request.form['venue_id'].rstrip(" ")
          start_time = request.form['start_time']

          new_show = Show(artist_id = artist_id, venue_id=venue_id, start_time=start_time)
          db.session.add(new_show)
          db.session.commit()
      except:
          db.session.rollback()
      finally:
          db.session.close()
      flash('Show was successfully listed!')
  else:
      flash('An error occurred. Show could not be listed.')


  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
