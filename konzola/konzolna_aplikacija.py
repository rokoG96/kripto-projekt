import time
import bitcoin
import bitcoin.rpc
import sys


def brojblokova(p):
    visina = p.getblockcount()
    print("Broj blokova u testnet blockchainu: ", visina, "\n")
    return visina


def hashbloka(p, visina):
    blokhash = p.getblockhash(visina)
    return blokhash


def brojtransakcija(p, blockhash):
    blok = p.getblock(blockhash)
    blok_brojtx = blok["nTx"]
    print("Broj transakcija u bloku: ", blok_brojtx)
    return blok


def vrijednosttransakcija(p, blok):
    transakcije = blok["tx"]
    vrijednost = 0
    for txid in transakcije:
        tx_vrijednost = 0
        raw_tx = p.getrawtransaction(txid)
        decoded_tx = p.decoderawtransaction(raw_tx)
        for izlaz in decoded_tx["vout"]:
            tx_vrijednost = tx_vrijednost + izlaz["value"]
            vrijednost = vrijednost + tx_vrijednost
    print("Vrijednost transakcija u bloku: ", vrijednost, " tBTC")


def infoblok(blok):
    blok_brojtx = blok["nTx"]
    print("Broj transakcija u bloku: ", blok_brojtx)

    hash_blok = blok["hash"]
    print("Hash bloka: ", hash_blok)

    potvrde = blok["confirmations"]
    print("Broj potvrda: ", potvrde)

    vrijeme_bloka = blok["time"]
    datum = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(vrijeme_bloka))
    print("Vrijeme kad je izrudaren blok: ", datum)

    velicina_bloka = blok["size"]
    print("Veličina bloka: ", velicina_bloka)

    visina_bloka = blok["height"]
    print("Visina bloka: ", visina_bloka)

    verzija_bloka = blok["version"]
    print("Verzija: ", verzija_bloka)

    merkle_blok = blok["merkleroot"]
    print("Merkle root bloka: ", merkle_blok)

    tezina_bloka = blok["difficulty"]
    print("Težina: ", tezina_bloka)

    transakcije_bloka = blok["tx"]
    print("Transakcije u bloku: ", transakcije_bloka)


def transakcija(p, adresa):
    ukupno_ulaza = 0
    ukupno_izlaza = 0
    sirova_transakcija = p.getrawtransaction(adresa)
    dekodirana_transakcija = p.decoderawtransaction(sirova_transakcija)
    ulazi = dekodirana_transakcija["vin"]
    print("Ulazi transakcije:\n ")
    for i in ulazi:
        print("ID ulazne transakcije:", i["txid"])
        identifikator = i["vout"]
        raw_tx = p.getrawtransaction(i["txid"])
        decoded_tx = p.decoderawtransaction(raw_tx)
        for j in decoded_tx["vout"]:
            if j["n"] == identifikator:
                print("Adresa: ", j["scriptPubKey"]["addresses"])
                print("Vrijednost ulaza:", j["value"], "tBTC", "\n")
                ukupno_ulaza += j["value"]

    print("\n")
    izlazi = dekodirana_transakcija["vout"]
    print("Izlazi transakcije:\n ")
    for j in izlazi:
        print("Adresa: ", j["scriptPubKey"]["addresses"])
        print("Vrijednost izlaza:", j["value"], "tBTC")
        ukupno_izlaza += j["value"]

    print("\n")
    print("Ukupna vrijednost ulaza u transakciju je:", ukupno_ulaza, "tBTC")
    print("Ukupna vrijednost izlaza iz transakcije je:", ukupno_izlaza, "tBTC")
    print(
        "Vrijednost naknade za rudara u transakciji je:",
        ukupno_ulaza - ukupno_izlaza,
        "tBTC",
    )


def adresa(p, broj):
    informacija = p.getaddressinfo(broj)
    print("Valjana adresa: ", informacija["address"])
    print("Heksadecimalni prikaz pubkey skripte: ", informacija["scriptPubKey"])
    print("Pripada li adresa poslužitelju: ", informacija["ismine"])
    print("Možemo li trošiti bitcoine sa ove adrese: ", informacija["solvable"])
    print("Dozvoljeno samo gledanje: ", informacija["iswatchonly"])
    print("Je li ključ adrese skripta: ", informacija["isscript"])
    print("Je li adresa svjedok: ", informacija["iswitness"])
    print("Je li adresa korištena za vraćanje ostatka: ", informacija["ischange"])
    print("Oznake vezane za adresu: ", informacija["labels"])


def main():
    bitcoin.SelectParams("testnet")
    p = bitcoin.rpc.RawProxy("Podaci za poslužitelj")
    print(
        "\nDobrodošli na searchblock u konzoli!\nOvdje možete saznati informacije o blokovima, transakcijama i adresama na bitcoin testnet mreži.\n"
    )
    visina = brojblokova(p)
    print(
        "\n---------------------------------------------------------------------------------\n"
    )
    odgovor = input(
        "Postojeće ocije: \n1. Informacije o bloku\n2. Informacije o transakciji\n3. Informacije o adresi \nOdaberite broj željene opcije: "
    )

    if odgovor == "1":
        zeljena_visina = input("Unesite visinu bloka o kojem želiš saznati više: ")
        if int(zeljena_visina) > visina:
            print("Blok broj ", zeljena_visina, "još nije izrudaren!")
            sys.exit()
        else:
            print(
                "\nInformacije o bloku koji se nalazi na visini", zeljena_visina, ":\n"
            )
            hashovi = hashbloka(p, int(zeljena_visina))
            blok = brojtransakcija(p, hashovi)
            vrijednosttransakcija(p, blok)
            infoblok(blok)

    elif odgovor == "2":
        zeljena_transakcija = input("Unesite željenu transakcije: ")
        if len(zeljena_transakcija) != 64:
            print("Transakcija nije valjana!")
            sys.exit()

        else:
            print("\nInformacije o transakciji čiji je hash", zeljena_transakcija, ":")
            transakcija(p, zeljena_transakcija)
    elif odgovor == "3":
        zeljena_adresa = input("Unesite željenu adresu: ")

        if len(zeljena_adresa) >= 26 and len(zeljena_adresa) <= 35:
            print("\nInformacije o adresi:\n ")
            adresa(p, zeljena_adresa)

        else:
            print("Unešena adresa nije valjana!")
            sys.exit()
    else:
        print("Unešen krivi broj, molimo ponovno pokrenite program!")
        sys.exit()


if __name__ == "__main__":
    main()
