def incoming_parser(self, data):
	
	# Handle empty message from server
	if len(data) == 0:
		return
	
	# Handle message with first word longer than 3 letters
	elif len(data) > 3 and not data[3] == " ":
		response = "ERR"
		self.csoc.send(response)
		return
	
	
	rest = data[4:]
	
	elif data[0:3] == "BYE":
		username = rest.strip()
		msg = "Goodbye " + username + ", we hope to see you again!"
	
	elif data[0:3] == "ERL":
		msg = "You need to login to do that. Login command: USR <username>"
	
	elif data[0:3] == "HEL":
		username = rest.strip()
		msg = "Login successful. Hello " + username
	
	elif data[0:3] == "REJ":
		username = rest.strip()
		msg = "Username " + username + " already exists in the system. Please login with a different username."
	
	elif data[0:3] == "MNO":
		username = rest.strip()
		msg = "User " + username + " could not be found. Message was not delivered."
	
	elif data[0:3] == "MSG":
		splitted = rest.split(":")
		username = splitted[0]
		message = splitted[1]
		msg = username + " <private> : " + message
	
	elif data[0:3] == "SAY":
		msg = "Someone says "rest[0]
	
	elif data[0:3] == "SYS":
		msg = "<SYSTEM MESSAGE> : " + rest[0]
	
	elif data[0:3] == "LSA":
		splitted = rest.split(":")
		msg = "-Server- Registered nicks: "
		for i in splitted:
			msg += i + ","
		msg = msg[:-1]
	
	elif data[0:3] == "TOC"
		msg = "TOC!"
	
	elif data[0:3] == "SOK"
		msg = "Message sent to everyone."
	
	elif data[0:3] == "MOK"
		msg = "Private message delivered to user."
	
	elif data[0:3] == "ERR"
		msg = "Invalid command."
	
	else:
		response = "ERR"
		self.csoc.send(response)
		return

	
	self.app.cprint(msg)
