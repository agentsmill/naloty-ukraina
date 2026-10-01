# Naloty na Ukrainę 2022–2026

Trójwymiarowa wizualizacja skali rosyjskich ataków i wybranych nalotów na zachód Ukrainy.
Statyczna strona bez etapu budowania: `index.html`, moduł obliczeń `js/model.mjs`, dane JSON
oraz three.js r160 z CDN. Lokalnie wymaga HTTP.

**Strona:** https://agentsmill.github.io/naloty-ukraina/

## Co oznaczają liczby

| Warstwa | Znaczenie |
|---|---|
| Główny strumień | Ilustracja natężenia, bez skali 1:1 i bez rzeczywistych miejsc trafień |
| Wybrany nalot | Zachód: 1 sylwetka / obiekt scenariusza; pozostałe BSP w grupach do 5, rakiety pojedynczo |
| Trasy | Umowne punkty startu i celu; niskie łuki o stałym tempie ruchu po długości krzywej |
| Czas lotu | Odległość geograficzna / przyjęta prędkość (185 lub 800 km/h); nie rekonstrukcja każdej klasy broni |
| BSP / dzień | Średnia miesiąca w starszej serii; od VIII 2026 liczba z konkretnego porannego raportu |
| BSP narastająco | Wyłącznie BSP, bez rakiet; sumy miesięczne i szacunki plus dostępne raporty dzienne |
| Zachód — ostatni wpis | Liczba przyjęta w zestawie; brak lub niezweryfikowane źródło opisane przy zdarzeniu |
| Zachód — wpisy ze źródłem | Suma tylko wpisów ze wskazanym źródłem liczby; nie pełna suma ataków ani liczba trafień |
| Poza Ukrainą | Liczba wybranych incydentów, nie obiektów; obejmuje przeloty i szczątki |

Odtwarzanie i przewijanie wyliczają liczniki z aktualnej daty. Powtórzenie zdarzenia nie dodaje
ponownie tych samych liczb. Scenariusze używają stałego ziarna losowania, więc odtworzenia są identyczne.
Nie losujemy skuteczności obrony na podstawie arbitralnej średniej krajowej.

## Dane i ograniczenia

- IX 2022 – XII 2024: wcześniejsze szacunki projektu; szare słupki. Nie zweryfikowano
  w tym przeglądzie wszystkich pierwotnych źródeł tych oszacowań.
- I 2025 – VII 2026: miesięczne liczby z tabel ISIS. Pierwsze siedem miesięcy 2025 ma
  wartości 2629, 3904, 4198, 2422, 4003, 5438 i 6297, razem **28 891**.
  VIII 2025 – VII 2026 daje **66 994** (wcześniej błędnie wpisano 62 994).
- Od VIII 2026: suma **porannych** raportów, a nie pełnych dób. Sierpień: **4620 BSP**;
  wrzesień: **5217 BSP** z 30 raportów. Dane sięgają raportu z 1 X 2026; skrypt dopisuje kolejne dni.
- Liczby rakiet zapisane słownie („двома протикорабельними ракетами”) są liczone. Przechwycone
  rakiety podnoszą `msl_min`, gdy opis ataku podaje typy bez liczby (np. 24 IX: co najmniej 7).
  Liczba w wyniku równa sumie pozostałych („55 ракет: 1 + 54”) jest traktowana jako suma, nie kolejna grupa.
- Raport z 12 IX 2026 wcześniej został zastąpiony większym raportem dziennym (410 BSP).
  Seria poranna zawiera teraz właściwy komunikat 77891 (129 BSP); nie oznacza to,
  że tego dnia użyto tylko 129 BSP. Osobne ataki dzienne nie wchodzą do tej serii.
- Wczesne szacunki i późniejsze raporty obejmują różne kategorie. BSP nie zawsze oznacza
  Shahed-136; zbiorcza kategoria zawiera także wabiki i inne typy.
- Brak raportu to brak danych. Częściowe słupki pokazują sumę dostępnych wpisów,
  bez prognozy całego miesiąca. Szacunkowa interpolacja dotyczy tylko serii miesięcznej.
- Około 163 obiekty z 5 X 2025 dotyczą obszaru dowództwa „Zachód”, nie samego obwodu lwowskiego.
  Trasa do Lwowa jest ilustracyjna; ta liczba nie trafia do zestawienia dla pojedynczego obwodu.
- Usunięto nieudokumentowane liczby ~40 (Tarnopol, 19 XI 2025), ~30 (Lwów, 24 III 2026)
  oraz arbitralny podział 82 BSP między miasta (1 IV 2026). Zdarzenia pozostają na osi.

Źródła sprawdzone 18 IX 2026:

- [ISIS — tabela 1 dla 2025 i I–VI 2026](https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine)
- [ISIS — VII–VIII 2026 i ograniczenia porannych raportów](https://isis-online.org/isis-reports/monthly-analysis-of-russian-shahed-136-deployment-against-ukraine-updated)
- [Siły Powietrzne, 30 VII 2026](https://t.me/kpszsu/70754): 284 BSP, 74 rakiety wystrzelone,
  320 przechwyconych celów łącznie, w tym 265 BSP; 55 dotyczyło przechwyconych rakiet.
- [Siły Powietrzne, 3 VIII 2026](https://t.me/kpszsu/71299): 181 BSP wystrzelonych; 14 oznaczało trafienia.
- [Siły Powietrzne, 17 IX 2026](https://t.me/kpszsu/78627): 157 BSP wystrzelonych,
  131 przechwyconych celów łącznie, w tym 124 BSP; co najmniej 4 rakiety, pełna liczba nieznana.
- [Siły Powietrzne, 6 VII 2023](https://t.me/kpszsu/3108): 10 Kalibrów, 7 przechwyceń.
- [Administracja lwowska, 5 X 2025](https://t.me/kozytskyy_maksym_official/25016): około 163 cele w obszarze „Zachód”.

Źródła sprawdzone 1 X 2026:

- [Siły Powietrzne, 13 IX 2026](https://t.me/kpszsu/78070): 453 BSP wystrzelonych, 405 przechwyconych.
- [Siły Powietrzne, 19 IX 2026](https://t.me/kpszsu/78956): „двома … ракетами” — 2 rakiety, pełna liczba.
- [Siły Powietrzne, 24 IX 2026](https://t.me/kpszsu/79861): typy rakiet bez liczby; przechwycono 4 + 3, więc minimum 7.
- [Siły Powietrzne, 29 IX 2026](https://t.me/kpszsu/81294): „ракетою” i „двома … ракетами” — 3 rakiety.
- Każdy z 27 incydentów poza Ukrainą ma w `index.html` własny odnośnik do źródła (pole `s`),
  widoczny w panelu po kliknięciu szpilki.

### Incydenty poza Ukrainą

Szpilki to wybrane, udokumentowane incydenty: upadki, zestrzelenia, szczątki i przeloty.
Liczą zdarzenia, nie pociski. 1 X 2026 sprawdzono wszystkie wcześniejsze wpisy ze źródłami
i poprawiono 10 z 13, głównie współrzędne. Merytoryczne korekty:

- Grindu, 11 XI 2025: dron spadł bez szkód; wcześniejszy opis trafienia w dom był błędny.
- Gaigalava (Łotwa), 7 IX 2024: ok. 85 km od granicy z Białorusią, nie ok. 150 km.
- Osiny, 20 VIII 2025: typ drona nie został ustalony, więc usunięto „Gerbera”.
- Wyryki-Wola, 10 IX 2025: według prokuratury dom trafiła rakieta AIM-9X z F-35.
- Tarnawa-Kolonia, 30 VII 2026: prokuratura potwierdziła pocisk Ch-101; poprawiono położenie.
- Dodano Bydgoszcz (Ch-55, 16 XII 2022) i 13 nowych zdarzeń z XI 2025 – IX 2026 w Rumunii,
  Mołdawii, Polsce i na Litwie, m.in. pierwsze zestrzelenie nad Rumunią (24 VII 2026),
  uzbrojony dron Gerbera-2 na plaży w Rusinowie (14 IX 2026) i zestrzelenie nad Litwą (15 IX 2026).
- Wybór nie jest kompletny. Według ABC News do 17 VIII 2026 Rumunia odnotowała 23 naruszenia
  przestrzeni, a prezydent Mołdawii mówi o 39 w 2026 r. Dodawaj wpisy tylko ze źródłem.

## Aktualizacja raportów

`scripts/scrape_af.py` czyta publiczny podgląd Telegrama @kpszsu, wyłącznie poranne komunikaty
„У ніч на …”. Sekcja wystrzeleń jest parsowana osobno od wyników obrony. Najnowsza korekta
tego samego raportu ma pierwszeństwo nawet wtedy, gdy zmniejsza liczbę.

Pola: `d` (data raportowanego nalotu), `id`, `source`, `coverage: "morning"`, `uav`,
`uav_down` (wyłącznie BSP lub `null`), `down_total` (wszystkie cele), `msl`
(pełna liczba wystrzelonych rakiet lub `null`), `msl_min` (znane minimum), `msl_complete`, `dirs`.

Skrypt nie zamienia nieznanej liczby w zero. Pojedynczy błąd sieci albo pusta strona są ponawiane;
trwały błąd albo brak rozpoznanych raportów przerywa aktualizację, a zapis jest atomowy.
GitHub Actions uruchamia skrypt codziennie o 06:10 UTC, a potem testy parsera i danych.

Kanał publikuje ok. 150–200 wpisów na dobę, więc domyślny limit 400 stron sięga ok. 45 dni wstecz.
Starsze dni uzupełnisz, podając id wpisu, od którego zacząć:

```bash
python3 scripts/scrape_af.py 2026-07-30 74300
```

Strona waliduje i sortuje dane, usuwa duplikaty dat i pomija przyszłe wpisy.
Po błędzie pobierania pokazuje jawny komunikat i kończy serię na 31 VII 2026,
bez fikcyjnych wartości zastępczych dla kolejnych miesięcy.

## Dane geograficzne

- **Granice obwodów** — geoBoundaries gbOpen ADM1 dla Ukrainy (27 jednostek: 24 obwody, Krym,
  Kijów, Sewastopol), uproszczone algorytmem Douglasa–Peuckera do ok. 1 800 punktów
- **Granice państw** — Natural Earth 50m. Domyślna wersja NE rysuje Krym po stronie rosyjskiej;
  pierścień Krymu został wycięty z wielokąta Rosji i zszyty z lądem Ukrainy wzdłuż wspólnych
  wierzchołków Przesmyku Perekopskiego, więc topologia z sąsiadami pozostaje spójna
- **Klasyfikacja granicy** — każdy segment obrysu Ukrainy dostaje kolor sąsiada, do którego
  jest najbliżej: NATO (Polska, Słowacja, Węgry, Rumunia), Białoruś, Rosja, Mołdawia, wybrzeże
- Linia frontu i zasięg okupacji — przybliżone ręcznie
- **Reszta kontynentu** — Natural Earth 50m, państwa przycięte do 2–78°E / 33–73°N i uproszczone do ok. 0,1°,
  tonowane politycznie (NATO chłodne, Rosja i Białoruś ciepłe, pozostałe neutralne) z granicami; woda zostaje
  tylko w Morzu Czarnym, Azowskim, Bałtyku i Kaspijskim

## Interakcje

- **Pauza** zatrzymuje loty, emisję tła, efekty i czas. Kamerę nadal można obracać.
- **1× / 3× / 8×** skaluje liniowo zarówno oś czasu, jak i tempo modelu nalotu.
- **Znacznik nalotu** uruchamia powtarzalny scenariusz. Koniec wymaga pustej kolejki,
  ukończonych lotów i krótkiego wygaszenia efektów.
- **Koniec osi** kończy ostatnie loty i pokazuje podsumowanie. „Odtwórz ponownie” zaczyna od 24 II 2022.
- **Koniec danych** przechodzi bezpośrednio do podsumowania, czyszcząc bieżącą animację.
- **Suwak** umożliwia przewijanie również klawiaturą. **Pomiń nalot** przechodzi do kolejnego dnia.
- **Obwód** otwiera wpisy z zestawu; zakończenia tras w modelu są opisane osobno od danych historycznych.
- **Obiekt w locie** pokazuje orientacyjny czas, dystans i wagę sylwetki w modelu.
- **Spacja** — pauza, **strzałki** — ±30 dni, **1/2/3** — tempo, **+/−** — zbliżenie, **Esc** — zamknięcie panelu.
- **Kółko myszy** przewija stronę także nad mapą. Mapę przybliża **Ctrl/⌘ + kółko**, gest szczypania
  na gładziku albo przyciski **+ / −** na mapie.
- **Dotyk:** przesunięcie w pionie przewija stronę, w bok obraca mapę, dwa palce przybliżają i pochylają.
  Dotknięcie obwodu lub szpilki otwiera panel, a lecącego obiektu pokazuje dymek na 4 s.
- **Telefon:** opis nalotu i liczniki są pod mapą, nie na niej; kamera obejmuje cały kraj.
- Przy `prefers-reduced-motion` strona zaczyna w pauzie, bez obrotu kamery.

## Stack

- three.js r160 (ESM przez importmap, jsDelivr), fonty IBM Plex Sans i Fraunces
- `OrbitControls`, `EffectComposer` z `UnrealBloomPass` i winietą, `OutputPass`, `RoomEnvironment`
- Mapa polityczna: 27 obwodów z zachłannym kolorowaniem (sąsiednie nigdy w tym samym odcieniu),
  obwody zachodnie w osobnej, cieplejszej palecie; rzeki; tereny okupowane kreskowane; 2048 px na `<canvas>`
- Sąsiedzi jako płaskie płyty niżej niż Ukraina, tonowane wg przynależności (NATO chłodne,
  Białoruś i Rosja ciepłe ciemne)
- Subtelny relief (przewyższenie ok. 5×) — tylko po to, żeby Karpaty łapały światło i rzucały cień
- Woda: płaszczyzna z kafelkowaną mapą normalnych z periodycznego Perlina, animowana
- Obrys, front, obwody i trasy — `Line2` o stałej szerokości ekranowej
- Modele: dron delta i rakieta jako `InstancedMesh` (pule 2 600 i 420), raycast z ręcznie ustawioną
  sferą otaczającą, żeby ruchome instancje były trafialne
- Efekty: pula 300 obiektów — błysk, kula ognia, dym, fala; odłamki z grawitacją; poświata na `<canvas>`
- Etykiety miast, obwodów i państw jako overlay HTML rzutowany co klatkę; obwody pokazują się po zbliżeniu

Zero plików binarnych. Geometria wbudowana w plik (ok. 35 KB), reszta generowana w locie.

## Uruchomienie lokalne

Importmap wymaga serwera HTTP — otwarcie przez `file://` nie zadziała.

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Wdrożenie na GitHub Pages

```bash
git init
git add index.html js README.md REVIEW.md scripts tests data .github .gitignore
git commit -m "Wizualizacja 3D nalotów na Ukrainę 2022-2026"
git branch -M main
git remote add origin git@github.com:UZYTKOWNIK/REPO.git
git push -u origin main
```

Potem w repo:

1. Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save
2. Settings → Actions → General → Workflow permissions → Read and write (żeby bot mógł commitować)
3. Actions → „Dane Sił Powietrznych” → Run workflow — pierwszy przebieg ręcznie, dla sprawdzenia

Po 1–2 minutach strona jest pod `https://UZYTKOWNIK.github.io/REPO/`.

Samo wyświetlanie strony nie wymaga GitHub Actions. Workflow jest potrzebny do automatycznej aktualizacji raportów.

## Testy

```bash
node --test tests/model.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Testy obejmują moment zakończenia lotu, pauzę i wygaszanie animacji, deterministyczne naloty,
zgodność wag z salwą, brak podwójnego liczenia, luki w danych, granice miesięcy i regresje parsera
na zapisanych fragmentach komunikatów. Szczegóły przeglądu: [REVIEW.md](REVIEW.md).

## Licencja

Kod: MIT. Dane liczbowe pochodzą z podanych wyżej źródeł i podlegają ich warunkom.
