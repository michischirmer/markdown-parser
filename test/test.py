import markdown

with open('file.md') as file:
	print(markdown.markdown(file.read()))