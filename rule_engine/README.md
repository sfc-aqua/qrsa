# Rule Engine (RE)
- [Rule Engine (RE)](#rule-engine-re)
  - [Introduction](#introduction)
  - [Activity Diagrams](#activity-diagrams)
    - [Idle (Booting -\> Waiting for RuleSet)](#idle-booting---waiting-for-ruleset)
    - [New RuleSet arrive](#new-ruleset-arrive)
    - [Link Allocation / Link Allocation Policy switching](#link-allocation--link-allocation-policy-switching)
    - [RuleSet termination message handling (Initiator / Repeater / Router)](#ruleset-termination-message-handling-initiator--repeater--router)
    - [RuleSet execution](#ruleset-execution)
  - [Data Structures](#data-structures)
  - [Message Contents](#message-contents)

## Introduction

## Activity Diagrams

### Idle (Booting -> Waiting for RuleSet)
Related components: RE, Connection Manager, Real-Time Controller, Hardware Monitor

```mermaid
sequenceDiagram
autonumber
participant re as Rule Engine
participant cm as Connection Manager
participant hm as Hardware Monitor
Note over re: Boot
re ->> hm: Helth check
hm ->> re: Ready
re ->> cm: Notify Ready
Note over cm: Start accepting request & response
```

### New RuleSet arrive
Related components: RE, Connetion Manager, Hardware Monitor

1. The case where there is no running RuleSet
```mermaid
sequenceDiagram
autonumber
participant cm as Connection Manager
participant hm as Hardware Monitor
participant re as Rule Engine
participant rep as RE/Policy Manager
participant rsr as RE/RuleSet Runtime
Note over cm: New RuleSet
cm ->> re: Forward RuleSet
Note over re: Check running RuleSet (Empty)
re ->> cm: Return proposed LA
cm ->> re: Forward negotiated LA
re ->> rep: Instantiate Policy Manager
re ->> rsr: Instantiate RuleSet Runtime 
activate rsr
%rsr ->> hm: Check current PPTSN
%hm ->> rsr: Return current PPTSN (Possible in real time?)
re ->> rep: Runtime ownership
rep -->> rsr: Ownership (read/exec)
Note over rsr: Wait for link resource
alt Only for the first time 
re ->> hm: Start link generation request
end
hm ->> re: Link enatnglement Ready
Note over cm, rsr: Go to link allocation
deactivate rsr
```


### Link Allocation / Link Allocation Policy switching
Releated componentns: RE, HM

When there is one link allocation policy, all the resoruces go to one policy.
```mermaid
sequenceDiagram
autonumber
participant hm as Hardware Monitor
participant re as Rule Engine
participant rep as RE/Policy Manager
participant rsr as RE/RuleSet Runtime
Note over rep: 0 <= PPTSN
hm ->> re: Link resource ready (PPTSN=10 ~ 20)
re ->> hm: OK (or continue?)
Note over re: Check resource's PPTSN
re -->> rep: Transfer ownership
Note over rep: Check running runtime status
Note over rep: Decide resource distribution policy
rep -->> rsr: Transfer ownership
Note over rsr: Consume Resource
rsr ->> re: Resource consumed notification
re ->> hm: Resource ready for next round
```

When there are two link allocation policies (active LA and proposed LA), link allocation policy has to be properly switched.


```mermaid
sequenceDiagram
autonumber
participant hm as Hardware Monitor
participant re as Rule Engine
participant rtc as Real-Time Controller
participant rep_old as RE/Old Policy Manager
participant rep_new as RE/New Policy Manager
participant rsr as RE/RuleSet Runtime
activate rep_old
Note over rep_old: 0 <= PPTSN < 100
Note over rep_new: 100 <= PPTSN
rep_old -->> rsr: Runtime Ownership (read/exec)
rep_new -->> rsr: Runtime ownership (read)
hm ->> re: Link resource ready (PPTSN=90 ~ 110)
re ->> hm: OK (or continue?)
Note over re: Check resource's PPTSN
re ->> rep_old: Transfer link ownership (PPTSN 90 to 99)
re ->> rep_new: Transfer link ownership (PPTSN 100 to 110)
activate rep_new
Note over rep_new: Activate new policy
Note over rep_new: Get Runtime Ownership
rep_new -->> rsr: Runtime Ownership (read/exec)
re ->> rep_old: Deactivate 
rep_old ->> re: Unconsumed resources
Note over rep_old: Deactivate old policy
deactivate rep_old
re ->> rtc: Free resource request
rtc ->> re: Requested resource freed 
re ->> hm: Link ready for next round
Note over rsr: Consumed Resource
rsr ->> re: Resource Consumed Notification
re ->> hm: Link ready for next round
deactivate rep_new
```

When there are multiple resources arrived at RE simultaneously, it might be diffuclt to handle transitions from old policy to new policy.


### RuleSet termination message handling (Initiator / Repeater / Router)
Related components: RE, Connection Manager, Hardware Monitor

```mermaid
sequenceDiagram
autonumber
participant cm as Connection Manager
participant re as Rule Engine
participant hm as Hardware Monitor
participant rep as RE/Current Policy Manager
participant rep_new as RE/New Policy Manager
participant rsr as RE/Terminated RS Runtime
participant rsr2 as RE/Running RS Runtime
rep -->> rsr: Ownership (read/exec)
rep -->> rsr2: Ownership (read/exec)
Note over cm: RuleSet Termination
cm ->> re: Terminate RuleSet request
Note over re: Check running RuleSet
re ->> cm: Return Proposed LA
cm ->> re: Forward negotiated LA
re ->> rep_new: Instantiate a new Policy Manager
rep_new -->> rsr2: Ownership (read)
Note over rep, rep_new: LA switching
re ->> rsr: Close RuleSet Runtime
re ->> rep_new: Transfer ownership to new policy
rep_new -->> rsr2: Ownership (read/exec)
alt Final RuleSet terminated
re ->> hm: Stop entanglement generation
hm ->> re: Entanglement generation stopped
end
```


### RuleSet execution
Related Components: RE/RuleSet Runtime, Real-Time Controller, Hardware Driver(HWD), Socket

```mermaid
sequenceDiagram
autonumber
participant re as RE/RuleSet Runtime
participant rtc as Real-Time Controller
participant qubit as HWD/QNIC
participant socket as Socket
Note over re: Received resource ownership
Note over re: Instruction: Perform CX
re ->> rtc: Request CX (q1, q2)
rtc ->> qubit: Peform CX
rtc ->> re: Performed
Note over re: Instruction: Perform Measurement
re ->> rtc: Request Measurement (q2)
rtc ->> qubit: Perform Measurement
qubit ->> rtc: Measurement Result
rtc ->> re: Measurement Result
Note over re: Instruction: Perform SendMessage
re ->> socket: Request Messege transfer
Note over socket: Transfer message
socket ->> re: Message Sent
```

## Data Structures


## Message Contents