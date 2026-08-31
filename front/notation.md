# Notation and conventions

A reader who wants to check this book rather than trust it needs to know how it
is written. This page states the conventions once.

## Typography

`Monospace` marks anything that exists in a file or on a wire: signal names,
identifiers, coverpoint and property names, code, file paths, and command
fragments. *Italic* marks a term at the point where it is defined, and marks
emphasis of a distinction. **Bold** marks the subject of a paragraph in the
structured boxes described below, and nothing else.

## References and how to check a claim

Citations appear as a superscript number keyed to a numbered list at the end of
the chapter. Numbering is per chapter and follows first appearance, so the same
source can be reference 3 in one chapter and reference 11 in another; the
reference list gives the full citation each time, so no cross-chapter lookup is
needed.

Each entry also carries the identifier of the source in the project's corpus.
That identifier is not decoration: it means the full text of that document was
held and opened, and the claim was checked against the page, not against a
summary or an abstract.

Works the corpus does not hold in full text are never cited for a claim. They
appear, where they are worth knowing about, under **Further reading**, marked as
not held. The distinction is deliberate: a reference is a promise that somebody
opened the document.

## Standards

A normative document is identified the first time a chapter relies on it, by
issuing body, designation, issue or version, and — where a specific requirement
is asserted — clause. For example, a requirement of the AXI4 protocol is
attributed to *AMBA AXI and ACE Protocol Specification*, ARM IHI 0022H.c
(ID012621), with the clause that states it. The designation is given in the form
the document itself prints, which is not always the form catalogues use.

Two consequences follow, and both matter for checking. First, the issue is part
of the citation, because specifications change: the current issue of Arm IHI 0022
no longer contains AXI4 at all, so an AXI4 requirement can only be attributed to
the last issue that specifies it. Second, where a requirement is quoted rather
than paraphrased, the quotation is short and marked as a quotation, so that a
reader can see where the specification's words end and this book's begin.

## Pointers into this book, and pointers out of it

A section sign followed by a bare number always points inside this book: §7.3 is
the third section of Chapter 7. It never means a section of anything else, so a
reader who follows one never leaves the volume.

A clause of an external document is always preceded by that document's
designation, and its clause identifier carries the form that document uses —
Arm IHI 0022H.c §A5.2.2, IEEE 1800-2023 §16.12. The designation is what
disambiguates: without one, the pointer is this book's. Where a document numbers
its sections in the same bare style this book does, the word is spelled out
instead, as in *the integration specification, section 3.2*, so that no bare §N.M
in these pages can be mistaken for an outside reference.

## Figures and tables

Every figure and every table is numbered by chapter — Figure 8.1 is the first
figure of Chapter 8 — and carries a caption that says what the reader is looking
at without requiring the surrounding paragraph. Figure captions sit below the
figure, table captions above the table. Cross-references use the number, and the
lists of figures and tables in the front matter give the page.

The numbers are assigned by the build from symbolic labels in the sources, so a
reference in the text and the float it points at cannot drift apart when a figure
is inserted or removed. A reference to a label that does not exist, and a label
defined twice, both fail the build rather than producing a wrong number. An
uncaptioned figure or table is reported by the build with its line number, so
the guarantee in the paragraph above is **checked on every build rather than
asserted**.

No figure or table in this book is reproduced from a standard or from another
publication. Where a diagram of something a specification defines is needed, it
is drawn for this book from the specification's text.

## The chapter apparatus

Chapters open with a statement of the problem on one of the example systems, in
engineering terms, followed by a paragraph mapping the sections. Four structured
elements recur:

**Scenario** boxes state a situation, the approach taken and the reason it is the
right approach, in that order. They are constructed examples on the example
systems unless a source is cited.

**In practice** boxes report what teams do, including the parts that are
inconvenient. Each is either cited to a published source or marked as a
constructed illustration; the book does not present unsourced practice as
reporting.

**Pitfalls** list common mistakes as a symptom and a cure, on the assumption that
a reader recognises the symptom before the cause.

**Summary** closes the chapter with the claims it established, not with a recap
of its topics.

## The example systems

Bare names refer to the **reference SoC**: "the crossbar", "the DMA engine", "the
core", "the neural accelerator" are that system's blocks, with the parameters
fixed in the front matter of Chapter 1 and unchanged thereafter. Parts of the
larger, later **flagship SoC** are always qualified as such — "the flagship's
compute cluster", "the flagship's mesh NoC" — because several blocks exist in
both generations at different scales, and an unqualified name would read as the
same block twice.

A supporting cast of other devices — a safety-critical microcontroller, a secure
element, an analog front end, and a set of IP blocks including a GPU, a video
codec, an Ethernet controller and a flash controller — appears where a point
needs a device the reference SoC does not have. These are introduced where they
are used.

## Vocabulary

The glossary in Appendix A is binding, not summarising: where it defines a term,
this book means that and nothing else. One case is worth flagging here because
the industry uses the word both ways. **Validation** in this book means checking
a design on real hardware — on fabricated silicon, or in the lab on a prototype.
Everything done on a model, before there is hardware, is **verification**. The
distinction being drawn is hardware against model, not fabricated against
programmable.

## Quantities

Memory sizes and address boundaries are powers of two: 4 KB is 4,096 bytes, and
the 4 KB boundary of the AXI protocol is that boundary. Data rates and clock
frequencies are powers of ten: 200 MHz is 200 × 10⁶ Hz. Large ratios are written
in scientific notation, as 10¹², when the exponent is the point being made.

Two protocol encodings recur and are stated wherever they are used, because both
are a common source of off-by-one errors: a burst length field encodes the number
of beats minus one, and a coverage bin count is a count of cells in a model, not
of tests.

Where a quantity in an example can be derived from that example's published
parameters, the derivation is given. Where it cannot, its source is cited. A
number with neither is a defect, and finding one is worth reporting.
