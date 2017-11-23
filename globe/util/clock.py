def timeNow():
	import time
	rightNow = time.localtime(time.time())
	print rightNow
	date = time.strftime("%a %b %d", rightNow)
	time = time.strftime("%H:%M:%S", rightNow)

	timeStamp = {
		"time": time,
		"date": date
	}

	return timeStamp
