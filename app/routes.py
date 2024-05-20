from app import app
import requests
import json
import os
from bs4 import BeautifulSoup
from flask import render_template, request, redirect, url_for
from app import utils
@app.route("/")
def index():
    return render_template("index.html.jinja")
@app.route('/extract', methods={'POST','GET'})
def extract():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        url=f'https://www.ceneo.pl/{product_id}'
        response = requests.get(url)
        if response.status_code == requests.codes['ok']:
            page_dom = BeautifulSoup(response.text,"html.parser")
            opinions_count = utils.extract(page_dom,"a.product-review__link > span").text.strip()
            if opinions_count:
                while(url):
                    response = requests.get(url)
                    page_dom = BeautifulSoup(response.text, "html.parser")
                    opinions = page_dom.select("div.js_product-review")
                    for opinion in opinions:
                        single_opinion = {
                            key : extract(opinion, *value)
                                for key, value in selectors.items()
                        }
                        all_opinions.append(single_opinion)
                    try:
                        url = "https://www.ceneo.pl" + extract(page_dom,"a.pagination__next","href")
                    except TypeError:
                        url = None
                    if not os.path.exists("opinions"):
                        os.mkdir("opinions")
                    with open(f"opinions/{product_id}")
                return redirect(url_for('product', product_id=product_id))
            return render_template("extract.html.jinja", error="dla produktu o podanym kodzie nie ma opinii")
        return render_template("extract.html.jinja", error="produkt o podanym kodzie nie istnieje")
    return render_template("extract.html.jinja")
@app.route('/products')
def products():
    return render_template("products.html.jinja")
@app.route('/author')
def author():
    return render_template("author.html.jinja")
@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id)