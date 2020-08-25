from app import db, Venue, Show, Artist, Location, format_datetime

location1 = Location(city = "San Francisco", state = "CA")
location2 = Location(city = "New York", state = "NY")

db.session.add(location1)
db.session.add(location2)

# Add venues

venue1 = Venue(name = "The Musical Hop", location_id = 1, phone = "123-123-1234" , image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60", facebook_link = "https://www.facebook.com/TheMusicalHop", address = "1015 Folsom Street", website = "https://www.themusicalhop.com" , seeking_talent = True, seeking_description = "We are on the lookout for a local artist to play every two weeks. Please call us.")

venue2 = Venue(name = "The Dueling Pianos Bar", location_id = 2 , phone = "914-003-1132" , image_link = "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80", facebook_link = "https://www.facebook.com/theduelingpianos", address = "335 Delancey Street", website = "https://www.theduelingpianos.com" , seeking_talent = False)

venue3 = Venue(name = "Park Square Live Music & Coffee", location_id = 1, phone = "415-000-1234" , image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80", facebook_link = "https://www.facebook.com/ParkSquareLiveMusicAndCoffee", address = "34 Whiskey Moore Ave", website = "https://www.parksquarelivemusicandcoffee.com" , seeking_talent = False)

print("Add Venues")
db.session.add(venue1)
db.session.add(venue2)
db.session.add(venue3)


# Add Artists

artist1 = Artist(id = 4, name = "Guns N Petals" , location_id = 1, phone = "326-123-5000", image_link = "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80" , facebook_link = "https://www.facebook.com/GunsNPetals", seeking_description = "Looking for shows to perform at in the San Francisco Bay Area!", seeking_venue = True, website = "https://www.gunsnpetalsband.com" )

artist2 = Artist(id = 5, name = "Matt Quevedo" , location_id = 2 , phone = "300-400-5000" , image_link = "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80" , facebook_link = "https://www.facebook.com/mattquevedo923251523" , seeking_venue = False)

artist3 = Artist(id = 6, name = "The Wild Sax Band" , location_id = 1, phone = "432-325-5432" , image_link = "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80" , seeking_venue = False )

print("Add Artists")
db.session.add(artist1)
db.session.add(artist2)
db.session.add(artist3)


#Add shows

show1 = Show(venue_id = 1, artist_id = 4 , start_time = format_datetime("2019-06-15T23:00:00.000Z"))

show2 = Show(venue_id = 3, artist_id = 5, start_time = format_datetime("2019-06-15T23:00:00.000Z"))

show3 = Show(venue_id = 3, artist_id = 6, start_time = format_datetime("2035-04-01T20:00:00.000Z"))

show4 = Show(venue_id = 3, artist_id = 6, start_time = format_datetime("2035-04-08T20:00:00.000Z"))

show5 = Show(venue_id = 3, artist_id = 6, start_time = format_datetime("2035-04-15T20:00:00.000Z"))

print("Add Shows")
db.session.add(show1)
db.session.add(show2)
db.session.add(show3)
db.session.add(show4)
db.session.add(show5)

db.session.commit()
