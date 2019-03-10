"""
Sample script to test ad-hoc scanning by table drive.
This accepts a number with optional decimal part [0-9]+(\.[0-9]+)?

NOTE: suitable for optional matches
"""

def getchar(text,pos):
	""" returns char category at position `pos` of `text`,
	or None if out of bounds """
	
	if pos<0 or pos>=len(text): return None
	
	c = text[pos]
	
	# **Σημείο #3**: Προαιρετικά, προσθέστε τις δικές σας ομαδοποιήσεις
	
	if c == '0':
		return 'DIGIT_EQUAL_TO_0'
	if c >= '1' and c <= '2':
		return 'DIGIT_1_TO_2'
	if c == '3':
		return 'DIGIT_EQUAL_TO_3'
	if c == '4':
		return 'DIGIT_EQUAL_TO_4'
	if c == '5':
		return 'DIGIT_EQUAL_TO_5'
	if c >= '6' and c <= '9':
		return 'DIGIT_6_TO_9'
	
	return c	# anything else
	


def scan(text,transitions,accepts):
	""" scans `text` while transitions exist in
	'transitions'. After that, if in a state belonging to
	`accepts`, it returns the corresponding token, else ERROR_TOKEN.
	"""
	
	# initial state
	pos = 0
	state = 's0'
	# memory for last seen accepting states
	last_token = None
	last_pos = None
	
	
	while True:
		
		c = getchar(text,pos)	# get next char (category)
		
		if state in transitions and c in transitions[state]:
			state = transitions[state][c]	# set new state
			pos += 1	# advance to next char
			
			# remember if current state is accepting
			if state in accepts:
				last_token = accepts[state]
				last_pos = pos
			
		else:	# no transition found

			if last_token is not None:	# if an accepting state already met
				return last_token,last_pos
			
			# else, no accepting state met yet
			return 'ERROR_TOKEN',pos
			
	
# **Σημείο #1**: Αντικαταστήστε με το δικό σας λεξικό μεταβάσεων
transitions = {'s0': {'DIGIT_EQUAL_TO_0': 's1', 'DIGIT_1_TO_2': 's1', 'DIGIT_EQUAL_TO_3': 's4'},
               's1': {'DIGIT_EQUAL_TO_0': 's2', 'DIGIT_1_TO_2': 's2', 'DIGIT_EQUAL_TO_3': 's2', 'DIGIT_EQUAL_TO_4': 's2', 'DIGIT_EQUAL_TO_5': 's2', 'DIGIT_6_TO_9': 's2'},
               's2': {'DIGIT_EQUAL_TO_0': 's3'},
               's4': {'DIGIT_EQUAL_TO_0': 's5', 'DIGIT_1_TO_2': 's5', 'DIGIT_EQUAL_TO_3': 's5', 'DIGIT_EQUAL_TO_4': 's5', 'DIGIT_EQUAL_TO_5': 's5'},
               's5': {'DIGIT_EQUAL_TO_0': 's3'},
               's3': {'DIGIT_EQUAL_TO_0': 's6', 'DIGIT_1_TO_2': 's6', 'DIGIT_EQUAL_TO_3': 's6', 'DIGIT_EQUAL_TO_4': 's6', 'DIGIT_EQUAL_TO_5': 's6', 'DIGIT_6_TO_9': 's6'},
               's6': {'DIGIT_EQUAL_TO_0': 's8', 'DIGIT_1_TO_2': 's8', 'DIGIT_EQUAL_TO_3': 's8', 'DIGIT_EQUAL_TO_4': 's8', 'DIGIT_EQUAL_TO_5': 's8', 'DIGIT_6_TO_9': 's8'},
               's8': {'G': 's9', 'K': 's12', 'M': 's14'},
               's9': {'DIGIT_EQUAL_TO_0': 's10', 'DIGIT_1_TO_2': 's10', 'DIGIT_EQUAL_TO_3': 's10', 'DIGIT_EQUAL_TO_4': 's10', 'DIGIT_EQUAL_TO_5': 's10', 'DIGIT_6_TO_9': 's10'},
               's10': {'DIGIT_EQUAL_TO_0': 's11', 'DIGIT_1_TO_2': 's11', 'DIGIT_EQUAL_TO_3': 's11', 'DIGIT_EQUAL_TO_4': 's11', 'DIGIT_EQUAL_TO_5': 's11', 'DIGIT_6_TO_9': 's11'},
               's11': {'K': 's12', 'M': 's14'},
               's12': {'T': 's13'},
               's14': {'P': 's15'},
               's15': {'S': 's13'}
               }
# **Σημείο #2**: Αντικαταστήστε με το δικό σας λεξικό καταστάσεων αποδοχής
accepts = {'s13': 'WIND_TOKEN'
           }

# get a string from input
text = input('give some input>')

# scan text until no more input
while text:		# i.e. len(text)>0
	# get next token and position after last char recognized
	token,pos = scan(text,transitions,accepts)
	if token=='ERROR_TOKEN':
		print('unrecognized input at position',pos,'of',text)
		break
	print("token:",token,"text:",text[:pos])
	# new text for next scan
	text = text[pos:]
	
