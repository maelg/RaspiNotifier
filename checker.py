import os, sys, time
from config import *
from checker import facebook, gmail

if( int(time.strftime('%H')) >= 8 and int(time.strftime('%H')) <= 21 ):
    #facebook.checkFacebook()
    gmail.checkGmail()

elif( int(time.strftime('%H')) == 22 ) :
    state_gpio = [ True, GPIO.input(11), GPIO.input(16) ] #Night mode state, gpio11, gpio16

    file = open(os.path.dirname(__file__)+"/night.save", "w")
    cPickle.dump(state_gpio, file)
    file.close()

    GPIO.output(11, False)
    GPIO.output(16, False)

elif( int(time.strftime('%H')) == 8 ) :
    state_gpio = cPickle.load( open( os.path.dirname(__file__)+"/night.save", "r" ) )

    GPIO.output(11, state_gpio[0])
    GPIO.output(16, state_gpio[1])
