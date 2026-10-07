*Recovered from the OCP wiki snapshot dated 2022-11-10. See [TAP:Restoration notes](Restoration-notes) for coverage.*

<img src="https://raw.githubusercontent.com/wiki/Time-Appliances-Project/wiki/images/Screenshot_2020-07-01_16.35.12.png" alt="Time Appliances Project" width="135">

## Instrumentation and Measurement - Workstream #6

[Time Appliances Project](Home)

## Objective

Open source ecosystem for instrumentation and measurement software and tools. Scalable, reliable, cost-effective and efficient.

## Project Team

- Lead: [Anand Ram](mailto:anand.ram@calnexsol.com) (Calnex)

- Lead: [Julian St James](mailto:julianstj@fb.com) (Meta)

## Meeting invite

8:00am - 8:30am PST every Second and Fourth Thursday: [Launch Teams Meeting Link](https://teams.microsoft.com/dl/launcher/launcher.html?url=%2F_%23%2Fl%2Fmeetup-join%2F19%3Ameeting_OGE1MzNkMGMtZDRjMS00YzFiLTg4MTAtZjcxNzEwYzI2ODIy%40thread.v2%2F0%3Fcontext%3D%257b%2522Tid%2522%253a%2522fbb4e2fb-f802-4d55-beca-b7149551e928%2522%252c%2522Oid%2522%253a%2522cff27e02-befc-4437-98d5-96034f77b90c%2522%257d%26anon%3Dtrue&type=meetup-join&deeplinkId=5f0bbd41-a286-4e8b-b786-5162812cfe21&directDl=true&msLaunch=true&enableMobilePage=true&suppressPrompt=true)

## Recording from Past Calls

[20 Jan 2022](https://drive.google.com/file/d/1Ctz2eWt2e71y9ChquZGdu6Fc9H5PQZZs/view?usp=sharing)

[27 Jan 2022](https://drive.google.com/file/d/1Ew3LOo-vUEA_KcP0A_MnnkuHmVzykC6V/view?usp=sharing)

[24 Feb 2022](https://drive.google.com/file/d/1iBY6HX9EA6CKG3QWYw7ZwfNMUUyketMG/view?usp=sharing)

[23 Jun 2022](https://drive.google.com/file/d/1xPt-CWZEpcoVGmgpRnG8ccebdfoZ46vq/view?usp=sharing)

[27 October 2022 PTP Simulator Demo](https://drive.google.com/file/d/1uO8RtSFO5l7xTY6mTIrsImsP2iaRvyNC/view?usp=sharing)

[10 November 2022 Monitoring Discussion](https://drive.google.com/file/d/1sZzXC85Pl4viJoBF0x6Y_eYNiCe-YtY-/view?usp=sharing)

## Hardware Roadmap

|  | Design | Objective |
| --- | --- | --- |
| **#1** | Time Card based PPS measurement | Scaleable use of the Time Card in a generic server to perform up to 4 PPS measurements |

## Software

|  | Design | Objective |
| --- | --- | --- |
| **#1** | Time Card based PPS measurement | Interface with Time Card driver and export PPS measurement data in a useful format |

## Potential Future Hardware Solutions

|  | Core Hardware | Objective |
| --- | --- | --- |
| **#1** | TDC | Small, cheap, and low power use-case |
| **#2** | PTM controller | A PCIe based daughter card that can be synchronized with a high stability source (Time Card) over PCIe to scale PPS measurements |
| **#3** | UWB | A method for distributing GPS and time to areas where measurements are made, but GPS is not available |
| **#4** | DPLL | A discrete design based around a DPLL , removing the need for an FPGA |
