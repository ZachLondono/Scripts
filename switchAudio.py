import os

class Sink:
	def __init__(self):
		self.index = 0
		self.name = ""
		self.device = ""
		self.isSelected = False


out = os.popen('pacmd list-sinks').read()
lines = out.split('\n')

#sink_file = open("sinks")
#lines = sink_file.readlines()

sinks = []

curr_sink = ""
for line in lines:
	if "index" in line :
		curr_sink = Sink()
		sinks.append(curr_sink)
		index = line.split("index: ")[1]
		curr_sink.index = int(index, base=10)
		if "*" in line:
			curr_sink.isSelected = True

	if "name: <" in line :
		curr_sink.name = line.split("name: <")[1][0:]

	if "device.description" in line :
		curr_sink.device = line.split("device.description = ")[1]

options = ""
length = len(sinks)
for i in range(length):
	name = sinks[i].device
	if sinks[i].isSelected: name = "\"* " +name[1:]
	option = " {0} {1}".format(i, name)
	options += option

dialog = 'dialog --stdout --keep-tite --menu \"Choose Audio Sink\" 0 0 0'
dialog += options

out = os.popen(dialog).read()
if out.isnumeric() :
	index = int(out)
	switch = "pacmd set-default-sink {0}".format(sinks[index].name)
	os.system(switch)
