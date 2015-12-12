def outgoing_parser(self):
	data = self.sender.text()
	if len(data) == 0:
		return
		
	if data[0] == "/":
		...
		...
		
		if command == "list":
			...
			...
		
		elif command == "quit":
			...
			...
		
		elif command == "msg":
			...
			...
		
		else:
			self.cprint("Local: Command Error.")
	
	else:
		self.threadQueue.put("SAY " + data)
	
	self.sender.clear()
