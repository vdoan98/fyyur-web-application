from app import db, ArtistGenre, VenueGenre, Genre, format_datetime

# genre1 = Genre(name='Jazz')
# genre2 = Genre(name='Reggae')
# genre3 = Genre(name='Swing')
# genre4 = Genre(name='Classical')
# genre5 = Genre(name='Folk')
# genre6 = Genre(name='R&B')
# genre7 = Genre(name='Hip-Hop')
# genre8 = Genre(name='Rock n Roll')


genre9 = Genre(name='Alternative')
genre10 = Genre(name='Blues')
genre11 = Genre(name='Country')
genre12 = Genre(name='Electronic')
genre13 = Genre(name='Funk')
genre14 = Genre(name='Heavy Metal')
genre15 = Genre(name='Instrumental')
genre16 = Genre(name='Musical Theatre')
genre17 = Genre(name='Pop')
genre18 = Genre(name='Punk')
genre19 = Genre(name='Soul')
genre20 = Genre(name='Other')


print("add genres")
db.session.add(genre9)
db.session.add(genre10)
db.session.add(genre11)
db.session.add(genre12)
db.session.add(genre13)
db.session.add(genre14)
db.session.add(genre15)
db.session.add(genre16)
db.session.add(genre17)
db.session.add(genre18)
db.session.add(genre19)
db.session.add(genre20)


#db.session.commit()
