[TAP home](Home)

## Welcome

Welcome to the OCP Time Appliances Project wiki.

This Project is open to the public and we welcome all those who would like to be involved.

Time is one of the key elements to improve efficiency in a distributed system. Theoretically, the performance of a distributed system depends on the synchronization of its elements. Several industries such as telecom, mobile, power, industrial, professional audio and video and many more have embraced the need for highly accurate and more importantly reliable distribution and synchronization of time and frequency across packet networks. Although the use case scenario for each of the industries is different, they all share one common thing and that is, time synchronization. Since there is a diverse need for time synchronization across different industries, driven from different use cases and applications, managing the needs of this industry chain can become a challenge.

Time Appliances Project (TAP) aims to provide a platform to bring together the community, discuss, standardize and share technologies and solutions across industries with the datacenter applications and datacenter network infrastructure as the main interest. The project aims to bring together the community of datacenter operators, application developers, and equipment and semiconductor companies together to enable datacenter time-sensitive applications such as consistency in distributed systems, edge computing, AR/VR and IoT. These applications will greatly benefit from high accuracy, reliable, and scalable distribution and synchronization of time.

IEEE 1588 Precision Timing Protocol (PTP) and other synchronization methods have been adopted by various industries to maximize the efficiency of various distributed system use cases. Each use case scenario comes with a set of requirements and configurations. These configurations are collected as a ‘PTP profile’. Time appliances project aims to support the development of a PTP profile for datacenter applications and datacenter network infrastructure. The profile will cover time-sensitive applications over OCP-compliant and PTP-aware networking infrastructure such as network switches, network clocks, network interface cards, timing modules & connectors, etc. Additionally, the profile will address various requirements for high accuracy and reliable distribution and synchronization of time, such as expected performance, networking, software API, data models, deployment and telemetry. The project also aims at openness and interoperability through the use of open-source PTP software implementations for timing appliances.

IEEE P3335 Standard for Architecture and Interfaces for Time Card defines the generic architecture and interfaces of a time card system, which constitutes a traceable source of time-of-day to heterogeneous systems that distribute and/or use that time. Additionally, this standard defines figures of merit that univocally characterize the relevant performance of the Time Card. The Time Card provides a traceable time-of-day for systems directly attached to it, as well as networked distributed systems. Such systems include, but are not limited to, servers hosting the Time Card, and servers synchronized with the Time Card using such protocols as Precision Time Protocol (PTP) or Network Time Protocol (RFC Request for Comments) 5905). This standard also defines the basic building blocks of the Time Card and their interfaces in order to allow modularization. The main building blocks include time source, local oscillator, and time processor. Additionally, this standard defines interfaces between the Time Card and other systems. This includes physical interfaces that allow input and output of time-related signals. This also includes logical interfaces that are compatible with Portable Operating System Interface for UNIX (POSIX) and include for example an interface to share a Physical Hardware Clock (PHC). This allows sharing the time of day with other systems, as well as providing means for diagnostic and configuration. The definition of logical interfaces allows for a variety of Time Card’s form factors (e.g. Peripheral Component Interconnect Express (PCIe)) while ensuring uniform support from the operating system. Any device that complies with this standard provides performance figures that are obtained following the specifications of this standard. As such, different implementations of the Time Card can be easily compared in terms of performance.

Datacenter applications are the primary target of time appliances project. In addition, the project extends to related topics on time synchronization in academia, research and other industries. The time appliances project brings together the community and will be highly collaborative through technical meetings and collaboration with other OCP Projects including the Networking, Storage, Server, and Telco Projects.

*Disclaimer: Please do not submit any confidential information to the Project Community. All presentation materials, proposals, meeting minutes and/or supporting documents are published by OCP and are open to the public in accordance to OCP’s Bylaws and IP Policy. This can be found on the OCP [OCP Policies](https://www.opencompute.org/about/ocp-policies/) page. If you have any questions please contact OCP.*

<img src="https://raw.githubusercontent.com/wiki/Time-Appliances-Project/wiki/images/Screenshot_2020-07-01_16.35.12.png" alt="Time Appliances Project" width="135">

Time Appliances Project

## Mission Statement

1. Create specifications and references for **Data Center Timing** appliances, applications and networking infrastructure
2. Promote openness in **Timing Appliances** and interfaces through open-source implementations

## Project Leadership

- Steering Committee Representative: [Elad Wind](mailto:elad@nvidia.com)
- Project Leads: [Ahmad Byagowi](mailto:byagowi@turba.ai)

## Liaisons

- IEEE-IC Liaison: [Rodney Cummings](mailto:rodney.cummings@keysight.com) (Keysight)
- ITU-T Liaison: [Silvana Rodrigues](mailto:Silvana.rodrigues@huawei.com) (Huawei)
- ITU-T Liaison: [Stefano Ruffini](mailto:stefano.ruffini@calnexsol.com) (Calnex)

## Get Involved

- [TAP mailing list](https://ocp-all.groups.io/g/ocp-tap)
- [Time Appliances calendar](https://ocp-calendar.pages.dev/)
- [TAP repositories](https://github.com/Time-Appliances-Project)
