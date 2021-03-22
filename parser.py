import re
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print('Usage: python parser.py <Input File> (<Output File>)')
	exit(1)

def parse(input):
	input_lines = input.splitlines()
	lines = []
	list_start = False
	list_o_start = False
	quote_start = False
	code_block = False

	for line in input_lines:
		toAdd = ''
		wrapper = False

		if not re.search(r'^\s*(-|\*|\+).*', line):
			if list_start:
				toAdd += '</ul>'
			list_start = False

		if not re.search(r'^(\>).*', line):
			if quote_start:
				toAdd += '</p></blockquote>'
			quote_start = False

		if not re.search(r'^\s*(\d*\.).*', line):
			if list_o_start:
				toAdd += '</ol>'
			list_o_start = False

		if line == '```':
			if code_block:
				code_block = False
				toAdd += '</code>'
			else:
				code_block = True
				toAdd += '<code>'

		# Headings
		if re.search(r'^#{1,6}', line): 
			for i in [6,5,4,3,2,1]:
				if re.search(r'^#{' + str(i) + r'}', line):
					count = i
					break
			line = re.sub(r'^#{' + str(count) + '} *', '<h' + str(count) + '>', line) + '</h' + str(count) + '>'
			line = re.sub(r' *#+', '', line)
			toAdd += line

		# Links
		if re.search(r'\[.+\]\(.+\)', line):
			link = re.findall(r'\(.+\)', line)[0][1:-1]
			anker = re.findall(r'\[.+\]', line)[0][1:-1]
			prev = line[:line.find('[')]
			after = line[line.find(')') + 1:]
			toAdd += f'{prev}<a href="{link}">{anker}</a>{after}'
			wrapper = True

		# Bold and Italic Text
		if re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', line) or re.search(r'[(.^\*)*]\*{2}.+\*{2}[(.^\*)*]', line):
			if re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', line):
				text = re.sub(r'[_]', '<em><strong>', line, 1)
				text = re.sub(r'[_]', '', text, 4)
				text = re.sub(r'[_]', '</em></strong>', text, 1)
			else:
				text = re.sub(r'[\*]', '<em><strong>', line, 1)
				text = re.sub(r'[\*]', '', text, 4)
				text = re.sub(r'[\*]', '</em></strong>', text, 1)
			toAdd += text
			wrapper = True

		# Bold Text
		elif re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line) or re.search(r'[(.^\*)*]\*{1}.+\*{1}[(.^\*)*]', line):
			if re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line):
				text = re.sub(r'[_]','<strong>' , line, 1)
				text = re.sub(r'[_]','' , text, 1)
				text = re.sub(r'[_]','</strong>' , text, 1)
				text = re.sub(r'[_]','' , text, 1)
			else:
				text = re.sub(r'[\*]','<strong>' , line, 1)
				text = re.sub(r'[\*]','' , text, 1)
				text = re.sub(r'[\*]','</strong>' , text, 1)
				text = re.sub(r'[\*]','' , text, 1)
			toAdd += text
			wrapper = True

		# Emphasized Text
		elif re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', line) or re.search(r'[.^\*]*\*{1,1}.+\*{1,1}[.^\*]*', line):
			if re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', line):
				text = re.sub(r'[_]','<em>' , line, 1)
				text = re.sub(r'[_]','</em>' , text, 1)
			else:
				text = re.sub(r'[\*]','<em>' , line, 1)
				text = re.sub(r'[\*]','</em>' , text, 1)
			toAdd += text
			wrapper = True

		# Inline Code
		if re.search(r'`.+`', line) and re.match(r'`.+`', line) is None:
			code = re.sub(r'`', '<code>', line, 1)
			toAdd += re.sub(r'`', '</code>', code, 1)
			wrapper = True
		
		if re.search(r'`.+`', line) and re.match(r'`.+`', line) is not None:
			code_block = True

		
		# Unordered List
		if re.search(r'^\s*(-|\+).*', line):
			if not list_start:
				toAdd += '<ul>'
				list_start = True
			toAdd += re.sub(r'\s*[-|\+] *', '<li>', line)

		# Quote
		if re.search(r'^(\>).*', line):
			if not quote_start:
				toAdd += '<blockquote><p>'
				quote_start = True
			toAdd += re.sub(r'[\>] *', '', line)

		# Ordered List
		if re.search(r'^\s*(\d*\.).*', line):
			if not list_o_start:
				toAdd += '<ol>'
				list_o_start = True
			toAdd += re.sub(r'\s*(\d*\.) *', '<li>', line)

		if toAdd != '' and wrapper:
			while toAdd != inline_parse(toAdd):
				toAdd = inline_parse(toAdd)
			lines.append('<p>' + inline_parse(toAdd) + '</p>')
		elif code_block and line != '```':
			lines.append('<p>' + line + '</p>')
		else:
			lines.append(toAdd)


	output = '\n'.join(lines)
	return output


def inline_parse(string):
	toAdd = ''
	case = True

	# Headings
	if re.search(r'^#{1,6}', string): 
		for i in [6,5,4,3,2,1]:
			if re.search(r'^#{' + str(i) + r'}', string):
				count = i
				break
		string = re.sub(r'^#{' + str(count) + '} *', '<h' + str(count) + '>', string) + '</h' + str(count) + '>'
		string = re.sub(r' *#+', '', string)
		toAdd += string
		case = False

	# Links
	if re.search(r'\[.+\]\(.+\)', string):
		link = re.findall(r'\(.+\)', string)[0][1:-1]
		anker = re.findall(r'\[.+\]', string)[0][1:-1]
		prev = string[:string.find('[')]
		after = string[string.find(')') + 1:]
		toAdd += f'{prev}<a href="{link}">{anker}</a>{after}'
		case = False

	# Bold and Italic Text
	if re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', string) or re.search(r'[(.^\*)*]\*{2}.+\*{2}[(.^\*)*]', string):
		if re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', string):
			text = re.sub(r'[_]', '<em><strong>', line, 1)
			text = re.sub(r'[_]', '', text, 4)
			text = re.sub(r'[_]', '</em></strong>', text, 1)
		else:
			text = re.sub(r'[\*]', '<em><strong>', string, 1)
			text = re.sub(r'[\*]', '', text, 4)
			text = re.sub(r'[\*]', '</em></strong>', text, 1)
		toAdd += text
		case = False

	# Bold Text
	elif re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', string) or re.search(r'[(.^\*)*]\*{1}.+\*{1}[(.^\*)*]', string):
		if re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', string):
			text = re.sub(r'[_]','<strong>' , string, 1)
			text = re.sub(r'[_]','' , text, 1)
			text = re.sub(r'[_]','</strong>' , text, 1)
			text = re.sub(r'[_]','' , text, 1)
		else:
			text = re.sub(r'[\*]','<strong>' , string, 1)
			text = re.sub(r'[\*]','' , text, 1)
			text = re.sub(r'[\*]','</strong>' , text, 1)
			text = re.sub(r'[\*]','' , text, 1)
		toAdd += text
		case = False

	# Emphasized Text
	elif re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', string) or re.search(r'[.^\*]*\*{1,1}.+\*{1,1}[.^\*]*', string):
		if re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', string):
			text = re.sub(r'[_]','<em>' , string, 1)
			text = re.sub(r'[_]','</em>' , text, 1)
		else:
			text = re.sub(r'[\*]','<em>' , string, 1)
			text = re.sub(r'[\*]','</em>' , text, 1)
		toAdd += text
		case = False

	# Inline Code
	if re.search(r'`.+`', string) and re.match(r'`.+`', string) is None:
			code = re.sub(r'`', '<code>', string, 1)
			toAdd += re.sub(r'`', '</code>', code, 1)
			case = False
	
	return toAdd if not case else string


with open(sys.argv[1]) as file:
	input = file.read()

with open(sys.argv[2], 'w') as f:
	f.write(parse(input))