# Markdown to HTML Parser

## Usage

From the command line via

```sh
python parser.py Input-File Output-File
```

or in a Python script via

```python
import parse from parser

parser.parse(Input-String)
```

## Dependencies

Markdown Parser requires an installed Python distribution, recommended the latest one (Version > 3), but also supports versions Python 2.7 and PyPy.
This project depends only on the [Regular Expression Library](https://docs.python.org/3/howto/regex.html) `re` (Regex) which can be installed using

```sh
pip install regex
```

## Supporting Types

- Plain Text
- Headings (`h1 - h6`)
- Links
- Boldface Texts
- Emphasized Texts
- Inline Code
- Code Blocks
- Unordered and Ordered Lists
- Quotations

# Behavior

Markup | HTML
------------ | -------------
`# Heading 1` | `<h1>Heading 1</h1>`
`## Heading 2` | `<h2>Heading 2</h2>`
`### Heading 3` | `<h3>Heading 3</h3>`
`#### Heading 4` | `<h4>Heading 4</h4>`
`##### Heading 5` | `<h5>Heading 5</h5>`
`###### Heading 6` | `<h6>Heading 3</h6>`
`> This is fun. - Me` | `<blockquote><p>This is fun. - Me</p></blockquote>`
`* Item 1`<br>`- Item 2`<br>`+ Item 3` | `<ul>` <br> `<li>Item 1` <br> `<li>Item 2` <br> `<li>Item 3` <br> `</ul>`
`1. Item 1`<br>`1. Item 2`<br>`1. Item 3` | `<ol>` <br> `<li>Item 1` <br> `<li>Item 2` <br> `<li>Item 3` <br> `</ol>`
`[Stack Overflow](https://stackoverflow.com/)` | `<p><a href="https://stackoverflow.com/">Stack Overflow</a></p>`
`_Emphasized Text_ also *emphasized Text*` | `<p><em>Emphasized Text</em> also *emphasized Text*</p>`
`__Strong Text__ also **strong Text**` | `<p><strong><strong>Strong Text</strong></strong> also **strong Text**</p>`
`***Strong and Emphasized Text***` | `<p><em><strong>Strong and Emphasized Text</em></strong></p>`
``Some inline Code: `pip install regex` `` | `<p>Some inline Code: <code>pip install regex<code></p>`
`` ``` ``<br> ``pip install regex``<br> `` pip install flask `` <br> `` ``` `` | `<code>`<br> `<p>pip install regex</p>` <br> `<p>pip install flask</p>` <br> `</code>`

## Author

Michael Schirmer <br>

- [Github](https://github.com/michischirmer/)
- [E-Mail](mailto:m.schirmer@tum.de)
