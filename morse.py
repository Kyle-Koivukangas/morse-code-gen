#This is a morse code generator, input text and the morse code equivalent will be played back.
#TODO: - pause_word is actually only .2 second pause as a shortcut workaround to letter pausing spaces being added before and after spaces
import time
import math
import numpy
import pyaudio

conversion_table = {
	'a':'.-',
	'b':'-...',
	'c':'-.-.',
	'd':'-..',
	'e':'.',
	'f':'..-.',
	'g':'-.',
	'h':'....',
	'i':'..',
	'j':'.---',
	'k':'-.-',
	'l':'.-..',
	'm':'--',
	'n':'-.',
	'o':'---',
	'p':'.--.',
	'q':'--.-',
	'r':'.-.',
	's':'...',
	't':'-',
	'u':'..-',
	'v':'...-',
	'w':'.--',
	'x':'-..-',
	'y':'-.--',
	'z':'--..',
	'1':'.----',
	'2':'..---',
	'3':'...--',
	'4':'....-',
	'5':'.....',
	'6':'-....',
	'7':'--...',
	'8':'---..',
	'9':'----.',
	'0':'-----',
	' ':'/',
	'.':'.-.-.-',
	',':'--..--',
	':':'---...',
	'?':'..--..',
	'\'':'.----.',
	'-':'-....-',
	'/':'-..-.',
	'(':'-.--.-',
	')':'-.--.-',
	'\"':'.-..-.',
	'@':'.--.-.',
	'=':'-...-'
}

class Sound:
	"""this class contains all the Sound and pause functions, all are reliant on the length of time that they will be played/paused
	1. Length of a dot is one unit.
	2. Length of a dash is three units.
	3. The pause between parts of the same letter is one unit.
	4. The pause between letters of the same word is three units.
	5. The pause between words is seven units.
	"""

	LENGTH = .100 #miliseconds
	BITRATE = 44100 #fps per frameset
	FREQUENCY = 3400  #Hz

	NUMBEROFFRAMES = int(BITRATE * LENGTH)
	RESTFRAMES = NUMBEROFFRAMES % BITRATE

	p = pyaudio.PyAudio()
	stream = p.open(format=pyaudio.paFloat32,
			channels=1, rate=BITRATE, output=True)

	def sine(self, frequency=FREQUENCY, length=LENGTH, rate=BITRATE):
		#makes the sine wave/tone to be played
		length = int(length * rate)
		factor = float(frequency) * (math.pi * 2) / rate
		return numpy.sin(numpy.arange(length) * factor)

	def play_tone(self, stream, frequency=FREQUENCY, length=LENGTH, rate=BITRATE):
		#writes or outputs a tone to the stream, which is played via pyaudio module
		chunks = []
		chunks.append(Sound.sine(self, frequency, length, rate))

		chunk = numpy.concatenate(chunks) * 0.25
		stream.write(chunk.astype(numpy.float32).tostring())

	def dot(self):
		#placeholder function for a short 'dot' beep of a interval of one unit
		print(".")
		Sound.play_tone(self, Sound.stream)
		pass

	def dash(self):
		#placeholder function for a long 'dash' beep of an interval of three units
		print("---")
		Sound.play_tone(self, stream=Sound.stream, length=Sound.LENGTH*3)
		pass

	def pause(self):
		#A one unit length pause (pause for between parts of a letter)
		time.sleep(self.LENGTH)
		print(">")
		return
	def pause_letter(self):
		#A three unit lengt pause (pause for between letters of a word)
		print('>>')
		time.sleep(self.LENGTH*2) 	#*2 not *3 because there is a 1 unit pause automaticall added inbetween every character anyways
		return
	def pause_word(self):
		#A seven unit length pause (pause for between words, signifies a space)
		print('>>')
		time.sleep(self.LENGTH*2) 	#*6 not *7 because of automatic 1 unit pause added after every character.
		return


def convert_input(input):
	#converts the input in to more code symbols according to the conversion table. 
	converted = []
	for char in list(input):
		converted.append(conversion_table[char])
		converted.append('_')
	return ''.join(converted)

def play(converted_input):
	#takes the morse converted symbols and iterates through them, playing the appropriate Sound or pause.
	#input should look like this: "...._._.-.._.-.._---/.--_---_.-._.-.._-.." <- says "hello world"
	switch_dict = {
		'.': sound.dot,
		'-': sound.dash,
		'_': sound.pause_letter,
		'/': sound.pause_word
	}

	for char in converted_input:
		switch_dict[char]()
		if char == '.' or char == '-':
			sound.pause() #automatic pause between each note


if __name__ == "__main__":
	sound = Sound()
	inp = "hello world"


	print("Welcome to the morse code generator, this program will convert a string into morse code...\nto exit type in 'e'\n\n")
	while inp != 'e':

		inp = raw_input("Type something to convert to morse code: ")
		converted_input = convert_input(inp)

		print(converted_input)
		play(converted_input)
		print(inp)
		print(converted_input)

		if inp == 'e':
			print("EXITING...")

	
	sound.stream.close()
	sound.p.terminate()


