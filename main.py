"""
Třetí projekt do Engeto Online Python Akademie
Autor: Tomas Horvath
Email: Tomas@horvath.site

Popis:
Tento skript slouží ke stahování a zpracování výsledků voleb z webu.
Na základě URL odkazu extrahuje seznam lokací, stahuje výsledky voleb
pro každou lokaci a ukládá je do souboru CSV.
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def ziskej_seznam_lokaci(odkaz):
    """
    Na základě odkazu (URL) stáhne stránku a extrahuje kódy okrsků,
    jejich názvy a relativní odkazy. Výsledek vrací jako list n-tic (kod, nazev, odkaz).

    Parametry:
        odkaz (str): URL odkaz na stránku se seznamem lokací.

    Návratová hodnota:
        list: Seznam n-tic obsahujících kód, název a odkaz na detaily okrsku.
    """
    soup = ziskej_soup(odkaz)

    cisla = ziskej_cisla_lokaci(soup)
    nazvy = ziskej_nazvy_lokaci(soup)
    odkazy = ziskej_odkazy_lokaci(soup)

    return list(zip(cisla, nazvy, odkazy))

def zapis_do_csv(seznam_lokaci, nazev_souboru):
    """
    Ukládá výsledky voleb do CSV souboru.

    Parametry:
        seznam_lokaci (list): Seznam lokací (n-tice obsahující kód, název a odkaz).
        nazev_souboru (str): Název výstupního souboru (bez přípony).

    Návratová hodnota:
        None
    """
    if not seznam_lokaci:
        print("Nebyla nalezena žádná lokace, ukončuji program.")
        sys.exit()

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
    Stáhne HTML obsah stránky a vrátí jej jako objekt BeautifulSoup.

    Parametry:
        odkaz (str): URL adresa stránky.

    Návratová hodnota:
        BeautifulSoup: HTML obsah stránky.
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
    Extrahuje kódy okrsků z HTML.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Seznam kódů okrsků.
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
    Extrahuje názvy okrsků z HTML.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Seznam názvů okrsků.
    """
    td_prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb2", "t2sa1 t2sb2", "t3sa1 t3sb2")
    return [td.text for td in td_prvky]

def ziskej_odkazy_lokaci(soup_obj):
    """
    Extrahuje relativní odkazy na detaily okrsků z HTML.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Seznam relativních odkazů.
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
    Vyhledá a spojí td prvky podle atributu headers.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.
        *args (str): Hodnoty atributu headers.

    Návratová hodnota:
        list: Seznam td prvků.
    """
    prvky = []
    for arg in args:
        prvky += soup_obj.select(f'td[headers="{arg}"]')
    return prvky

def vytvor_csv_hlavicku(soup_obj):
    """
    Vytvoří hlavičku CSV souboru.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Hlavička CSV souboru.
    """
    zakladni_informace = ["code", "location", "registered", "envelopes", "valid"]
    nazvy_stran = ziskej_nazvy_stran(soup_obj)
    return zakladni_informace + nazvy_stran

def ziskej_nazvy_stran(soup_obj):
    """
    Extrahuje názvy politických stran z HTML.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Názvy politických stran.
    """
    prvky = ziskej_td_prvky(soup_obj, "t1sa1 t1sb2", "t2sa1 t2sb2")
    return [p.text for p in prvky if p.text != "-"]

def ziskej_vysledky_lokace(soup_obj):
    """
    Extrahuje výsledky voleb pro jednu lokaci.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Výsledky voleb (registrovaní voliči, obálky, platné hlasy a hlasy pro strany).
    """
    return ziskej_hodnoty_info(soup_obj) + ziskej_hlasy_stran(soup_obj)

def ziskej_hodnoty_info(soup_obj):
    """
    Extrahuje základní informace (registrovaní voliči, obálky, platné hlasy).

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Základní informace o volbách.
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
    Extrahuje počty hlasů pro politické strany.

    Parametry:
        soup_obj (BeautifulSoup): HTML obsah stránky.

    Návratová hodnota:
        list: Hlasy pro politické strany.
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
    """
    Hlavní funkce programu. Zpracovává argumenty z příkazové řádky, stahuje data
    a ukládá je do CSV souboru.
    """
    if len(sys.argv) != 3:
        print("Použití: python main.py [URL] [název_souboru_bez_přípony]")
        sys.exit(1)

    odkaz = sys.argv[1]
    nazev_souboru = sys.argv[2]

    lokace = ziskej_seznam_lokaci(odkaz)
    zapis_do_csv(lokace, nazev_souboru)

if __name__ == "__main__":
    main()
