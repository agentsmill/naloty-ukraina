# Przegląd animacji i danych — 18 września 2026

## Naprawione błędy

| Problem | Poprawka |
|---|---|
| Obiekt dotarł do celu przy `t=1`, ale wybuch następował dopiero przy `t=2` | Zakończenie dokładnie przy końcu trasy; przechwycenie dokładnie w punkcie modelu |
| Noc kończyła się zanim wszystkie obiekty zakończyły lot | Warunek obejmuje zegar, kolejkę, aktywne loty i wygaszenie efektów |
| Nowy obiekt dostawał czas całej klatki sprzed swojego startu | Pozycja wyliczana z czasu od zaplanowanego startu |
| Dwa różne mnożniki czasu dla rakiet i dronów, nieliniowe przyciski prędkości | Jeden zegar modelu, liniowe 1×/3×/8×, stałe tempo po długości krzywej |
| Pauza nie zatrzymywała tła, wybuchów i lotów | Jedna bramka zatrzymuje cały stan animacji |
| Po końcu osi tworzyły się kolejne drony | Faza kończenia aktywnych lotów, następnie nieruchome podsumowanie i przycisk powtórki |
| Start i powtórka pomijały nalot z pierwszej doby | Jawne uruchomienie pierwszego scenariusza |
| Narastające liczniki dublowały się po kliknięciu zdarzenia | Wyliczanie sum z daty, niezależnie od historii kliknięć |
| Rakiety krajowe zwiększały licznik zachodu | Osobne pole `west`, niezależne od typu pocisku |
| Grupy dronów zaokrąglano do wielokrotności pięciu | Ostatnia sylwetka ma wagę odpowiadającą reszcie |
| Widok końca pokazywał następny dzień po ostatnim raporcie | Koniec osi jest granicą wyłączną; etykieta pozostaje na ostatniej dacie danych |
| Miesiące liczono jako 30,4 dnia, niepełne miesiące powiększano do prognozy | Rzeczywista długość miesiąca, liczba obecnych raportów i faktyczne sumy |
| Na mapie można było trafić niewidoczną szpilkę przyszłego zdarzenia | Raycast obejmuje tylko widoczne znaczniki |
| Przy starcie sporadycznie występował ujemny krok czasu | Krok klatki ograniczony także od dołu do zera |

## Korekty treści i danych

- Miesięczna seria VIII 2025 – VII 2026 sumuje się do **66 994**, nie 62 994.
  Tabela korzysta teraz z tej samej serii co licznik, bez ręcznie wpisanej sumy.
- I–VII 2025: rzeczywisty rozkład miesięczny z tabeli ISIS zastąpił siedem identycznych oszacowań.
- Parser rozdziela wystrzelenia, przechwycenia BSP i wszystkie przechwycone cele.
  Przykład 30 VII 2026: **74** wystrzelone rakiety, **55** przechwyconych rakiet;
  **320** przechwyconych celów ogółem, z tego **265** BSP.
- Ukraińska forma „181-м ударним БпЛА” jest rozpoznawana. Wcześniej z raportu 3 VIII
  wybierano późniejsze **14 trafień**, zamiast **181 wystrzelonych BSP**.
- Nieznana pełna liczba rakiet jest `null`, obok znajduje się `msl_min`.
  Pole `uav_down` nie otrzymuje automatycznie łącznej liczby celów z nagłówka.
- 50 wcześniejszych rekordów sprawdzono względem oryginalnych komunikatów.
  W porannej serii 12 IX użyto komunikatu **77891 (129 BSP)** zamiast dziennego
  **77970 (410 BSP)**. Osobna dzienna fala nie jest negowana ani uznawana za duplikat;
  leży poza opisanym zakresem serii. Sierpień: **4620**, 1–17 IX: **2842** BSP.
- Około **163** obiekty z 5 X 2025 dotyczą obszaru dowództwa „Zachód”. Nie przypisujemy
  tej sumy w panelu do obwodu lwowskiego i nie nazywamy jej liczbą trafień.
- Usunięto nieudokumentowane 40/30 obiektów w dwóch scenariuszach oraz podział 82 BSP
  między miasta. Nadal można odtworzyć ogólny scenariusz krajowy tych wpisów.
- Suma zachodu obejmuje wyłącznie wpisy z odnośnikiem do źródła liczby: obecnie
  10 z 6 VII 2023 i około 163 z 5 X 2025. **≈173 jest sumą tego małego wyboru,
  a nie liczbą wszystkich ataków, trafień czy obiektów na zachodzie w całej wojnie.**
- Usunięto losowanie 85–90% przechwyceń bez podstawy dla konkretnego nalotu.
  Pozostaje jawny scenariusz 7 przechwyceń z 10 rakiet z 6 VII 2023.
- Szpilki poza Ukrainą liczą incydenty, nie pociski. Trasy, poświata, godziny modelu
  i statyczna linia frontu mają jawnie opisany ilustracyjny charakter.

Odnośniki do sprawdzonych źródeł i definicje pól są w [README.md](README.md).

## Granice przeglądu

Wczesne sumy 2022–2024, pozostałe opisy historycznych zdarzeń, liczby krajowych salw
w tych wpisach oraz katalog incydentów poza Ukrainą nie mają kompletnej weryfikacji źródłowej
w tym repozytorium. Zachowano je jako opisany wybór i wcześniejsze oszacowania projektu;
nie należy traktować wizualizacji jako pełnej bazy wszystkich ataków.

Poranne raporty nie są pełną statystyką dobową. Braki wymagają osobnego zbioru z zakresem godzin,
źródłami i kontrolą nakładania się okien, zanim będzie można bezpiecznie sumować ataki dzienne
i nocne. Nie wyprowadzamy z tej serii odsetka trafień na zachód ani skuteczności obrony.

## Weryfikacja

Testy Node i Python sprawdzają reguły obliczeń, przejścia stanu odtwarzania i regresje parsera.
Kontrola w przeglądarce obejmuje pauzę, powtórkę, przewijanie, źródła, koniec odtwarzania,
widok telefonu oraz fallback przy niedostępnym pliku danych.

## Aktualizacja 1 października 2026

- Ten przegląd czekał niezacommitowany, a bot dopisywał dane starym parserem. Dni 18–30 IX
  i 1 X pobrano ponownie nowym parserem; wszystkie 50 sprawdzonych dni odtworzyło się bez zmian BSP.
- Parser liczy liczebniki słowne rakiet i bierze przechwycone rakiety jako dolne ograniczenie.
  Zmieniło to wyłącznie pola rakietowe w 10 dniach; każdą zmianę porównano z komunikatem.
- Pobieranie ponawia błędy sieci i puste strony; przy limicie stron skrypt ostrzega zamiast milczeć.
- Katalog incydentów poza Ukrainą ma teraz źródło przy każdym wpisie. Poprawki i nowe wpisy opisuje README.
- Dodano wpis 13 IX 2026: dron w lokomotywę pociągu Kijów–Warszawa ok. 2 km od granicy z Polską.
  Bez liczby obiektów dla zachodu, bo żadne źródło jej nie podało.
- Interakcja: kółko i jeden palec przewijają stronę zamiast blokować ją nad mapą; zbliżenie przez
  Ctrl/⌘ + kółko, dwa palce albo przyciski. Na telefonie opis i liczniki są pod mapą, kamera bliżej.
