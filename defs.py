
# this is a tool for music theory learners
# made in python by dubis

# numbers to represent notes
# just get the index in the list
# doesn't use flats
# C is [0], D# is [3]
# intervals are [last note] - [first note]
# major third (E and C, for example) is 4-0=4
notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

# jazz extensions
# interval from root

extensions_list = {
	'b6':8,
	'6':9,
	'b7':10,
	'7':11,
	'b9':13,
	'9':14,
	'#9':15,
	'11':17,
	'#11':18,
	'b13':20,
	'13':21
}

# lists to keep things organized

chordtypes = []
chords = []
scaletypes = []
scales = []

# classes for more versatility

# chord types, such as major and minor
class ChordType:
	def __init__(self,fullname:str,intervals:list,allList=chordtypes,mood=None,names:list=[]):
		self.names = names
		self.fullname = fullname
		self.intervals = intervals
		self.mood = mood
		if allList != None:
			allList.append(self)
	def add_from_root(self,interval):
		intsum = 0
		for eachint in self.intervals:
			intsum += eachint
		return interval - intsum

# chords, such as C major or C minor
class Chord:
	def __init__(self,root,ctype:ChordType,slash=None,mood=None,allList=chords):
		self.root = root
		self.ctype = ctype
		self.mood = mood
		self.slash= slash
		self.name = root+' '+ctype.fullname
		if allList != None:
			allList.append(self)
		result = [self.root]
		current = notes.index(self.root)
		for interval in self.ctype.intervals:
			result.append(notes[(current+interval)%len(notes)])
			current = current + interval
		self.notes = result

# scales, such as F lydian or G major
class ScaleType:
	def __init__(self,name,intervals:list,mood=None,allList=scaletypes):
		self.name = name
		self.intervals = intervals
		self.mood = mood
		if allList != None:
			allList.append(self)

class Scale:
	def __init__(self,root,stype:ScaleType,mood=None,allList=scales):
		self.root = root
		self.stype = stype
		self.mood = mood
		self.name = root+' '+self.stype.name
		if allList != None:
			allList.append(self)
		result = [self.root]
		current = notes.index(self.root)
		for interval in self.stype.intervals:
			result.append(notes[(current+interval)%len(notes)])
			current = current + interval
		self.notes = result

# this part is for defining all chords, scales etc
# using lists for faster creation

# chord types list
# only triads
# extensions separately
chordtypeslist = [
	['major',['','M','+'],[4,3]],
	['minor',['m','-'],[3,4]],
	['diminished',['dim','º'],[3,3]],
	['suspended 2nd',['sus2'],[2,5]],
	['suspended 4th',['sus4'],[5,2]],
	['power chord',['5'],[7]]
]
# [0] is full name
# [1] is common names
# [2] is intervals

# creating chord types
for chordtypelist in chordtypeslist:
	ChordType(chordtypelist[0],chordtypelist[2],names=chordtypelist[1])

# creating all possible chords
for note in notes:
	for chordtype in chordtypes:
		Chord(note,chordtype)

# other functions

# find_chord for triads
def find_chord(small_name:str):
	try:
		if small_name[1:2] == '#':
			num = 2
		else:
			num = 1
		root = small_name[:num]
		rest = small_name[num:]
		for chordtype in chordtypes:
			for name in chordtype.names:
				if rest == name:
					result_type = chordtype
		for chord in chords:
			if chord.root == root:
				if result_type == chord.ctype:
					return chord
	except:
		# return a C major if error
		chords[0]

def find_chord_type(full_name:str):
	try:
		for ctype in chordtypes:
			if ctype.fullname == full_name:
				return ctype
		# return a C major if error
		return chords[0]
	except:
		# return a C major if error
		return chords[0]

# find intervals
def find_interval(root,interval):
	return notes[notes.index(root)+interval%len(notes)]

# create jazzy chords with extensions
# extensions in jazz notation (like b13)
def chord_type_with_extensions(base_ctype:ChordType,extensions:list):
	try:
		intervals = base_ctype.intervals
		new_name = base_ctype.fullname + ' ('
		for ext in extensions:
			intervals.append(base_ctype.add_from_root(extensions_list[ext]))
			new_name += ext
			if extensions.index(ext) < len(extensions)-1:
				new_name += ','
		new_name += ')'
		return ChordType(new_name,intervals)
	except:
		return chordtypes[0]

def extended_chord(base_chord_name:list,extensions:list):
	chord = find_chord(base_chord_name)
	return Chord(chord.root,chord_type_with_extensions(chord.ctype,extensions))