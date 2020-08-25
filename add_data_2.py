from app import db, ArtistGenre, VenueGenre, Genre, format_datetime


genre1 = Genre(name='Jazz')
genre2 = Genre(name='Reggae')
genre3 = Genre(name='Swing')
genre4 = Genre(name='Classical')
genre5 = Genre(name='Folk')
genre6 = Genre(name='R&B')
genre7 = Genre(name='Hip-Hop')
genre8 = Genre(name='Rock n Roll')

print("add genres")
db.session.add(genre1)
db.session.add(genre2)
db.session.add(genre3)
db.session.add(genre4)
db.session.add(genre5)
db.session.add(genre6)
db.session.add(genre7)
db.session.add(genre8)


venueGenre1 = VenueGenre(venue_id = 1, genre_id = 1)
venueGenre2 = VenueGenre(venue_id = 1, genre_id = 2)
venueGenre3 = VenueGenre(venue_id = 1, genre_id = 3)
venueGenre4 = VenueGenre(venue_id = 1, genre_id = 4)
venueGenre5 = VenueGenre(venue_id = 1, genre_id = 5)

venueGenre6 = VenueGenre(venue_id = 2, genre_id = 4)
venueGenre7 = VenueGenre(venue_id = 2, genre_id = 6)
venueGenre8 = VenueGenre(venue_id = 2, genre_id = 7)

venueGenre9 = VenueGenre(venue_id = 3, genre_id = 8)
venueGenre10 = VenueGenre(venue_id = 3, genre_id = 1)
venueGenre11 = VenueGenre(venue_id = 3, genre_id = 4)
venueGenre12 = VenueGenre(venue_id = 3, genre_id = 5)


print("add venue genre")

db.session.add(venueGenre1)
db.session.add(venueGenre2)
db.session.add(venueGenre3)
db.session.add(venueGenre4)
db.session.add(venueGenre5)
db.session.add(venueGenre6)
db.session.add(venueGenre7)
db.session.add(venueGenre8)
db.session.add(venueGenre9)
db.session.add(venueGenre10)
db.session.add(venueGenre11)
db.session.add(venueGenre12)


artistGenre1 = ArtistGenre(artist_id = 4, genre_id = 8)
artistGenre2 = ArtistGenre(artist_id = 5, genre_id = 1)
artistGenre3 = ArtistGenre(artist_id = 6, genre_id = 1)
artistGenre4 = ArtistGenre(artist_id = 6, genre_id = 4)

print("add artist genre")

db.session.add(artistGenre1)
db.session.add(artistGenre2)
db.session.add(artistGenre3)
db.session.add(artistGenre4)


db.session.commit()
