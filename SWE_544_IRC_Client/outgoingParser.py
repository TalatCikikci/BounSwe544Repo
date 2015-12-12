def outgoing_parser(self):
	data = self.sender.text()
	
	# Handle empty input from user
	if len(data) == 0:
		return
	
	# Valid user messages start with a "/"
	if data[0] == "/":
		theCommandText = ''.join(data[1:])
		theCommandList = theCommandText.split()
		command = theCommandList[0]
		delta = theCommandList[1:]
		delta = ':'join(delta)
		
		if command == "nick":
			self.threadQueue.put("USR " + delta)
		
		if command == "list":
			self.threadQueue.put("LSQ")
		
		elif command == "quit":
			self.threadQueue.put("QUI")
		
		elif command == "msg":
			self.threadQueue.put("MSG " + delta)
		
		else:
			self.cprint("Local: Command Error.")
	
	else:
		self.threadQueue.put("SAY " + data)
	
	self.sender.clear()
