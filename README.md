# Hardware Verification: A Holistic Guide

Manuale in inglese sulla verifica funzionale dell'hardware, con 26 capitoli,
quattro appendici, indice analitico e 139 esercizi con soluzioni. Il corso comprende
ora sette lezioni da 90 minuti, con slide essenziali, handout completi e note del
docente separate: 21 PDF, oltre alle versioni HTML.

[Apri i materiali delle sette lezioni](slides/README.md).

[Leggi o scarica il PDF](build/hardware_verification_guide.pdf).

## Materiali

- `book/`: capitoli e appendici B, C e D in Markdown.
- `front/`: frontespizio, copyright, prefazione e convenzioni.
- `meta/glossary.md`: sorgente dell'Appendice A.
- `meta/index_terms.md`: termini e alias dell'indice analitico.
- `meta/book_manifest.txt`: ordine completo dei file del libro.
- `slides/`: sette lezioni, sette handout e sette note del docente; i deck
  storici restano come sorgenti del materiale di studio.
- `tools/`: generazione del libro e controlli disponibili nella distribuzione.

## Ricostruire il libro

La build usa Python con Markdown, Pygments, WeasyPrint e PyMuPDF, `pdftotext`
(Poppler), Node.js e i renderer `@mermaid-js/mermaid-cli` e `wavedrom-cli`.
WeasyPrint richiede anche le proprie librerie di sistema. I renderer vengono
richiamati tramite `npx`; senza pacchetti già disponibili serve accesso al registry.

```bash
python tools/build_book.py --with-index --out-base build/hardware_verification_guide
```

Il manifesto include tutte le appendici. La build con `--with-index` produce una
prima versione, ne ricava le pagine dei termini e genera la versione con indice,
controllando che l'aggiunta non sposti i capitoli già indicizzati.

I frammenti SystemVerilog dichiarati come tali richiedono il contesto indicato
nel testo. Un controllo sintattico non sostituisce l'esecuzione nel relativo
ambiente UVM né una prova del comportamento del circuito.

## Provenienza della distribuzione

Il ramo pubblico contiene il testo del libro e i file necessari alla sua build.
I PDF delle fonti, gli estratti di lavoro, le review editoriali, i log e le
conversazioni degli agenti restano fuori da questa distribuzione. I riferimenti
bibliografici identificano le fonti senza includerle.

I controlli automatici coprono struttura, citazioni, invarianti, glossario,
rimandi, frammenti e generazione dell'indice. Gli esercizi sono stati risolti
separatamente e confrontati con l'Appendice D. Il materiale conserva limiti e
assunzioni espliciti. Lezione 1 approvata dall’autore; revisione finale del corso
e lettura dei capitoli 22, 19, 15 e 23 restano disponibili come revisione editoriale.
Il rilascio GitHub non aggiorna gli eventuali artifact ospitati su Claude.

## Licenza

Copyright Fondazione Chips-IT. Il testo originale del libro è distribuito con
licenza **CC BY-NC-SA 4.0**, riportata in [LICENSE](LICENSE) e nel frontespizio.
Le opere citate e i materiali dei rispettivi autori conservano i propri diritti.
