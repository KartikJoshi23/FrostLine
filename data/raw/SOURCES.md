# Raw data: sources and licences

Downloaded 24 November 2026. Files are never edited. Checksums are in `checksums.md5`.
The files from Zenodo 24031003, 24124768 and 24124771 match the MD5 values published on their record pages.

| Folder | Source | Licence | Do not commit to a public repository because |
|---|---|---|---|
| zenodo_24031003 | https://zenodo.org/records/24031003 | CC BY 4.0 | Large; cite instead |
| zenodo_24124768 | https://zenodo.org/records/24124768 | CC BY 4.0 | Address lists |
| zenodo_24124771 | https://zenodo.org/records/24124771 | CC BY 4.0 | Address lists |
| zenodo_24124777 | https://zenodo.org/records/24124777 | CC BY 4.0 (README) | Address lists |
| mendeley_62dmsngtfb_v3 | https://data.mendeley.com/datasets/62dmsngtfb/3 | CC BY 4.0 | Court-named addresses |
| ofac_mirror | https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses (lists branch) | MIT (tool) | Address lists |
| opensanctions_il_mod_crypto | https://www.opensanctions.org/datasets/il_mod_crypto/ | CC BY-NC 4.0 | Non-commercial licence; names. `targets.simple.csv` holds only active orders. `nbctf_tron_addresses.csv` was extracted from the full file (688 TRON addresses, order date, status; no names) and is the one to use |
| uk_sanctions | https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv | Open Government Licence v3.0 (linked from the publication page) | Names of people; 50 MB |
| eu_sanctions | https://webgate.ec.europa.eu/fsd/fsf (public CSV 1.1) | European Commission reuse notice | Names of people; 25 MB |
| references | UAE supervisory paper, https://www.centralbank.ae/media/z02hk1ct/jointp-3.pdf | Published by the Central Bank of the UAE; copy kept for reading only | Third-party document |

Names in the sanctions files are never loaded. Only TRON addresses and list dates are used.
