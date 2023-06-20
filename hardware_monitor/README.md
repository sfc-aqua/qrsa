# Hardware Monitor (HM)- 
[Hardware Monitor (HM)](#hardware-monitor-hm)
- [Hardware Monitor (HM)-](#hardware-monitor-hm-)
  - [Introduction](#introduction)
  - [Interfaces](#interfaces)
  - [Activity Diagrams](#activity-diagrams)
    - [Boot component](#boot-component)
      - [Expected Exceptions](#expected-exceptions)
    - [Link cost calculation](#link-cost-calculation)
      - [Expected Exceptions](#expected-exceptions-1)
    - [Start link generation](#start-link-generation)
    - [Send link ready notification](#send-link-ready-notification)
    - [Stop link generation](#stop-link-generation)

## Introduction

## Interfaces


## Activity Diagrams
See detailed workflow in google drive (not publicly available)

### Boot component
Related Components: HM, EPPS/BSA

```mermaid
sequenceDiagram
autonumber

participant hm as Hardware Monitor (HM)
participant rd as Routing Daemon (RD)
participant epbs as EPPS / BSA
participant hm2 as HM at next hop

Note over hm: Boot HM (Link up)
hm ->> rd: Request next hop repeater info
rd ->> hm: Return next hop repeater info

hm ->> hm2: Notify new link up
hm ->> epbs: Request device config
epbs ->> hm: Send device config

hm2 ->> epbs: Request device config
epbs ->> hm2: Send device config
```

Device configuration contains a set of information about the intermediate entanglement generation devices such as EPPS generation, BSA acceptable photon numbers per sec, EPPS estimated generation rate etc. 

#### Expected Exceptions
- No device found: HM cannot establish connection with EPPS/BSA
- No config found: EPPS/BSA cannot provide their configuration in some reasons
- Request timeout: It takes too long to get response from EPPS/BSA
- Device config type invalid: The contents of device config is invalid

### Link cost calculation
Related Components: HM, EPPS/BSA, Routing Daemon (RD)

```mermaid
sequenceDiagram
autonumber

participant hm as Hardware Monitor (HM)
participant epbs as EPPS / BSA
participant rd as Routing Daemon
participant hm2 as HM at next hop

Note over hm: HM booted

Note over hm: Decide tomography plan
hm ->> hm2: Request link tomography
Note over hm2: Check tomography strategy
hm2 ->> hm: Response link tomography request

hm ->> epbs: Request link generation
epbs ->> hm: Link generation notification / Timing notifications
epbs ->> hm2: Link generation notification / Timing notifications

loop for all the requested entanglement
    hm2 --> hm: Entanglement
    Note over hm: Measure in random basis
    Note over hm2: Measure in random basis
    Note over hm: Stack measurement result
    Note over hm2: Stack measurement result
end

hm ->> hm2: Send measurement results
hm2 ->> hm: Send measurement results
Note over hm: Link cost calculation
Note over hm2: Link cost calculation

hm ->> rd: Notify link cost
Note over rd: Update link cost

hm ->> epbs: Stop entanglement generation request
epbs ->> hm: Link generation stopped
epbs ->> hm2: Link generation stopped
```

#### Expected Exceptions
Numbers are corresponding to the sequence numbers in the diagram
- 1. Request link tomography
  - Invalid request format: The request format for link tomography is invalid.
- 2. Response to link tomography request
  - Invalid response format: The response format for link tomography is invalid.

### Start link generation 
Related Components: HM, EPPS/BSA, RuleEngine

Start link generation when a first RuleSet arrives and RE sends message to HM.

```mermaid
sequenceDiagram
autonumber

participant hm as HM
participant epbs as EPPS / BSA
participant re as RuleEngine
participant hm2 as HM at next hop

Note over re: Received the first RuleSet
re ->> hm: Entanglement generation request
hm ->> epbs: Link generation request
epbs ->> hm: Link generation start notification / Timing
epbs ->> hm2: Link generation start notification / Timing

Note over hm, hm2: Entanglement generation start
```

**BSA**
```mermaid
sequenceDiagram
autonumber

participant hm as HM
participant bsa as BSA
participant hm2 as HM at next hop

loop for notified trials
    hm -->> bsa: Photon 0
    hm2 -->> bsa: Photon 0
    Note over bsa: Perform BSM
    Note over bsa: Stack BSM results
end

bsa ->> hm: Send Result
bsa ->> hm2: Send Result

```

**EPPS**
```mermaid

sequenceDiagram
autonumber

participant hm as HM
participant epps as EPPS
participant hm2 as HM at next hop

loop for expected trials (this could be streaming)
    epps -->> hm: Photon Pair 0
    epps -->> hm2: Photon Pair 0

    Note over hm: Perform BSM
    Note over hm2: Perform BSM
    Note over hm: Stack BSM result
    Note over hm2: Stack BSM result
end 

hm ->> hm2: Meausrement results
hm2 ->> hm: Measurement results
```


### Send link ready notification
Related Components: HM, RuleEngine

Once the link entanglement is ready, notify it to the RuleEngine.

```mermaid
sequenceDiagram
autonumber

participant hm as HM
participant re as RuleEngine
participant hm2 as HM at next hop

hm --> hm2: Entanglement
hm ->> re: Entanglement Ready Response
```

### Stop link generation
Related Components: HM, EPPS/BSA, RuleEngine

When all the RE execution is done and no RuleSet is running, RE request link generation stop.

```mermaid
sequenceDiagram
autonumber

participant hm as HM
participant epbs as EPPS / BSA
participant re as RuleEngine
participant hm2 as HM at next hop

Note over re: Terminate final RuleSet
re ->> hm: Entanglement generation stop request
hm ->> epbs: Link generation stop request
epbs ->> hm: Link generation stop notification
epbs ->> hm2: Link generation stop notification

Note over hm, hm2: No more entanglement here
```