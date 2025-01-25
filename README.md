# Engeto-project-3

Poslední projekt Engeto Python akademie (online) s daty.


## Cíl projektu

Primárním cílem tohoto projektu je stáhnout a rozparsovat data z webové stránky [(voleb)](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Dojde k extrakci (kódu okrsků, názvy, počty registrovaných voličů, platných hlasů a rozdělení hlasů podle stran) a uloží je do CSV souboru. 

Repozitář projektu je k dispozici [zde](https://github.com/xhorva04/Engeto-project-3).


## Instalace potřebných knihoven
Vytvořný soubor `requirements.txt` obsahuje soupis knihoven a verzí potřebných ke spuštění projektu.

K nainstalování všech závislostí ze souboru: `requirements.txt` je vhodné použít:

`pip install -r requirements.txt`

## Spuštění projektu (skriptu)
Spuštění projektu probíhá přes příkazovou řádku, kde je nezbytné prvně naisntalovat virtuální prostředí s potřebnýmí knihovnami (viz výše), dále pak je nutné mít virtuální prostředí aktivní a zapsat:

`python main.py [URL] [název_souboru_bez_přípony]`


## Ukázka projektu
Pro parsování údajů z Ostravy bude příkaz vypadat následovně:

`python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106" "Ostrava"`


Správnost spuštění indikuje dílčí výpis ze zpracovávané lokace:
```
Aktuálně zpracovávám lokaci: Čavisov.
Aktuálně zpracovávám lokaci: Dolní Lhota.
Aktuálně zpracovávám lokaci: Horní Lhota.
Aktuálně zpracovávám lokaci: Klimkovice.
Aktuálně zpracovávám lokaci: Olbramice.
Aktuálně zpracovávám lokaci: Ostrava.
Aktuálně zpracovávám lokaci: Stará Ves nad Ondřejnicí.
Aktuálně zpracovávám lokaci: Šenov.
Aktuálně zpracovávám lokaci: Václavovice.
Aktuálně zpracovávám lokaci: Velká Polom.
Aktuálně zpracovávám lokaci: Vratimov.
Aktuálně zpracovávám lokaci: Vřesina.
Aktuálně zpracovávám lokaci: Zbyslavice.
```

Ukázkový výstup z Ostravy (Ostrava.csv) může vypadat následovně (zkráceno):
```
code,location,registered,envelopes,valid,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,Česká národní fronta,Referendum o Evropské unii,TOP 09,ANO 2011,Dobrá volba 2016,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů
569119,Čavisov,419,318,316,29,0,0,22,0,16,34,4,2,2,0,0,36,0,0,5,103,0,0,27,0,1,2,0,29,4
506711,Dolní Lhota,1202,904,899,95,2,0,69,0,31,41,9,3,2,1,1,90,0,0,25,356,0,2,65,0,6,7,0,91,3
...
```