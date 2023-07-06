# Connection Manager (CM)
- [Connection Manager (CM)](#connection-manager-cm)
  - [Introduction](#introduction)
  - [Modules](#modules)
  - [Activity Diagrams](#activity-diagrams)
    - [Connection Setup (at Initiator)](#connection-setup-at-initiator)
    - [Connection Setup (at Repeater/Router)](#connection-setup-at-repeaterrouter)
  - [Connection Setup (at Responder)](#connection-setup-at-responder)
    - [Connection Teardown (at Initiator, Repeater/Router)](#connection-teardown-at-initiator-repeaterrouter)
    - [Link Allocation Update / Barrier](#link-allocation-update--barrier)
      - [Expected exceptions](#expected-exceptions)
  - [Data Structures](#data-structures)
  - [Message Contents](#message-contents)
  - [Variables](#variables)


## Introduction

## Modules
- connection_manager: The main module that communicates with external components
- message.rs: The model of message contents


## Activity Diagrams

### Connection Setup (at Initiator)
Related components: CM, Application, Routing Daemon, Rule Engine, Hardware MOnitor

```mermaid
sequenceDiagram
autonumber

Box orange Initiator
participant app as Application
participant cm as Connection Manager
participant rd as Routing Daemon
participant hm as Hardware Monitor
participant re as Rule Engine
end
participant cm2 as CM at next hop
participant res as CM at Responder

% setup request
Note over app, res: Connection Setup
Note over cm: Listen to application request
app ->> cm: Request application (maybe socket?)
cm ->> hm: Check the latest performance indicator (could be cached)
hm ->> cm: Return the latest device performance
cm ->> rd: Check next hop
rd ->> cm: Return next hop
cm ->> cm2: Forward Request with device and link performance information


% setup response
Note over app, res: Connection Setup Response
cm2 ->> cm: Forward connection setup response
Note over cm: Deserialize/Validate RuleSet
cm ->> re: Foward RuleSet
Note over re: Stack it to idle RuleSet queue

cm ->> res: RuleSet received message (may not need this)

Note over app, res: LAU / Barrier
```


### Connection Setup (at Repeater/Router)
Related components: CM, RuleEngine, Routing Daemon, Hardware Monitor

```mermaid
sequenceDiagram
autonumber

participant cm0 as CM at previous hop
Box orange Router/Repeater
    participant cm as Connection Manager
    participant rd as Routing Daemon
    participant hm as Hardware Monitor
    participant re as Rule Engine
end
participant cm2 as CM at next hop

% Connection Setup Request
Note over cm0, cm2:Connection Setup Request
cm0 ->> cm: Forward Request
cm ->> hm: Check the latest performance indicator (could be cached)
cm ->> rd: Check next hop
rd ->> cm: Return next hop
cm ->> cm2: Forward request to the next hop with performance indicator

% Connection Setup response
Note over cm0, cm2: Connection Setup Response
cm2 ->> cm: Forward connection setup response
Note over cm: Extract RuleSet for this repeater/router
Note over cm: Deserialize/Validate RuleSet
cm ->> cm0: Forward response

Note over cm0, cm2: LAU / Barrier
```

## Connection Setup (at Responder)
Related components: CM, RuleEngine, Routing Daemon, Hardware monitor
```mermaid
sequenceDiagram
autonumber

participant cm0 as CM at previous hop
Box orange Responder
    participant cm as Connection Manager
    participant re as Rule Engine
    participant rd as Routing Daemon
end

% Connection Setup Request
Note over cm0, rd: Connection Setup Request
cm0 ->> cm: Forward request
Note over cm: Extract performance indicators
cm ->> cm: Forward to RuleSet Factory
Note over cm: Create Rulesets
cm ->> re: Forward RuleSet to itself
re ->> cm: Return proposed LA

% Connection Setup Response
Note over cm0, rd: Connection Setup Response
Note over cm: Create connection setup responses for all the repeaters with RuleSet.
cm ->> rd: Request next hop information
rd ->> cm: Return next hop information
cm ->> cm0: Send responses

Note over cm0, rd: LAU / Barrier
```


### Connection Teardown (at Initiator, Repeater/Router)
Related components: CM, RuleEngine

```mermaid
sequenceDiagram
autonumber

Box pink Initiator
    participant cm_ini as CM at Initiator
    participant re_ini as RE at Initiator
end 
Box orange Repeater/Router
    participant cm as Connection Manager
    participant re as Rule Engine
end
Box yellow Responder
    participant cm_res as CM at Responder
    participant re_res as RE at Responder
end

Note over re_res: Terminate RuleSet
re_res ->> cm_res: Notify RuleSet Termination with next proposed LAU
cm_res ->> cm: Terminate RuleSet Message 

cm ->> cm_ini: Terminate RuleSet Message
cm ->> re: RuleSet Termination Request
re ->> cm: Return Proposed LA

cm_ini ->> re_ini: RuleSet Termination Request
re_ini ->> cm_ini: Return proposed LA


```
After CM gets negotiated LA with Barrier value and send it to RE, RE stop execution.
The next hop check also happens with routing daemon.

### Link Allocation Update / Barrier
Related components: CM, RE, 

> note: We might meta policy to align over the different links

Need to decide which is primary.
```mermaid
sequenceDiagram
autonumber
Box orange Node A (Primary)
    participant re as Rule Engine
    participant cm as Connection Manager
end
Box pink Node B (Secondary)
    participant cm2 as CM at next hop
    participant re2 as RE at next hop
end 

Note over cm: New RS / Terminate RS
Note over cm2: New RS / Terminate

cm ->> re: New RS / Terminate Request
cm2 ->> re2: New RS / Terminate Request

re ->> cm: Return proposed LA
re2 ->> cm2: Return proposed LA

cm ->> cm2: Send Primary LA
cm2 ->> cm: Send LA acceptance message

Note over cm, cm2: Stick with primary proposed LA
```
#### Expected exceptions
- 5: Inconsitent link information: CM at two nodes have different set of running RuleSet
- message inconsistent error: Only one of the nodes gets new RS or RS termination then send primary LA but no ruleset running at Secondary node


## Data Structures


## Message Contents
## Variables
|         key         |                             value                              | descripttions                                                |
| :-----------------: | :------------------------------------------------------------: | :----------------------------------------------------------- |
|      node_type      | Enum("Initiator", "Responder", "Repeater", "Router", "Switch") | A type of network node                                       |
| link_interface_list |                   List\[LinkInterfaceInfo\]                    | Link information cached in cm to store performance indicator |
|                     |                                                                |                                                              |