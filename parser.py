import re

with open('file.md') as file:
	input = file.read()
	input_lines = input.splitlines()

lines = []
list_start = False
list_o_start = False
quote_start = False
for line in input_lines:
	if not re.search(r'^(-|\*|\+).*', line):
		if list_start:
			lines.append('</ul>')
		list_start = False

	if not re.search(r'^(\>).*', line):
		if quote_start:
			lines.append('</blockquote>')
		quote_start = False
	if not re.search(r'^(\d*\.).*', line):
		if list_o_start:
			lines.append('</ol>')
		list_o_start = False

	
		

	# Headings
	if re.search(r'^#{1,6}', line): 
		for i in [6,5,4,3,2,1]:
			if re.search(r'^#{' + str(i) + r'}', line):
				count = i
				break

		line = re.sub(r'^#{' + str(count) + '} *', '<h' + str(count) + '>', line) + '</h' + str(count) + '>'
		lines.append(line)
	# Links
	elif re.search(r'\[.+\]\(.+\)', line):
		link = re.findall(r'\(.+\)', line)[0][1:-1]
		anker = re.findall(r'\[.+\]', line)[0][1:-1]
		lines.append(f'<a href="{link}">{anker}</a>')
	# Bold Text
	elif re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line) or re.search(r'[(.^\*)*]\*{1}.+\*{1}[(.^\*)*]', line):
		if re.search(r'[(.^_)*]_{1}.+_{1}[(.^_)*]', line):
			text = re.sub(r'[_]','' , line)
		else:
			text = re.sub(r'[\*]','' , line)
		lines.append(f'<strong>{text}</strong>')
	# Emphasized Text
	elif re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', line) or re.search(r'[.^\*]*\*{1,1}.+\*{1,1}[.^\*]*', line):
		if re.search(r'[.^_]*_{1,1}.+_{1,1}[.^_]*', line):
			text = re.sub(r'[_]','' , line)
		else:
			text = re.sub(r'[\*]','' , line)
		lines.append(f'<em>{text}</em>')
	# Inline Code
	elif re.search(r'.*`.*`.*', line):
		code = re.sub(r'`[.*`]', '</code>', line)
		lines.append('<p>' + re.sub(r'`', '<code>', code) + '</p>')
	# Unordered List
	elif re.search(r'^(-|\*|\+).*', line):
		if not list_start:
			lines.append('<ul>')
			list_start = True
		lines.append(re.sub(r'[-|\*|\+] *', '<li>', line))
	# Quote
	elif re.search(r'^(\>).*', line):
		if not quote_start:
			lines.append('<blockquote>')
			quote_start = True
		lines.append(re.sub(r'[\>] *', '<p>', line) + '</p>')
	# Ordered List
	elif re.search(r'^(\d*\.).*', line):
		if not list_o_start:
			lines.append('<ol>')
			list_o_start = True
		lines.append(re.sub(r'(\d*\.) *', '<li>', line))
	# Plain Text
	elif line != '':
		lines.append('<p>' + line + '</p>')
	
	else:
		lines.append(line)
	

for line in lines:
	print(line)

