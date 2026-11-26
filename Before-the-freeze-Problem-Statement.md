**Problem statement**

# Before the freeze: early warning for USDT accounts on TRON that Tether later freezes

AI in Finance group project, crime domain  
SP Jain School of Global Management, Dubai  
Team: Kartik Joshi, Prem Kukreja, Samuel Alex, Gagandeep Singh  
November 2026. Facts as verified on 23 November 2026; corrected on 24 November 2026 (see section 17).

---

## 1. The problem in one sentence

> Laundering through USDT on the TRON network is documented on several continents, but Tether's freezes act after the fact and unevenly. This project asks whether accounts that end up frozen can be told apart, from their public on-chain activity, before the freeze becomes public.

## 2. Summary

FATF, UNODC (for East and Southeast Asia), a UAE supervisory paper and US court papers all name USDT on TRON as a laundering rail. Criminal proceeds pass through unhosted wallets, outside anti-money-laundering (AML) checks, then leave through OTC brokers, P2P traders or underground banking. Tether can freeze addresses, but FATF describes this as a reactive control. A public analysis found that Tether had frozen all 355 addresses it checked on US, UK and EU sanctions lists, but only 2 of 642 addresses named in fraud court rulings. Using Tether's public freeze events as imperfect labels, this project asks five things:

- how later-frozen accounts differ from comparable accounts before they are frozen;
- how early that difference shows;
- what networks those accounts form;
- how much of the signal reflects sanctions-driven freezes rather than fraud or laundering;
- what share of value reaches an apparent off-ramp before a freeze.

## 3. Background

USDT on TRON is a documented laundering rail on several continents, and its main brake, Tether's freeze, works after the fact and unevenly.

Stablecoins now carry most illicit crypto money. FATF reports that stablecoins are the asset most used in illicit transactions. Citing Chainalysis, a private analytics firm, it puts their share at 84% of the US$154 billion in illicit virtual-asset transaction volume in 2025 (FATF, 2026, paras 2 and 29).

USDT on the TRON network appears in official and court material from several regions:

- **Global (FATF).** North Korean launderers often convert stolen funds into USDT on TRON before cashing out. Drug networks use it to pay overseas suppliers of precursor chemicals (FATF, 2026, paras 33 and 38).
- **East and Southeast Asia (UN).** In January 2024, UNODC called USDT on TRON a preferred choice for fraudsters and money launderers in the region. Tether and TRON disputed that finding at the time (DL News, 2024).
- **United States (court).** A network that laundered over US$1 billion for clients, including drug trafficking organisations, ended in a 12-year prison sentence in November 2026 (U.S. Attorney's Office, 2026b). Court papers at the charging stage, as reported by DL News, put USDT on TRON at its centre (Di Salvo, 2026).
- **United Arab Emirates (supervisor).** A UAE supervisory paper on stablecoins says TRON is particularly popular for illicit transactions. It says firms should build scenario rules for USDT on TRON (Supervisory Subcommittee, n.d., sections 3.1 and 6.5).

## 4. The problem

Laundering on this rail runs in three steps, each described by FATF (FATF, 2026):

1. Criminal proceeds, for example from scams, drug sales or sanctions evasion, are turned into stablecoins, sometimes through OTC brokers (Annex A).
2. The coins hop between unhosted wallets. FATF calls these peer-to-peer transfers a key vulnerability, since no AML-obliged intermediary takes part (paras 3 and 48).
3. The coins leave through OTC brokers or P2P platforms, some of them unlicensed (paras 33 and 47). In some cases stablecoins are used to settle underground-banking deals (para 39).

The main brake on the rail is the issuer. Tether can freeze an address so that its USDT cannot move. FATF describes this as a more reactive control, typically set off when law enforcement contacts the issuer or when a wallet appears on a national sanctions list (FATF, 2026, paras 54 and 66). Tether does not publish its reasons, although every freeze is a public on-chain event (Bitquery, 2026). On TRON, freezes since early 2021 are first proposed in a 2-of-3 multisig wallet, so the target is public before the freeze takes effect (FreezeCheck, 2026b; our own reading of the contract, 24 November 2026). A frozen address can still receive USDT (Bitquery, 2026).

Issuer practice is changing. The T3 Financial Crime Unit run by TRON, Tether and TRM Labs reportedly disbanded in August 2026, and TRON, Tether and Chainalysis announced a new Digital Crime Task Force on 12 November 2026 (Vardai, 2026).

### What the project studies: each wallet's public record before any freeze

*(Figure 1 is a diagram in the PDF; it is reproduced here as a table and notes.)*

| Step | Stage | Detail | Marking in the figure |
|---|---|---|---|
| 1 | Criminal proceeds | from scams, drugs or sanctions evasion | *off-chain* (dashed grey) |
| 2 | Turned into USDT | sometimes through an OTC broker | public record on TRON (green) |
| 3 | Hops between wallets | on TRON, often unhosted, no AML intermediary | public record on TRON (green) |
| 4 | Cash-out | OTC broker, P2P trader or underground banking | *payout is off-chain* (dashed grey) |

- Banner above steps 2 to 3: "What the project studies: each wallet's public record before any freeze".
- Marker at step 3, labelled **Tether freeze**: "locks the wallet's USDT, usually after police contact or sanctions".
- Annotation between step 3 and step 4: "*money may leave first*".

**Figure 1.** The laundering rail and the window the project studies. Green marks the public record on TRON; dashed grey marks steps that happen off-chain and are not in the data. Steps follow FATF (2026).

## 5. Evidence of scale

- **Freezes on TRON.** By 12 August 2026 Tether had frozen 7,987 TRON addresses in 8,017 freeze events. Those addresses held US$3.83 billion at the moment they were frozen (Bitquery, 2026). These counts cover every address ever frozen. On 8 November 2026, 8,206 addresses were still frozen (FreezeCheck, 2026); on the same ever-frozen basis the count had reached 9,191 (our count from the USDT contract's events, 24 November 2026).
- **UAE example.** Between July 2023 and June 2025 the UAE Financial Intelligence Unit analysed over 800 virtual-asset suspicious transaction reports. About 38% concerned fraud and scams (Kochar et al., 2026, summarising the UAE FIU report).
- **Swiss example.** Switzerland's Financial Intelligence Unit, MROS, received 2,873 suspicious activity reports linked to virtual currencies in 2025, up 59.7% on the previous year (MROS, 2026, p. 25).

## 6. Why current controls fall short

- **No intermediary in the middle.** P2P transfers between unhosted wallets sit outside AML/CFT obligations (FATF, 2026, para 48).
- **Freezes follow official action.** A public analysis checked Tether's TRON freezes against six groups of addresses (Figure 2). Nearly all sanctioned addresses were frozen. Addresses from fraud court rulings, drainer wallets and address-poisoning factories almost never were. The authors note that some court-listed addresses may belong to victims or intermediaries (FreezeCheck, 2026). FreezeCheck also sells freeze-risk checks, and its article is marked AI-assisted.
- **Timing is uneven.** Some addresses were frozen before their sanctions designation. One sanctioned exchange was frozen three days after its designation, by which time about 2.46 million USDT had already left (FreezeCheck, 2026).

### Tether froze all 355 US, UK and EU-listed addresses, but 2 of 642 from fraud rulings

*Share of each list of TRON addresses frozen by Tether, as of 8 November 2026*

*(Figure 2 is a bar chart in the PDF; it is reproduced here as a table.)*

| List of TRON addresses | Share frozen | Frozen / listed |
|---|---|---|
| US, UK and EU sanctions lists | 100% | 355 of 355 |
| Israel NBCTF seizure list | 93% | 633 of 678 |
| US civil forfeiture complaints | 70% | 222 of 319 |
| Taiwanese fraud court rulings | 0.3% | 2 of 642 |
| Drainer wallets (rule-based) | 0% | 0 of 369 |
| Address-poisoning factories (rule-based) | 0% | 0 of 17 |

**Figure 2.** Freeze coverage by address list. Source: FreezeCheck (2026), a public analysis that is not peer reviewed. Addresses named in court papers may belong to victims or intermediaries, so an unfrozen one is not proof of a missed crime.

Freeze labels therefore record when the issuer acted, mostly after sanctions or police requests. They are not a full map of laundering accounts, and the project has to treat them as noisy labels. FATF's description of issuer freezing as more reactive, typically following outreach from law enforcement or identification on a national sanctions list, fits this pattern (FATF, 2026, para 66).

Freezes are also not independent or final. By our count, 78% of frozen addresses sit in batches of five or more, with ten minutes or less between neighbours. On 14 May 2026, 447 TRON addresses were released within 26 minutes (FreezeCheck, 2026c).

## 7. Who is affected

- **Fraud victims.** Their money is turned into crypto and cashed out abroad. According to India's Enforcement Directorate, money taken through impersonation fraud in one case was converted into crypto and cashed out through hawala operators and individuals in the UAE (News on AIR, 2025).
- **Unwitting P2P counterparties.** An Indian man sold 5,617.97 USDT for Rs 3 lakh in a P2P trade. After fraud complaints were linked to that trade, his whole bank account was frozen, although he was not an accused person. The High Court lifted the freeze and kept a lien only on the disputed Rs 3 lakh (Madras High Court, 2025).
- **Exchanges and banks.** They must decide on every cash-out. In a case study in the UAE supervisory paper, a licensed virtual asset service provider holds a customer's cash-out into dirhams after fast USDT-on-TRON hops. It then investigates and reports the case if the pattern fits laundering (Supervisory Subcommittee, n.d., Case Study E).

## 8. The cross-border cash-out leg

The last step of the rail can cross borders. FATF describes stablecoins being used to settle underground-banking deals (FATF, 2026, para 39). One FATF case study, titled as the remuneration of trafficked humans, describes Indians working in scam centres, mainly in Cambodia and Myanmar, whose pay reached family in India through accounts that were funded with USDT, converted straight away and withdrawn in rupees (FATF, 2026, Box 3). It is a case about trafficked people, not about launderers. Indian investigators say they have also traced crypto from fraud to cash-outs through hawala operators in the UAE (News on AIR, 2025). In the US case, according to court documents, most outbound funds went to businesses and individuals in the United States and overseas, including Colombia, China, Panama and Mexico (U.S. Attorney's Office, 2026b).

This leg is part of the problem, but it is treated as context and as research question 5. The payouts themselves happen off-chain, through cash, bank transfers, exchange houses or hawala. No public data links them to TRON addresses.

## 9. Aim

The project aims to establish whether, and how early, accounts that Tether later freezes can be told apart from comparable accounts. It uses only their public activity before the freeze became public, which is when it was proposed. It also asks what the answer shows about the limits of issuer freezes as a control.

## 10. Research questions

- **RQ1** How different, before the freeze, is the observable activity of later-frozen accounts from that of comparable unfrozen accounts?
- **RQ2** How early before a freeze, if at all, do those differences show up?
- **RQ3** What groups or network structures do frozen accounts form? Do any match documented red flags, such as rapid inflow and outflow, fast hops between wallets, cross-chain bridging or quick cash-outs (FATF, 2026, Annex A; Supervisory Subcommittee, n.d., Case Study E)?
- **RQ4** How much of the "frozen" signal reflects sanctions-driven freezes rather than fraud or laundering, and what does that do to any conclusion?
- **RQ5** What share of value reaches an apparent off-ramp before a freeze? What can and cannot on-chain data say about the cross-border cash-out leg?

## 11. Scope and limits

**In scope**

- USDT (TRC-20) accounts on TRON
- Tether freeze, unfreeze and destruction events, and the proposals that precede freezes
- Each account's activity before its freeze was proposed
- The transfer network around frozen accounts
- Only information available before each freeze became public

**Out of scope**

- Other blockchains and tokens
- Predicate crimes as separate targets
- Bank, exchange-house and remittance records
- Identifying any person
- Any claim that a given address is criminal

The geographic scope is global. The UAE is one documented example, alongside cases from Asia, Europe and the Americas. The crime in focus is a single one: money laundering through USDT on TRON. Fraud, scams, drug trafficking, sanctions evasion and hacks appear only as the sources of the money.

## 12. Data available

The data is real and public, and free within normal quotas. No synthetic data is used for training.

| Source | What it covers | Licence or terms |
|---|---|---|
| **Zenodo labelled dataset** (Muhammad et al., 2026) | 16,461 TRON USDT accounts: 7,212 frozen and 9,249 normal. Each has 21 features, cut before its freeze or pseudo-freeze time. Labels come from Tether's AddedBlackList and RemovedBlackList events. Built for evaluation that trains on the past and tests on the future. Published 7 November 2026. | CC BY 4.0 |
| **Google BigQuery TRON tables** (Google Cloud, n.d.-c) | Blocks, transactions, logs, receipts and decoded events for the whole TRON chain, in `bigquery-public-data.goog_blockchain_tron_mainnet_us`. Source of USDT transfers. | Public dataset in Preview. The first 1 TiB of queries each month is free (Google Cloud, n.d.-a, n.d.-b) |
| **TronGrid API** | Freeze, unfreeze and destruction events, and multisig proposals, read from the contracts. Source of labels and proposal times. | Free key; terms dated 24 September 2026 |
| **Sanctions lists**: OFAC (through a dated public mirror), UK, EU, and Israel's NBCTF (through OpenSanctions) | TRON addresses on public lists, for RQ4. To the end of 23 November 2026: 1,038 distinct TRON addresses, 993 of them ever frozen. | MIT (mirror tool); Open Government Licence v3.0; European Commission reuse notice; CC BY-NC 4.0 |
| **Taiwanese court labels** (Tsai, 2026) | 638 TRON addresses named in criminal judgments as fraud platforms or pseudo brokers, with victims' addresses withheld. 212 were active on or after 1 July 2024. | CC BY 4.0 |
| **FreezeCheck data** (FreezeCheck, 2026, 2026b, 2026c) | Proposal windows, list coverage, releases and destructions, used to cross-check our own counts. | CC BY 4.0 |

**Known gaps.** The Zenodo record describes three files that are not in its file list: a graph file (1,788,383 nodes and 9,756,607 edges), a label file (8,889 frozen accounts) and a raw edge file. Its notebook does name the 21 features, the time window (from 1 January 2024) and how normal accounts were chosen: addresses active on 11 fixed days, with reference dates drawn at random from real freeze dates. Normal accounts are therefore not matched to frozen ones, and some could be selected using activity after their reference date. Frozen accounts with no transfer history are missing. Labels came from the TronGrid API and transfers from BigQuery. No public source gives a country or owner for TRON addresses, none records the off-chain bank or remittance legs, and we know of no complete public list of exchange addresses.

## 13. Significance

- **It tests a control that supervisors already rely on.** The UAE supervisory paper says firms should monitor issuer blacklists and freezes, and that their analytics may include them (Supervisory Subcommittee, n.d., sections 3.1 and 6.5). If risk shows before the freeze, firms could act sooner; if it does not, that limit is worth knowing.
- **It speaks to a FATF concern.** FATF asks jurisdictions to monitor the volume and risk of P2P transactions through unhosted wallets (FATF, 2026, recommendation VI). This project does not measure that volume; it tests whether risk on this rail can be seen early from public data.

## 14. Ethical and legal limits

- A freeze is Tether's decision, not a court finding, and its reasons are not published (Bitquery, 2026; FreezeCheck, 2026).
- No address is tied to a named person. The Zenodo record states that it contains no personally identifying data.
- Sanctions listings and freezes are treated as records of official or issuer action, not as proof of crime.
- Court cases are described with their status: charged, or sentenced.

## 15. Key terms

| Term | Definition |
|---|---|
| **AddedBlackList / RemovedBlackList** | The on-chain records written when Tether freezes or unfreezes an address. They give the exact time the freeze takes effect, which is later than its public proposal. |
| **Address (wallet)** | A code that identifies a wallet on a blockchain, like an account number, without the owner's name. |
| **AML/CFT** | Anti-money laundering and countering the financing of terrorism: the rules that make banks and crypto firms check customers and report suspicious activity. |
| **Cross-chain bridging** | Moving tokens from one blockchain to another, for example from TRON to Ethereum. |
| **DestroyedBlackFunds** | The on-chain record written when Tether destroys the balance of a frozen address. |
| **FATF** | The Financial Action Task Force, the international body that sets global standards against money laundering. |
| **FIU** | Financial Intelligence Unit: the government office that receives and analyses suspicious transaction reports. |
| **Freeze (blacklist)** | Tether adds an address to the USDT contract's blacklist so its USDT cannot move. RemovedBlackList undoes it. |
| **Hawala** | An informal way of moving value across borders through trusted brokers, outside the banking system. |
| **Issuer** | The company that creates a stablecoin and stands behind it. Tether is the issuer of USDT. |
| **Noisy label** | A label that is sometimes wrong or incomplete. Freezes are noisy labels for laundering. |
| **Off-chain / on-chain** | On-chain activity is recorded on the blockchain and is public. Off-chain activity (cash, bank transfers, hawala) is not. |
| **Off-ramp (cash-out)** | Turning crypto back into fiat money such as dollars, dirhams or rupees. |
| **OTC broker** | A dealer who converts between fiat money and crypto directly with a customer, off exchange. |
| **P2P trading** | Users trading directly with each other, often arranged on platforms or chat apps. |
| **Proposal** | The public first step of a freeze: one of Tether's signers submits it to a multisig wallet, and a second signer later confirms it. |
| **Predicate crime** | The original crime that produced the money, such as fraud or drug trafficking. |
| **Pseudo-freeze time** | A stand-in reference date given to never-frozen accounts, so they can be compared with frozen ones. |
| **Stablecoin** | A crypto token designed to hold a steady value, usually one US dollar. |
| **STR / SAR** | Suspicious transaction or activity report, sent by a bank or crypto firm to its FIU. |
| **Tether** | The company that issues USDT and can freeze USDT at any address. |
| **TRON (TRC-20)** | A blockchain used heavily for stablecoin transfers because fees are low and settlement is fast. USDT on TRON is a TRC-20 token. |
| **Underground banking** | Informal systems outside regulated banking that move value across borders. |
| **Unhosted wallet** | A wallet its owner holds directly, with no AML-obliged intermediary. |
| **USDT** | Tether's stablecoin, backed by fiat money and pegged to the US dollar. |
| **VASP** | Virtual asset service provider: a licensed crypto firm such as an exchange or broker. |

## 16. References

Bitquery. (2026, August 13). [Investigation of Tether's USDT freeze regime on Ethereum and TRON]. https://bitquery.io/investigations/tether-blacklist-audit

Di Salvo, M. (2026, January 17). USDT on Tron central to $1 billion money laundering scheme, feds say. DL News. https://www.dlnews.com/articles/regulation/alleged-criminal-used-usdt-to-launder-1-billion/

DL News. (2024, January 18). [Report on the UNODC study naming USDT on Tron in Asian organised crime]. https://dlnews.com/articles/defi/tether-takes-fire-as-un-says-usdt-is-used-in-asia-crime/

Financial Action Task Force. (2026). Targeted report on stablecoins and unhosted wallets: Peer-to-peer transactions. https://www.fatf-gafi.org/en/publications/Virtualassets/targeted-report-stablecoins-unhosted-wallets.html

FreezeCheck. (2026, November 11). Who Tether freezes on TRON, and who it doesn't. DEV Community. https://dev.to/freezecheck/who-tether-freezes-on-tron-and-who-it-doesnt-3hfg

FreezeCheck. (2026b). Tether USDT freezes on TRON: Multisig proposal-to-freeze window, Nov 2025 - Nov 2026 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24124768

FreezeCheck. (2026c). Tether USDT unfreezes and burns of frozen balances on TRON, Nov 2025 - Nov 2026 [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24124777

Google Cloud. (n.d.-a). BigQuery pricing. https://cloud.google.com/bigquery/pricing

Google Cloud. (n.d.-b). BigQuery public datasets. https://docs.cloud.google.com/bigquery/public-data

Google Cloud. (n.d.-c). [Blockchain Analytics dataset schema]. https://docs.cloud.google.com/blockchain-analytics/docs/schema

Kochar, S., Aggarwal, K., Gera, S., & Kumar, A. (2026, March 26). Misuse of virtual assets in financial crime: Global trends, UAE regulatory framework, and risk mitigation strategies. Mondaq. https://www.mondaq.com/fintech/1765020/misuse-of-virtual-assets-in-financial-crime-global-trends-uae-regulatory-framework-and-risk-mitigation-strategies

Madras High Court. (2025, March 28). Moyeen Ahmed v. Additional Director General of Police, Cyber Crime Wing (W.P.(MD) No. 3165 of 2025). https://indiankanoon.org/doc/194938352/

Money Laundering Reporting Office Switzerland [MROS]. (2026). Annual report 2025. Federal Office of Police. https://www.fedpol.admin.ch/dam/en/sd-web/05JKPvNkIrsY/jb-mros-2025-e.pdf

Muhammad, W., Alsafi, T., & Iqbal, N. (2026). Data and code for: Early detection of illicit USDT accounts on the TRON blockchain using issuer-freeze labels and value-weighted evaluation (Version 1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24031003

News on AIR. (2025, August 6). ED conducts search operations at 11 locations in Delhi, Noida, Gurugram, Dehradun in global cyber fraud case. All India Radio. https://www.newsonair.gov.in/ed-conducts-search-operations-at-11-locations-in-delhi-noida-gurugram-dehradun-in-global-cyber-fraud-case

Supervisory Subcommittee. (n.d.). Virtual asset service providers (VASPs): Emerging ML/TF/PF risks, threats & vulnerabilities in the UAE relating to stablecoins. Central Bank of the UAE. https://www.centralbank.ae/media/z02hk1ct/jointp-3.pdf

Tsai, M. L. (2026, August 3). Judicially grounded virtual asset address labels and TRON TRC20-USDT behavioral analysis dataset (Version 3) [Data set]. Mendeley Data. https://doi.org/10.17632/62dmsngtfb.3

U.S. Attorney's Office, Eastern District of Virginia. (2026a, January 9). Venezuelan national charged with laundering approximately a billion dollars in illicit funds. U.S. Department of Justice. https://www.justice.gov/usao-edva/pr/venezuelan-national-charged-laundering-approximately-billion-dollars-illicit-funds

U.S. Attorney's Office, Eastern District of Virginia. (2026b, November 3). Venezuelan national sentenced to 12 years in prison for laundering over a billion dollars in illicit funds. U.S. Department of Justice. https://www.justice.gov/usao-edva/pr/venezuelan-national-sentenced-12-years-prison-laundering-over-billion-dollars-illicit

Vardai, Z. (2026, November 12). Tron and Tether bring in Chainalysis after T3 crime unit folds. Cointelegraph. https://cointelegraph.com/news/tron-tether-chainalysis-cybercrime-task-force-laundering

## 17. Corrections made on 24 November 2026

| Section | Change |
|---|---|
| Title, 2 | "Laundering accounts" replaced, because the project makes no claim that any address is criminal |
| 2 | "Four things" is now five, to match the five research questions |
| 4, 6 | FATF para 66 also names identification on a national sanctions list |
| 4, 9, 11, 15 | Freezes are publicly proposed before they take effect |
| 4 | T3 unit and new task force added |
| 5 | 8,206 is a still-frozen count; the like-for-like ever-frozen count is 9,191 |
| 5 | UAE reports were analysed, not filed, in that window |
| 6 | Six groups, not five; batch freezing and mass release added; source's commercial interest stated |
| 7, 8 | Indian case described as statements by investigators |
| 8 | FATF Box 3 described as FATF frames it; US destinations cited to the sentencing release |
| 12 | Gaps corrected; further sources added for RQ3 to RQ5 |
| 13 | "Meets a FATF request" reworded |
| 13 | UAE paper's wording matched to the source, which was read at its new address |
| 16 | Two dead links replaced; four references added; order corrected |
| 3, 4, 6, 12 | After a second audit: charging-stage wording, multisig start date, batch figure credited to our count, sanctions-list totals corrected (the first version used an incomplete Israeli file) |

Figure 2 in the PDF version still shows five groups and needs the sixth bar. The UAE paper moved to a new address and was read there; its PDF was created on 20 January 2026. The Madras High Court order was checked only through a law-firm summary, which confirms the defreeze and the Rs 3 lakh lien but does not say whether the seller was an accused person.
