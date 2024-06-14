from flask import Flask, render_template, request
import wikipediaapi


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/', methods=['POST'])
def getURL():
    wikiTitle = request.form['wikiTitle']
    
    return render_template('pass.html', main=grabContent(wikiTitle), title=wikiTitle)

def grabContent(title):
    wiki = wikipediaapi.Wikipedia(
        user_agent= 'EasyWikiRead/1.0 (samanantha.com@gmail.com) requests',
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
    )
    
    page = wiki.page(title)
    if(page.exists()):
        pageText = f'<h1>{title}</h1>'
        pageText += page.summary
        pageText += getText(page.sections)
        return pageText
    else:
        return '\"' + title + '\" does not exist'

def getText(sections, level=2, pageText=''):
    for s in sections:
        if s.title != 'See also' and s.title != 'References':
            header_tag = f'h{min(level, 6)}' 
            pageText += f'<{header_tag}>{s.title}</{header_tag}>'
            if s.text:
                pageText += s.text
            pageText = getText(s.sections, level + 1, pageText)
        else:
            break
    return pageText
if __name__ == '__main__':
    app.run(debug=True)