from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.secret_key = 'lkdkjfvjhdklkhuescb'

articles_dict = {
    'abcd': {'headline': 'This terrifying AI generates fake articles from any news site',
             'body': """The Allen Institute for Artificial Intelligence has an interesting new tactic in the war on fake news: make more of it.
                    A team of researchers at the institute recently developed Grover, a neural network capable of generating 
                    fake news articles in the style of actual human journalists. In essence, the group is fighting fire with 
                    fire because the better Grover gets at generating fakes, the better it’ll be at detecting them.
                     According to the institute:
             """
             },
    '1234': {'headline': 'Once Thriving Cheeto Driven To Extinction By Unregulated Snack Food Industry',
             'body': """This is dummy copy. It is not meant to be read. 
             It has been placed here solely to demonstrate the look and feel of finished. This is dummy copy. 
             It is not meant to be read. It has been placed here solely to demonstrate the look and feel of finished. 
             This is dummy copy. It is not meant to be read. 
             It has been placed here solely to demonstrate the look and feel of finished. This is dummy copy. 
             It is not meant to be read. It has been placed here solely to demonstrate the look and feel of finished. """}
}

@application.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@application.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls:
            flash('That shortened code is taken. Please pick something else and retry.')
            return redirect(url_for('home'))

        if 'url' in request.form:
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save("./static/user_files/{}".format(full_name))
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@application.route('/<string:code>')
def redirect_to_url(code):
    if code in articles_dict:
        return render_template('article.html', article=articles_dict[code])
    else:
        return abort(404)


@application.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@application.route('/api')
def session_api():
    return jsonify(list(session.keys()))


if __name__ == '__main__':
    application.debug = True
    application.run()