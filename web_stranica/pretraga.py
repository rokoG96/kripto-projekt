from flask import Flask, render_template, request
from konzolna_aplikacija import *

app = Flask (__name__)

@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
	txmempool = zadnjih_deset_transakcija(p);
	blokovi = zadnjih_deset_blokova(p)
	blokin = [] 
	for i in blokovi:
		hashbl = hashbloka(p, i)
		blokbl = vratiblok(p, hashbl)
		blokin_sve = infoblok(blokbl)
		blokin.append(blokin_sve)
	return render_template('home.html', value = blokin, txmempool = txmempool)

@app.route("/address_form")
def address_form():
	return render_template('address_form.html')

@app.route("/block_form")
def block_form():
	return render_template('block_form.html')

@app.route("/transaction_form")
def tx_form():
	return render_template('transaction_form.html')

@app.route("/error_page")
def error_pg():
	return render_template('error_page.html')

@app.route("/address", methods=['GET', 'POST'])
def address():
	ad=''
	if request.method == 'POST':
		if request.form.get('add2'):
			ad = request.form['add2']
		else:
			ad = request.form['adresa']
	if len(ad) >=14 and len(ad) <=74:
		saznajadresu = adresa(p, ad)
		return render_template('address.html', title = "address", value = saznajadresu, ad = ad)
	else:
		return render_template("error_page.html")

@app.route("/transaction", methods = ['GET', 'POST'])
def transaction():
	tx = ''
	if request.method == 'POST':
		if request.form.get('tx2'):
			tx = request.form['tx2']
		elif request.form.get('tx3'):
			tx = request.form['tx3']
		else:
			tx = request.form['transakcija']
	if len(tx) == 64:
		transakcijaa = transakcija(p, tx)
		ulazi = transakcijaa[0]
		izlazi = transakcijaa[1]
		ukupno_ulaza = transakcijaa[2]
		ukupno_izlaza = transakcijaa[3]
		razlika = transakcijaa[4]
		inn = transakcijaa[5]
		out = transakcijaa[6]
		return render_template('transaction.html', title = "transaction", value1 = ulazi, value2 = izlazi, 
							value3 = ukupno_ulaza, value4 = ukupno_izlaza, value5 = razlika, tx = tx, inn = inn, out = out);
	else:
		return render_template("error_page.html")

@app.route("/block", methods=['GET', 'POST'])
def block():
	height = brojblokova(p)
	blokinfo = ''
	if request.method == 'POST':
		if request.form.get('blok2'):
			blokinfo = request.form['blok2']
		else:
			blokinfo = request.form['blok']
	if blokinfo.isnumeric() == False:
		if len(blokinfo) == 64 and blokinfo[0] == '0':
			block = vratiblok(p, blokinfo);
			informacije = infoblok(block)
			sve = vrijednosttransakcija(p, block)
			return render_template('block.html', title = "block", value = informacije, ukupno = sve, visina = blokinfo);
		else:
			return render_template("error_page.html", 	blokinfo = blokinfo)
	elif int(blokinfo) > height:
		return render_template("error_page.html")
	else:
		hashblokaa = hashbloka(p, int(blokinfo))
		block = vratiblok(p, hashblokaa);
		informacije = infoblok(block)
		sve = vrijednosttransakcija(p, block)
		return render_template('block.html', title = "block", value = informacije, ukupno = sve, visina = blokinfo);

if __name__ == "__main__":
	bitcoin.SelectParams('testnet');
	p = bitcoin.rpc.RawProxy("Podaci za poslužitelj");
	app.run(debug=True);