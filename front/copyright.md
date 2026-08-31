# Hardware Verification: A Holistic Guide

Marco Paci · ChipsIT

First internal edition, August 2026.

© 2026 ChipsIT. All rights reserved.

<hr class="cp-rule" />

**Purpose of this edition.** This edition is prepared for internal use: as a
reference for engineers doing verification work, and as teaching material for
engineers moving into verification from design. It is not a vendor document and
recommends no commercial tool.

**Sources.** Every numbered reference in this book resolves to a document held in
full text, and every claim carrying a reference was checked against the page
cited rather than against recollection of it. Where the literature does not
settle a question, the book says so. Where a figure comes from a single source,
that source and its date are named, because a statistic without a date is not a
statistic.

**Example systems.** The reference SoC and the flagship SoC used throughout are
constructed teaching examples with fixed, published parameters. They are not any
company's product, and no claim about them should be read as a claim about
silicon. Claims about real organisations are a separate matter and are made only
where a published source states them; each is cited to that source.

<hr class="cp-rule" />

**Trademarks.** AMBA is a registered trademark of Arm Limited (or its
subsidiaries or affiliates) in the US and/or elsewhere; Arm publishes trademark
usage guidelines at arm.com. AXI, AHB, APB and ACE are protocol designations
within the AMBA family and are used here descriptively. IEEE is a registered
trademark in the U.S. Patent and Trademark Office, owned by The Institute of
Electrical and Electronics Engineers, Incorporated. Verilog is a registered
trademark of Cadence Design Systems, Inc. Other product, organisation and
standard names appearing in this book may be the trademarks of their respective
owners. They are used editorially, in the owner's favour, with no intent to
infringe.

**No endorsement.** None of the organisations whose specifications, publications
or results are cited in this book has reviewed, approved, sponsored or endorsed
it. That includes Arm, IEEE, Accellera, RISC-V International, and every company
named in a cited case study. Where this book characterises a published result,
the characterisation is the author's and any error in it is the author's.

**Quotation from standards.** Short passages of normative text are quoted, with
attribution to the document, its issue and its clause, for the purpose of
identifying and explaining the requirement under discussion. Those quotations
rest on the statutory right of quotation for purposes of criticism, review,
illustration and teaching — Article 5(3)(d) of Directive 2001/29/EC as
implemented in national law — and **not** on any specification licence: the AMBA
specification licence grants copying for the purpose of developing products that
comply with the specification, which is not the purpose of this book, and the
specifications' proprietary notices reserve reproduction to the publisher's
written permission. Accordingly no standard is reproduced in whole or in
substantial part, and **no figure or table from any standard is reproduced**;
where this book needs a diagram of something a standard specifies, the diagram
is drawn from scratch. Reproducing a figure or a table would require written
permission, which attribution does not substitute for.

**Assistance disclosure.** This book was written with substantial assistance
from large language models. The systems used were Anthropic's Claude — models in
the Claude Opus family for drafting, adversarial review and page-level citation
checking, and a Claude Fable model for orchestration across chapters. The tools
are not authors: responsibility for every claim, and for the decisions about
what the book argues, rests with the named author. The editorial procedure — a
closed source corpus, an independent review pass for each chapter, page-level
verification of citations, and mechanical gates on numbers, code, hedges and
cross-references — is described in the preface, together with its known ceiling,
so that a reader who wants to judge the method can.

**Errors.** Corrections are welcome and will be recorded. An error found in a
book of this size is a contribution to it, not an embarrassment to it.
{: .cp-note }
