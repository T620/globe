#used to insert random data into Users table

from faker import Faker
fake = Faker('en_GB')
from globe import app, db, models
from globe.models import User

from globe.util import id_gen
import string
from random import randint


newIds = []




for _ in range(0, 10):
	forename=fake.first_name()
	surname=fake.last_name()
	id=id_gen.user_id(5, string.digits)

	user = User(
		id=id,
		email=fake.email(),
		username=str(forename) + "." + str(surname) + "123",
		password=fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
		confirmationToken=fake.uuid4(),
		passwordToken=fake.uuid4(),
		forename=forename,
		surname=surname,
		city=fake.city(),
		biography=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
		verified=True,
		photo="https://s3.us-west-2.amazonaws.com/elasticbeanstalk-us-west-2-908893185885/static/user_uploads/39468/profile/placeholder.jpg"
	)

	db.session.add(user)
	db.session.commit()

	print "user id: %s" % id
	newIds.append(id)


f=open('/home/josh/projects/newids.txt', 'w')
f.write("\n" + str(newIds))
f.close()
