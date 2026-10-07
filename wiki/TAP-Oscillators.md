*Recovered from the OCP wiki snapshot dated 2022-11-30. See [TAP:Restoration notes](Restoration-notes) for coverage.*

<img src="https://raw.githubusercontent.com/wiki/Time-Appliances-Project/wiki/images/Screenshot_2020-07-01_16.35.12.png" alt="Time Appliances Project" width="135">

## Workstream #4

[Time Appliances Project](Home)

## Objective

Implementors needing to select oscillators for synchronizing networks in data centers face several challenges. Synchronization is a system-level requirement that is unclear how to satisfy by reading an oscillator datasheet. This makes it difficult and time consuming to select oscillators, leading to inconsistent and unpredictable PTP performance in the network. Therefore, the goal of this workstream is to specify classes of oscillators for common data center use cases to make it easier and faster to compare and select oscillators with high confidence to achieve a given level of PTP performance.

## Project Team

- Lead: [Gary Giust (SiTime)](mailto:ggiust@sitime.com)

## Documents

- [Requirements Document for OCP-TAP Oscillator Classes (Jan 8, 2022)](https://www.opencompute.org/documents/ocp-tap-oscillator-spec-jan-8-2022-docx-pdf)

## Recording from Past Calls

| Recordings | Slides |
| --- | --- |
| [Nov-30, 2022](https://drive.google.com/file/d/1HLcrq7dNSdfLOm_I_SLW02FLafMBWQ3X/view?usp=sharing) Class B1 osc specs, test method: daily aging |  |
| [Nov-16, 2022](https://drive.google.com/file/d/1zUo-0HsSk-6yE0agOKJKJebtcfAu-jqD/view?usp=share_link) Class B1 sys specs, test method: freq over temp slope |  |
| [Sep-21, 2022](https://drive.google.com/file/d/1ADDWmHf787E9skbWpd3ZCfuHsbptf4W8/view?usp=sharing) Test method: freq stability over temp |  |
| [Aug-24, 2022](https://drive.google.com/file/d/1OooOkd_Dwrg0yCwhjlY0xMeqSsmy9Y8A/view?usp=sharing) Test method: framework proposal |  |
| [Jun-29, 2022](https://drive.google.com/file/d/1JR--ArSWvf99No4swK--1zhNUN1yy7u2/view?usp=sharing) Test method: initial discussion, compliance options |  |
| [Apr-6, 2022](https://drive.google.com/file/d/1FjEqr-14R4Vt0VEtKKyq90SAci0r8jbS/view?usp=sharing) Recap of oscillator classes and use cases |  |
| [Mar-23, 2022](https://drive.google.com/file/d/1joauJq4oBpisjwt7tf6apZ3TTX-l3syY/view?usp=sharing) Classes F1, T1 |  |
| [Feb-2, 2022](https://drive.google.com/file/d/1v7rAdHIYnO83-Ujp0ozrxPjC5tPvpWPM/view?usp=sharing) |  |
| [Jan-5, 2022](https://drive.google.com/file/d/1kyptpA4o0PX_SMhsKARGpjlSAP5N5e-d/view?usp=sharing) |  |
| [Dec-1, 2021](https://drive.google.com/file/d/1mJODWTyLR49j9-WaFYphoKe98hdA_TU_/view?usp=sharing) |  |
| [Sep-1, 2021](https://drive.google.com/file/d/1LpgxV0YIMrhOO1sOY3nAtw9ozfyyzPQP/view?usp=sharing); [Sep-8, 2021](https://drive.google.com/file/d/1hpxMSDdZ7zWIW01AyltPNEpbuYz44QSW/view?usp=sharing); [Sep-15, 2021](https://drive.google.com/file/d/1uXuDhv7Tasnl6-kmZPr2LC1bFHOlcoM2/view?usp=sharing); [Sep-22, 2021](https://drive.google.com/file/d/1HvZ1JaIBqXgh7B76yMO6CMWSB-_D-eJN/view?usp=sharing) |  |
| [Aug-11, 2021](https://drive.google.com/file/d/14dONxCYDf-s0-uTZkzrcsJ9iUgHKUgGO/view?usp=sharing); [Aug-25, 2021](https://drive.google.com/file/d/1sE0POmbOwZujYnysLP3I0ckSuBx_nl4d/view?usp=sharing) |  |
| [Jul-21, 2021](https://drive.google.com/file/d/174ee4Vy40Xng_eadeGJCaqA-e30pUOoS/view?usp=sharing) |  |
| [Jun-2, 2021](https://drive.google.com/file/d/1-NCuDKgyX3BcNYXOigC_1iGxNpMkld3f/view?usp=sharing);[Jun-9, 2021](https://drive.google.com/file/d/1kAGJfEMGr3ohVcbOg4W1oP17h2EPLIpI/view?usp=sharing); [Jun-23, 2021](https://drive.google.com/file/d/1qpshLJ0M9NIZ6F8Zt0pToYQiMeeuJnck/view?usp=sharing) |  |
| [May-5, 2021](https://drive.google.com/file/d/15MWS5t-Wag0LsJBebB8mPmjKatvRBjgS/view?usp=sharing); [May-12, 2021](https://drive.google.com/file/d/1whjaGJv005NjJH81_pIZM6doiS6_zOPK/view?usp=sharing); [May-19, 2021](https://drive.google.com/file/d/1L3cF6nFC7HrlsZzoNsxx-5LBwGxmWVtt/view?usp=sharing), [May-26 2021](https://drive.google.com/file/d/1TWQdRqPglIp1begJf4_CT94GlDnIyLLT/view?usp=sharing) |  |
| [Apr-7, 2021](https://drive.google.com/file/d/1HyR0wECmPYLHITq3Af0xYlaOWdIPlpm9/view?usp=sharing); [Apr-14, 2021](https://drive.google.com/file/d/1lkECCGt6WCi9D1eYiFOizGqyPRPBhLnI/view?usp=sharing);[Apr-21, 2021](https://drive.google.com/file/d/1uu3kDE5E7qBSC3ztkUBh8ocj8tn7_qH6/view?usp=sharing);[Apr-28, 2021](https://drive.google.com/file/d/1a6jMilj6N4zSc5n5wD0AWF9wU1jsWA5M/view?usp=sharing); |  |
| [Mar-18, 2021](https://drive.google.com/file/d/12WmaGkLF1IUjLaAhXSzVp33pzmlYMA4J/view?usp=sharing); [Mar-31, 2021](https://drive.google.com/file/d/1P1bME9Z8jQsPGPF1msC3a825Ou-4mjol/view?usp=sharing); | [Mar-18, 2021](https://drive.google.com/file/d/1O2iMLKKRqtesziBLPQ9PTh23Yyg_Efx2/view) |
