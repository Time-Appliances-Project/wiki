*Recovered from the OCP wiki snapshot dated 2022-01-11. See [TAP:Restoration notes](Restoration-notes) for coverage.*

<img src="https://raw.githubusercontent.com/wiki/Time-Appliances-Project/wiki/images/Screenshot_2020-07-01_16.35.12.png" alt="Time Appliances Project" width="135">

## Workstream #3

[Time Appliances Project](Home)

The *clock_gettime* API was designed a couple of decades ago. The time is encoded as number of units between now and a half of a century ago. In theory, this encoding should be sufficient for any use of the phenomenon. For the majority of the systems, representing the time as an offset from the epoch works well. The changes in the last few decades were improvements related to the size of the unit; the unit shrank from seconds to nanoseconds.

Representing the time as just a number works well for many software systems. However, in the last two decades, to increase the efficiency of the system, we started building system where we replace communication with simple local calculation. For such systems, we need more information about the clock synchronization process. It became important when was the last time when the clock was synchronized, what type of physical local clock we have, what was the last measured offset between the local clock and the referent clock.

In the Time API stream, we will start with discussing software system and services that benefit from better time APIs. Initially I would like to focus our discussions on defining the problem that we want to solve, what are the requirements and what solution exist today. We will focus on defining the API and perhaps, at some point, we could discuss building a reference implementation. The goal is to publish an official proposal for time and clock API that allow designing system where time is reliable fundamental building block.

## Objective

Time and clock API that allow designing system where time is reliable fundamental building block

- APIs to bring accurate time to the user space

- APIs to disseminate the time error (error bound)

- APIs to provide viability over the time synchronization process

## Project Team

- Lead: [Georgi Chalakov (NVIDIA)](mailto:gchalakov@nvidia.com)

-

-

## Get Involved

- [Mailing List](https://ocp-all.groups.io/g/OCP-TAP-APIs)
