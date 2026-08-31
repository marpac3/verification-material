# Verification Material

Materiale didattico e di riferimento sulla **verifica funzionale dell'hardware**: un
manuale di 502 pagine e sette lezioni in slide, con ogni affermazione quantitativa
ancorata alla fonte primaria e alla pagina.

I contenuti sono in **inglese**. Questo README è in italiano perché descrive il
funzionamento del repository, non il materiale.

---

## Cosa c'è dentro

### Il manuale — *Hardware Verification: A Holistic Guide*

26 capitoli, **502 pagine**. Copre l'intero perimetro: dai fondamenti (cosa significa
"verificato", perché la copertura non è una misura di qualità) ai metodi dinamici
(constrained-random, coverage-driven, UVM), ai metodi formali (model checking,
equivalence checking, assertion-based), all'emulazione e alla verifica di sistema, ai
domini specializzati (safety, security, low-power, analog-mixed-signal), fino al
post-silicio e all'uso dei modelli linguistici nel flusso di verifica.

Sorgente in `book/` (Markdown, un file per capitolo). PDF già costruito in
`build/hardware_verification_guide.pdf`.

### Le sette lezioni

**296 slide**, HTML autonomo — si aprono in qualsiasi browser, nessuna dipendenza da
installare — più il PDF corrispondente.

| Deck | Capitoli | Slide |
|---|---|---|
| `part1_foundations` — Fondamenti | 1-4 | 37 |
| `part2_planning_measurement` — Pianificazione e misura | 5-7 | 32 |
| `part3_dynamic_verification` — Verifica dinamica | 8-12 | 49 |
| `part4_static_formal` — Metodi statici e formali | 13-16 | 44 |
| `part5_beyond_rtl` — Oltre la simulazione RTL | 17-20 | 46 |
| `part6_specialized_domains` — Domini specializzati | 21-23 | 43 |
| `part7_human_and_machine` — L'uomo e la macchina | 24-26 | 45 |

---

## Struttura

```
book/          i 26 capitoli in Markdown — la fonte editabile
front/         frontespizio e apparati preliminari
slides/        i 7 deck (HTML + PDF) e check_deck.py
tools/         build del libro e controlli automatici
meta/          i sei file di apparato necessari alla build (vedi sotto)
build/         il PDF finale del libro; il resto è rigenerabile
```

### `meta/` — cosa c'è e cosa manca

Sei file, quelli che servono a ricostruire il libro e a capire le sue convenzioni:

- **`references.md`** — la bibliografia: la mappa da `[cit:ID]` alla voce completa. In
  fondo, le *note di provenienza*: per ogni fonte in cui sede o anno non erano stampati
  nel documento, come sono stati risolti e su quale evidenza. È la parte che rende il
  materiale verificabile da un lettore esterno.
- **`corpus_index.md`** — l'inventario delle fonti citabili, con numero di pagine.
- **`glossary.md`** — il glossario; la build lo rende come Appendice A.
- **`outline_master.md`** — la struttura del libro, letta dalla build.
- **`style_guide.md`** — le convenzioni redazionali.
- **`example_bank.md`** — gli esempi hardware ricorrenti e i loro numeri.

**Cosa non è qui.** L'apparato editoriale completo — i registri delle fonti con gli
estratti verbatim, le 26 review capitolo per capitolo, gli audit numerici e di coerenza —
resta interno. Non per riservatezza: quei file contengono il testo *letterale* di standard
IEEE e di paper, copiato per controllare che le nostre parafrasi non tradissero la fonte.
Come apparato di lavoro privato è uso legittimo; pubblicarlo sarebbe riprodurre testo
protetto. Se lavori con noi e ti serve, chiedi accesso al repository interno.

---

## Ricostruire il materiale

Serve Python 3.12 con WeasyPrint.

```bash
PY=/percorso/al/tuo/python3.12

# Il libro completo (26 capitoli → HTML + PDF)
CH=$(for i in $(seq -w 1 26); do echo -n "ch$i "; done)
$PY tools/build_book.py --chapters $CH --out-base build/hardware_verification_guide

# Un sottoinsieme, per iterare in fretta
$PY tools/build_book.py --chapters ch13 ch14 --out-base build/prova
```

Entrambi gli argomenti sono obbligatori, e `--chapters` vuole gli **stem** dei file
(`ch01 ch02 …`), non i numeri.

---

## I controlli automatici

Servono a impedire che una revisione introduca un errore silenzioso — il modo tipico in
cui un manuale tecnico si degrada: qualcuno migliora una frase e nel farlo cambia un
numero, una citazione o un termine che aveva un significato preciso.

### `tools/check_invariants.py` — il gate degli invarianti

Confronta un capitolo prima e dopo una modifica e segnala se sono cambiati elementi che
una revisione *stilistica* non dovrebbe toccare: numeri, identificativi di citazione,
riferimenti incrociati, termini a significato vincolato.

```bash
$PY tools/check_invariants.py snapshot --dest .gate_baseline_$(date +%Y%m%d)
# ... modifiche ...
$PY tools/check_invariants.py check --before .gate_baseline_AAAAMMGG --policy A1 --chapters ch03
```

Due trappole, per chi legge il codice: la tupla di policy è `(add_fatal, rem_fatal)` e dice
se una modifica è **fatale**, non se è permessa; e il controllo di additività (G3) gira
**solo** sotto policy `B`, non sotto `A1`.

### `slides/check_deck.py` — il gate delle slide

Apre ogni slide in un browser headless e verifica che il testo non sbordi fuori dalla
pagina proiettata. Circa 4 secondi per slide.

```bash
$PY slides/check_deck.py slides/part1_foundations.html
```

Attenzione: lo script **esce con codice 1 anche solo per avvisi sul conteggio parole**. La
condizione di successo è **zero righe `OVERFLOW`**, non l'exit code.

---

## Diritti

Il testo è opera originale. Le fonti sono citate come **parafrasi attribuite** con numero
di pagina, non riprodotte: nessun documento di terzi è incluso in questo repository, e le
fonti primarie in PDF non ne fanno parte e restano soggette alle licenze dei rispettivi
editori.

**Licenza non ancora scelta.** Fino a quel momento vale il default: tutti i diritti
riservati agli autori. Il materiale è leggibile e citabile, ma non ancora riutilizzabile:
per riusarne parti, chiedi.

## Cosa resta aperto

- Sei citazioni nei deck nominano la fonte senza il numero di pagina. Le affermazioni
  corrispondono alla bibliografia, quindi non sono errori: è che non sono verificabili in
  un secondo da chi legge.
- `part4`, slide 24: un risultato è formulato in modo cautelativo anziché empirico;
  `book/ch14.md` lo attribuisce a `[cit:D31]` e sarebbe ripristinabile.

## Contribuire

Le modifiche vanno su un branch, non su `main`. Prima di aprire una pull request:

1. ricostruisci il libro e verifica **zero warning**;
2. se hai toccato i deck, esegui `check_deck.py` sui deck modificati e verifica **zero
   `OVERFLOW`**;
3. se hai cambiato una cifra o una citazione, aggiorna `meta/references.md` con documento
   **e pagina**.

Il punto 3 è quello che conta. Una cifra senza pagina non è verificabile, e questo
materiale vale esattamente quanto la sua verificabilità.
