import re
import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print('Usage: python parser.py <Input File> (<Output File>)')
	exit(1)

with open(sys.argv[1]) as file:
	input_lines = file.read().splitlines()

lines = []
list_start = False
list_o_start = False
quote_start = False
code_block = False

for line in input_lines:
	toAdd = ''
	wrapper = False

	if not re.search(r'^(-|\*|\+).*', line):
		if list_start:
			toAdd += '</ul>'
		list_start = False

	if not re.search(r'^(\>).*', line):
		if quote_start:
			toAdd += '</p></blockquote>'
		quote_start = False

	if not re.search(r'^(\d*\.).*', line):
		if list_o_start:
			toAdd += '</ol>'
		list_o_start = False

	if code_block:
		wrapper = False
	
	if re.search(r'^```$', line):
		wrapper = False
		if code_block:
			toAdd += '</code>'
			code_block = False
		else:
			toAdd += '<code>'
			code_block = True

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
	elif re.search(r'\[.+\]\(.+\)', line):
		link = re.findall(r'\(.+\)', line)[0][1:-1]
		anker = re.findall(r'\[.+\]', line)[0][1:-1]
		prev = line[:line.find('[')]
		after = line[line.find(')') + 1:]
		toAdd += f'{prev}<a href="{link}">{anker}</a>{after}'
		wrapper = True

	# Bold and Italic Text
	elif re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', line) or re.search(r'[(.^\*)*]\*{2}.+\*{2}[(.^\*)*]', line):
		if re.search(r'[(.^_)*]_{2}.+_{2}[(.^_)*]', line):
			text = re.sub(r'[_]','<em><strong>' , line, 3)
			text = re.sub(r'[_]','</em></strong>' , text, 3)
		else:
			text = re.sub(r'[\*]','<em><strong>' , line, 3)
			text = re.sub(r'[\*]','</em></strong>' , text, 3)
		toAdd += text
		wrapper = True

	# Bold Text
	elif re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line) or re.search(r'[(.^\*)*]\*{1}.+\*{1}[(.^\*)*]', line):
		if re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line):
			text = re.sub(r'[_]','<strong>' , line, 2)
			text = re.sub(r'[_]','</strong>' , text, 2)
		else:
			text = re.sub(r'[\*]','<strong>' , line, 2)
			text = re.sub(r'[\*]','</strong>' , text, 2)
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
	elif re.search(r'.*`.*`.*', line):
		code = re.sub(r'`[.*`]', '</code>', line)
		toAdd += re.sub(r'`', '<code>', code)
		wrapper = True

	# Unordered List
	elif re.search(r'^(-|\*|\+).*', line):
		if not list_start:
			toAdd += '<ul>'
			list_start = True
		toAdd += re.sub(r'[-|\*|\+] *', '<li>', line)

	# Quote
	elif re.search(r'^(\>).*', line):
		if not quote_start:
			toAdd += '<blockquote><p>'
			quote_start = True
		toAdd += re.sub(r'[\>] *', '', line)

	# Ordered List
	elif re.search(r'^(\d*\.).*', line):
		if not list_o_start:
			toAdd += '<ol>'
			list_o_start = True
		toAdd += re.sub(r'(\d*\.) *', '<li>', line)

	# Plain Text
	elif line != '':
		toAdd += line
		wrapper = True

	if toAdd != '' and wrapper:
		lines.append('<p>' + toAdd + '</p>')
	else:
		lines.append(toAdd)

output = '\n'.join(lines)
with open(sys.argv[2], 'w') as f:
	f.write(output)