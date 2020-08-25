from app import db, Venue, Location, Artist, Show, Genre, ArtistGenre, VenueGenre, format_datetime, get_or_create_loc
from datetime import datetime
from sqlalchemy import func, case, or_
from datetime import datetime
import json

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
        print(location_id)

        new_venue = Venue(name = name, location_id = location_id, phone = phone , image_link = image_link, facebook_link = facebook_link, address = address, website = website , seeking_talent = seeking_talent, seeking_description = seeking_description)
        db.session.add(new_venue)
        db.session.flush()

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
