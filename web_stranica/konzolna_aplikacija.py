import time
import bitcoin
import bitcoin.rpc
import sys

def brojblokova(p):
    visina = p.getblockcount()
    return visina

def zadnjih_deset_blokova(p):
    blokovi = []
    num = 1
    zadnji = brojblokova(p)
    blokovi.append(zadnji)
    while(num < 10):
        blokovi.append(zadnji-num)
        num+=1
    return blokovi

def zadnjih_deset_transakcija(p):
    transakcije=[]
    memorijski_bazen = p.getrawmempool(True);
    keys=memorijski_bazen.keys()
    vel = len(keys)
    granica=0
    if vel > 10:
        granica = 10
    else:
        granica = vel
    for i in keys:
        if (granica > 0):
            vrijeme_tx = memorijski_bazen[i]['time'];
            datum = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(vrijeme_tx));
            transakcije.append((i, memorijski_bazen[i]['size'], datum));
            granica -= 1
    return transakcije
       
def hashbloka(p, visina):
    blokhash = p.getblockhash(visina)
    return blokhash

def vratiblok(p, blockhash):
    blok = p.getblock(blockhash)
    blok_brojtx = blok['nTx']
    return blok
    
def vrijednosttransakcija(p, block):
    transactions = block['tx'];
    value = 0
    for txid in transactions:
        tx_value = 0
        raw_tx = p.getrawtransaction(txid)
        decoded_tx = p.decoderawtransaction(raw_tx)
        for output in decoded_tx['vout']:
            tx_value = tx_value + output['value']
            value = value + tx_value
    return value
    
def infoblok(block):
    info = []
    block_numbertx = block['nTx']
    info.append(block_numbertx)

    hash_block = block['hash']
    info.append(hash_block)

    confirmations = block['confirmations']
    info.append(confirmations)
    
    time_block = block['time']
    date=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time_block))
    info.append(date)
    
    size_block = block['size']
    info.append(size_block)
    
    height_block = block['height']
    info.append(height_block)
    
    version_block = block['version']
    info.append(version_block)
    
    merkle_block = block['merkleroot']
    info.append(merkle_block)

    difficulty_block = block['difficulty']
    info.append(difficulty_block)
    
    transactions_block = block['tx']
    info.append(transactions_block)
    
    return info

def transakcija(p, adresa):
    ulazi_transakcija = []
    izlazi_transakcija = []
    ukupno_ulaza = 0
    ukupno_izlaza = 0
    inn = 0
    out = 0
    sirova_transakcija = p.getrawtransaction(adresa)
    dekodirana_transakcija = p.decoderawtransaction(sirova_transakcija)
    ulazi = dekodirana_transakcija['vin']
    for i in ulazi:
        identifikator = i['vout']
        raw_tx = p.getrawtransaction(i['txid'])
        decoded_tx = p.decoderawtransaction(raw_tx)
        for j in decoded_tx['vout']:
            if j['n'] == identifikator:
                adresa_za_printanje_u = str(j['scriptPubKey']['addresses'])
                adresa_za_printanje_u = adresa_za_printanje_u.strip("[,',]")
                ulazi_transakcija.append((adresa_za_printanje_u, j['value']))
                ukupno_ulaza += j['value']
                inn +=1
            
    izlazi = dekodirana_transakcija['vout']
    for j in izlazi:
        adresa_za_printanje_i = str(j['scriptPubKey']['addresses'])
        adresa_za_printanje_i = adresa_za_printanje_i.strip("[,',]")
        izlazi_transakcija.append((adresa_za_printanje_i, j['value']))
        ukupno_izlaza += j['value']
        out +=1
     
    razlika = ukupno_ulaza - ukupno_izlaza
    return (ulazi_transakcija, izlazi_transakcija, ukupno_ulaza, ukupno_izlaza, razlika, inn, out)    
        
def adresa (p, broj):
    informacija = p.getaddressinfo(broj)
    addressinfo = []
    addressinfo.append(informacija['address'])
    addressinfo.append(informacija['scriptPubKey'])
    addressinfo.append(informacija['ismine'])
    addressinfo.append(informacija['solvable'])
    addressinfo.append(informacija['iswatchonly'])
    addressinfo.append(informacija['isscript'])
    addressinfo.append(informacija['iswitness'])
    if informacija['iswitness'] == True:
        addressinfo.append(informacija['witness_version'])
        addressinfo.append(informacija['witness_program'])
    addressinfo.append(informacija['ischange'])
    addressinfo.append(informacija['labels'])
    return addressinfo
