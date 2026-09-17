# Naloty na Ukrainę 2022–2026

Trójwymiarowa wizualizacja rosyjskiej kampanii powietrznej przeciw Ukrainie od 24 lutego 2022,
z naciskiem na jedno pytanie: **ile z tego dociera na zachód kraju.**

Jeden plik, zero zależności poza three.js z CDN. Działa na GitHub Pages bez build stepu.

**Strona:** https://agentsmill.github.io/naloty-ukraina/

## Co pokazuje

| Warstwa | Skala | Podstawa |
|---|---|---|
| Główny strumień | umowna — gęstość proporcjonalna do bieżącego tempa dobowego | seria miesięczna wystrzeleń |
| Uderzenia na zachód | **1:1** — tyle kropek, ile obiektów potwierdzono | komunikaty obwodowych administracji wojskowych |
| Łuki i czasy przelotu | rzeczywista odległość ortodromiczna | 185 km/h dla Gerana-2, ok. 800 km/h dla rakiet manewrujących |
| Relief terenu | przewyższenie ok. 40× | proceduralny, oparty na rzeczywistym układzie pasm |
| Licznik narastający | przybliżony | suma serii miesięcznej |
| Obiekty poza Ukrainą | wybór udokumentowanych przypadków | bursztynowe szpilki w Polsce, Mołdawii, Rumunii, na Łotwie i Litwie; lista `INC` w `index.html`, do rozszerzania |

## Skąd biorą się liczby i jak się aktualizują

Do lipca 2026 seria miesięczna jest wbudowana w `index.html` (ISIS, Sztab Generalny, sumy roczne).
Od sierpnia 2026 liczby dzienne przychodzą z porannych komunikatów Sił Powietrznych ZSU
na Telegramie (kanał @kpszsu, publiczny podgląd t.me/s/kpszsu). To ten sam materiał źródłowy,
z którego ISIS i dataset Petra Ivaniuka liczą miesiące, tylko bez pośrednika.

Mechanizm:

1. `scripts/scrape_af.py` czyta podgląd kanału, wyciąga posty „У ніч на …", parsuje liczbę
   ударних БпЛА, збито/подавлено, rakiety z podaną liczbą i „основні напрямки удару".
   Zapisuje do `data/daily.json`. Domyślnie ostatnie 10 dni, z parametrem daty cofa się dalej.
2. `.github/workflows/update-data.yml` uruchamia skrypt codziennie o 06:10 UTC i commituje
   plik, jeśli się zmienił. Commit odświeża GitHub Pages sam.
3. `index.html` przy starcie pobiera `data/daily.json` (ten sam origin, zero CORS), przelicza
   miesiące od sierpnia 2026 i przesuwa koniec osi czasu na ostatni dzień z danymi. Bieżący
   miesiąc ma słupek kreskowany, przeskalowany do pełnych 30 dni. Jeśli pliku nie ma albo
   fetch nie zdąży w 3 s, strona używa wbudowanych wartości i pisze o tym w rogu sceny.

Ograniczenia źródła, nie skryptu: od maja 2026 Siły Powietrzne raportują tylko okno nocne
(18:00–08:00), a od 10 sierpnia 2026 nie podają liczby części typów rakiet. Pole `msl`
w feedzie jest więc dolnym ograniczeniem.

| Okres | Wystrzeleń | Podstawa |
|---|---:|---|
| IX–XII 2022 | ~660 | suma roczna, rozłożona równo |
| 2023 | ~3 300 | 2022 i 2023 razem ok. 4 000 (ISIS) |
| I–IX 2024 | ~552/mies. | 6 987 za I–X minus zmierzony październik |
| X 2024 | 2 023 | Sztab Generalny |
| XI–XII 2024 | ~1 980/mies. | szacunek |
| I–VII 2025 | ~4 127/mies. | suma roczna 54 538 minus zmierzone VIII–XII |
| VIII 2025 – VII 2026 | 62 994 | seria miesięczna ISIS |
| od VIII 2026 | codziennie | feed z @kpszsu |

Do 2024 liczono faktyczne Shahedy, od 2025 wszystkie BSP typu Shahed razem z wabikami.
Licznik narastający miesza dwie definicje, stąd znak przybliżenia.

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

- **Najechanie na obiekt w locie** — typ, cel, punkt startu, ile km i minut zostało do celu
- **Najechanie na obwód** — nazwa i liczba trafień z ostatnich 90 dni symulacji
- **Kliknięcie obwodu** — kamera dolatuje, panel pokazuje udokumentowane naloty w ten obwód
  do bieżącej daty z liczbą potwierdzonych obiektów
- **Kliknięcie znacznika na osi czasu** — skok do daty i odtworzenie nalotu
- **Noc nalotu** — czas zwalnia do ok. godziny na sekundę; HUD pokazuje pasek postępu nocy i przycisk „Pomiń noc”
- **Szpilka poza Ukrainą** — najechanie lub kliknięcie pokazuje, co i kiedy spadło w sąsiednim państwie
- **Widoki** — cały kraj, zachód, front, z góry; płynny przelot kamery
- **Warstwy** — poświata, trasy, obwody, sąsiedzi, cienie, pierścienie zasięgu 400/800/1200 km
- **Klawiatura** — spacja pauza, strzałki ±30 dni, 1/2/3 prędkość, Esc zamyka panel

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
git add index.html README.md scripts data .github .gitignore
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

Nie potrzeba GitHub Actions ani `.nojekyll` — nie ma tu katalogów zaczynających się od
podkreślnika, więc Jekyll niczego nie zje.

## Licencja

Kod: MIT. Dane liczbowe pochodzą z podanych wyżej źródeł i podlegają ich warunkom.
