# Treti projekt do Engeto Online Python Akademie
# author: Tomas Horvath
# email: Tomas@horvath.site 


import requests
from bs4 import BeautifulSoup
import csv
import sys

def ziskej_seznam_lokaci():
    """
    Na základě odkazu zadaného uživatelem stáhne stránku a extrahuje kódy okrsků,
    jejich názvy a relativní odkazy. Výsledek vrací jako list n-tic (kod, nazev, odkaz).
    """
    odkaz = input("Vložte odkaz na volební výsledky z požadovaného okresu: ").strip()
    soup = ziskej_soup(odkaz)

    cisla = ziskej_cisla_lokaci(soup)
    nazvy = ziskej_nazvy_lokaci(soup)
    odkazy = ziskej_odkazy_lokaci(soup)

    return list(zip(cisla, nazvy, odkazy))

def zapis_do_csv(seznam_lokaci):
    """
    Očekává seznam lokací (n-tice: kód, název, odkaz).
    Od uživatele načítá název souboru a vytvoří soubor CSV s hlavičkou.
    Poté stahuje výsledky voleb pro každou lokaci a zapisuje je do nového řádku v CSV.
    """
    if not seznam_lokaci:
        print("Nebyla nalezena žádná lokace, ukončuji program.")
        sys.exit()

    nazev_souboru = input("Zadejte název vašeho výstupního souboru (bez přípony .csv): ").strip()
    prvni_odkaz = "https://www.volby.cz/pls/ps2017nss/" + seznam_lokaci[0][2]
    hlavicka_soup = ziskej_soup(prvni_odkaz)
    hlavicka_csv = vytvor_csv_hlavicku(hlavicka_soup)

    try:
        with open(f"{nazev_souboru}.csv", "w", newline="", encoding="utf-8") as vystupni_soubor:
            zapisovac = csv.writer(vystupni_soubor)
            zapisovac.writerow(hlavicka_csv)

            for kod, nazev, odkaz in seznam_lokaci:
                print(f"Aktuálně zpracovávám lokaci: {nazev}.")
                cilovy_odkaz = "https://www.volby.cz/pls/ps2017nss/" + odkaz
                soup = ziskej_soup(cilovy_odkaz)
                vysledky = ziskej_vysledky_lokace(soup)
                zapisovac.writerow([kod, nazev] + vysledky)
    except Exception as e:
        print(f"Nastala chyba při práci se souborem: {e}")
        sys.exit()

def ziskej_soup(odkaz):
    """
    Očekává URL adresu jako řetězec.
    Provádí GET požadavek a vrací objekt BeautifulSoup pro další zpracování.
    """
    try:
        odpoved = requests.get(odkaz)
        odpoved.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Nastala chyba při stahování stránky: {e}")
        sys.exit()
    return BeautifulSoup(odpoved.text, "html.parser")

def ziskej_cisla_lokaci(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vyhledává td prvky s kódy okrsků. V těchto prvcích dále hledá tag <a> a
    extrahuje text (číslo okrsku).
    Vrací list kódů okrsků.
    """
    td_prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1")
    cisla = []
    for td in td_prvky:
        odkaz = td.find("a")
        if odkaz:
            cisla.append(odkaz.text)
    return cisla

def ziskej_nazvy_lokaci(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vyhledává td prvky s názvy okrsků a extrahuje z nich text.
    Vrací list názvů okrsků.
    """
    td_prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2")
    return [td.text for td in td_prvky]

def ziskej_odkazy_lokaci(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vyhledává td prvky, kde se nachází tag <a> s odkazy na detail okrsku.
    Extrahuje atribut 'href' z každého takového tagu.
    Vrací list relativních odkazů.
    """
    td_prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb1", "t2sa1 t2sb1", "t3sa1 t3sb1")
    odkazy = []
    for td in td_prvky:
        odkaz = td.find("a")
        if odkaz:
            odkazy.append(odkaz.get("href"))
    return odkazy

def ziskej_td_prvky(soup_obj, *args):
    """
    Očekává objekt BeautifulSoup a libovolný počet řetězců, které
    reprezentují hodnoty atributu headers.
    Sloučí td prvky zadaných headers a vrací list těchto td prvků.
    """
    prvky = []
    for arg in args:
        prvky += soup_obj.select(f'td[headers="{arg}"]')
    return prvky

def vytvor_csv_hlavicku(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Kombinuje základní informace a názvy politických stran do jedné hlavičky CSV.
    Vrací list, který se následně stane hlavičkou CSV.
    """
    zakladni_informace = ["code", "location", "registered", "envelopes", "valid"]
    nazvy_stran = ziskej_nazvy_stran(soup_obj)
    return zakladni_informace + nazvy_stran

def ziskej_nazvy_stran(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vyhledává td prvky s názvy politických stran a extrahuje z nich text.
    Vrací list názvů stran.
    """
    prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb2", "t2sa1 t2sb2")
    return [p.text for p in prvky if p.text != "-"]

def ziskej_vysledky_lokace(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vrací výsledky voleb (registrovaní voliči, vydané obálky, platné hlasy a hlasy pro strany)
    jako list.
    """
    return ziskej_hodnoty_info(soup_obj) + ziskej_hlasy_stran(soup_obj)

def ziskej_hodnoty_info(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vrací list s počtem registrovaných voličů, vydanými obálkami a platnými hlasy.
    """
    hlavicky_info = ["sa2", "sa3", "sa6"]
    hodnoty = []
    for hlavicka in hlavicky_info:
        prvek = soup_obj.find("td", {"headers": hlavicka})
        text_hodnoty = prvek.text.replace("\xa0", "") if prvek else "0"
        try:
            hodnoty.append(int(text_hodnoty))
        except ValueError:
            hodnoty.append(0)
    return hodnoty

def ziskej_hlasy_stran(soup_obj):
    """
    Očekává objekt BeautifulSoup.
    Vyhledává td prvky s počtem hlasů pro jednotlivé strany a vrací je v listu.
    """
    prvky = ziskej_td_prvky(soup_obj, "t1sa2 t1sb3", "t2sa2 t2sb3")
    hlasy = []
    for p in prvky:
        if p.text != "-":
            hodnota = p.text.replace("\xa0", "")
            try:
                hlasy.append(int(hodnota))
            except ValueError:
                hlasy.append(0)
    return hlasy

def main():
    """Hlavní funkce. Načítá seznam okrsků (jako n-tice) a rovnou ukládá výsledky do CSV."""
    lokace = ziskej_seznam_lokaci()
    zapis_do_csv(lokace)

if __name__ == "__main__":
    main()
