# Seven lessons — course materials

Each lesson is designed for 90 minutes: 22 projection slides, four discussions, one book exercise, a complete study handout and separate teaching notes.

| Lesson | Projection | Study handout | Teaching notes |
|---|---|---|---|
| 1. Foundations | [PDF](lesson1_foundations.pdf) · [HTML](lesson1_foundations.html) | [PDF](handout1_foundations.pdf) · [HTML](handout1_foundations.html) | [PDF](notes1_foundations.pdf) · [HTML](notes1_foundations.html) |
| 2. Planning and measurement | [PDF](lesson2_planning_measurement.pdf) · [HTML](lesson2_planning_measurement.html) | [PDF](handout2_planning_measurement.pdf) · [HTML](handout2_planning_measurement.html) | [PDF](notes2_planning_measurement.pdf) · [HTML](notes2_planning_measurement.html) |
| 3. Dynamic verification | [PDF](lesson3_dynamic_verification.pdf) · [HTML](lesson3_dynamic_verification.html) | [PDF](handout3_dynamic_verification.pdf) · [HTML](handout3_dynamic_verification.html) | [PDF](notes3_dynamic_verification.pdf) · [HTML](notes3_dynamic_verification.html) |
| 4. Static and formal verification | [PDF](lesson4_static_formal.pdf) · [HTML](lesson4_static_formal.html) | [PDF](handout4_static_formal.pdf) · [HTML](handout4_static_formal.html) | [PDF](notes4_static_formal.pdf) · [HTML](notes4_static_formal.html) |
| 5. System execution and silicon | [PDF](lesson5_system_silicon.pdf) · [HTML](lesson5_system_silicon.html) | [PDF](handout5_system_silicon.pdf) · [HTML](handout5_system_silicon.html) | [PDF](notes5_system_silicon.pdf) · [HTML](notes5_system_silicon.html) |
| 6. Analog, safety and security | [PDF](lesson6_specialized_domains.pdf) · [HTML](lesson6_specialized_domains.html) | [PDF](handout6_specialized_domains.pdf) · [HTML](handout6_specialized_domains.html) | [PDF](notes6_specialized_domains.pdf) · [HTML](notes6_specialized_domains.html) |
| 7. Engineering practice and automation | [PDF](lesson7_practice_ml_future.pdf) · [HTML](lesson7_practice_ml_future.html) | [PDF](handout7_practice_ml_future.pdf) · [HTML](handout7_practice_ml_future.html) | [PDF](notes7_practice_ml_future.pdf) · [HTML](notes7_practice_ml_future.html) |

The study handouts retain all 296 historical panels. Their source lines remain visible. Section-level source ranges are embedded in every projection slide; historical handouts use chapter ranges, with explicit annotations for bibliographic locators, internal pointers, spelled-out numbers and retained illustrative calculations. These annotations are restricted to unchanged historical text.

Projection text is at least 18 pt, with at most 60 rendered words per page. Timing, discussion guidance, assigned exercise guidance and expected reasoning are in the teaching notes.

## Rebuild

Use Python with BeautifulSoup4, WeasyPrint 52.5 and PyMuPDF, plus Poppler. The book renderer also requires its documented Markdown and diagram dependencies.

```bash
python tools/build_lessons.py --out-dir /path/to/artifacts/slides
python tools/check_lessons.py /path/to/artifacts/slides
```

The historical `part*.html` files are retained as source dependencies. Generated PDFs are presentation and study artifacts; displayed SV excerpts still require the context described in the book.

Use the `lesson`, `handout` and `notes` PDFs listed above for this edition. The older `part*.pdf` files are archival outputs, not the regenerated study handouts.
