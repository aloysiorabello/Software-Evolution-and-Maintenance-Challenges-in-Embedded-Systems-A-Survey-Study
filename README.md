# Software Evolution and Maintenance Challenges in Embedded Systems: A Survey Study

This repository contains the replication package associated with the manuscript:

**Software Evolution and Maintenance Challenges in Embedded Systems: A Survey Study**

Authors: **Aloysio Augusto Rabello de Carvalho** and **Luiz Eduardo Galvão Martins**

## Purpose

The package supports transparency, traceability, and reproducibility of the revised survey analysis. It documents the analytical dataset, questionnaire structure, transformations from survey responses to reported categories, coding rules, figure provenance, and the material required to regenerate the manuscript figures.

## Analytical dataset

The Google Forms export contained 38 submissions.

- The **first 36 submissions** constitute the analytical dataset used in the manuscript.
- These responses were submitted between **9 August 2024 and 28 October 2024**.
- Two later submissions, both dated **12 December 2025**, were created for testing purposes and were excluded from every analysis.
- The public analytical dataset uses stable participant identifiers **P01–P36**.
- Timestamps are omitted from the public analytical dataset.
- The two participants involved in the questionnaire pilot/pretest are **not** part of the 36-response analytical dataset.

## Recruitment

The final survey was disseminated anonymously through WhatsApp groups and e-mail lists within the UNIFESP academic community involving individuals engaged in embedded-software development. Recipients could forward the survey to other eligible practitioners. No individually traceable invitations or predefined individual snowball seeds were used. Consequently, the total recruitment denominator and a reliable response rate cannot be reconstructed.

## Repository structure

```text
.
├── README.md
├── CITATION.cff
├── requirements.txt
├── data/
│   ├── analytical_dataset_anonymized.csv
│   ├── analysis_manifest.json
│   └── verified_counts.json
├── questionnaire/
│   ├── questionnaire_en.md
│   └── questionnaire_header_mapping.csv
├── traceability/
│   ├── category_mapping.csv
│   ├── figure_source_mapping.csv
│   └── quote_traceability.csv
├── coding/
│   ├── rework_frequency_codebook.csv
│   └── rework_frequency_coded_responses.csv
├── scripts/
│   └── generate_figures.py
└── figures/
    └── *.png
```

## Key analytical rules

1. All manuscript results use only **P01–P36**.
2. SQ08 measures **reported maintenance-strategy use**, not strategy effectiveness.
3. SQ14 measures **perceived software-tool effectiveness**.
4. SQ20 records lifecycle phases **reported as affected**; it does not measure impact magnitude.
5. SQ24 is an **open conditional follow-up**, not a Likert-scale item.
6. SQ09 and SQ08 are independent questions; their combined visualization does not imply pairwise challenge-to-strategy relationships.
7. Translations, semantic normalizations, free-text additions, and coding decisions are documented in `traceability/`.
8. Quotations used in the manuscript are linked to stable participant IDs through `traceability/quote_traceability.csv`.

## Unified maintenance and evolution model

SQ10 identified two participants who reported prior use of a unified maintenance and evolution model.

For analyses distinguishing prior experience from expectation-based responses:

- **Prior model experience:** P08 and P35
- **No prior model experience:** the remaining 34 participants

Because the experienced subgroup contains only two participants, subgroup results are descriptive and should not be generalized.

## Reproducing the figures

Install the required Python package:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scripts/generate_figures.py
```

The script reads `data/analytical_dataset_anonymized.csv` and recreates the manuscript figures in `figures/`.

## SQ24 coding

SQ24 asked respondents who reported rework in SQ23 to describe its frequency in free text. Only respondents answering **Yes** to SQ23 are included in the SQ24 frequency analysis.

Responses are coded as:

- **High**
- **Moderate**
- **Low**
- **Not specified / not classifiable**

The coding rules and row-level assignments are available in `coding/`.

## Notes on anonymity

The public dataset excludes timestamps and direct identifiers. Participant IDs (P01–P36) are artificial identifiers assigned according to analytical-response order and are used solely for traceability within this package.

## Repository URL

https://github.com/aloysiorabello/Software-Evolution-and-Maintenance-Challenges-in-Embedded-Systems-A-Survey-Study

## License

No license is assigned by this package automatically. Before public release, the authors should choose and add the license appropriate for the data, documentation, figures, and code.
