#this file generates IDs for posts etc
import os, uuid, random, string


def postID(size, chars, userID):
	#take the userID and add a random string to it
	postID = userID + "." + ''.join(random.choice(chars) for _ in range(size))
	return postID


#this function is also used to generate dispute ids
def booking_id():
	#random String
	bookingID = str(uuid.uuid4().hex)
	return bookingID


def user_id(size, chars):
	#take the userID and add a random string to it
	userID = ''.join(random.choice(chars) for _ in range(size))
	print "gen'd new id: %s" % userID
	return userID


def username(forename, surname):
	#generates a username by taking the forename and surname and three random numbers

	#i know, i'll fix this mess later
	num1 = str(random.randint(1,9))
	num2 = str(random.randint(1,9))
	num3 = str(random.randint(1,9))

	username = forename + "." + surname + num1 + num2 + num3

	return username
