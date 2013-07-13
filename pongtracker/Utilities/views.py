import string
import random

#----------------------------------------------
# Creates a random password of length len
#    len:    int    length of password
#
#    returns: string
#----------------------------------------------
def createRndPass(length):
    passChars = list(string.ascii_letters + string.digits)    #list of lowercase, uppercase and digits
    passChars.remove('l')   #remove characters that look similar to others
    passChars.remove('O')
    
    random.seed()   #generate random seed based on time
    
    rndPass = ''
    for x in range(length):     #create password
        rndPass += random.choice(passChars)
    
    return rndPass