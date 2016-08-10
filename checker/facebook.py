import RPi.GPIO as GPIO, feedparser, time, subprocess

#if( int(time.strftime('%H')) >= 8 and int(time.strftime('%H')) <= 21 ):

def checkFacebook():
	nbr_notif = int(open("/home/pi/RaspiNotifier/nbr/nbr_facebook.txt", "r").read())
	GPIO_PIN = int(config.get("Facebook", "gpioPin"))
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(GPIO_PIN, GPIO.OUT)
	proc = subprocess.Popen("php /home/pi/RaspiNotifier/FacebookAPI/FBChecker.php", shell=True, stdout=subprocess.PIPE)
	newnotif = proc.stdout.read()
	if newnotif.isdigit():
		print("Facebook say: " + str(newnotif))
		print("Last time: " + str(nbr_notif))
		if int(newnotif) > nbr_notif:
			GPIO.output(GPIO_PIN, True)
			print("Turn on pin " + str(GPIO_PIN))
		if int(newnotif) == nbr_notif:
			print("Don't change state on GPIO")
		if int(newnotif) < nbr_notif:
			GPIO.output(GPIO_PIN, False)
			print("Turn off pin " + str(GPIO_PIN))
		open("/home/pi/RaspiNotifier/nbr/nbr_facebook.txt", "w").write(str(newnotif))
	else:
		print("Error: " + newnotif)
#else:
#	print("Silence !")
