# Real-Time Controller(RTC)
- [Real-Time Controller(RTC)](#real-time-controllerrtc)
  - [Introduction](#introduction)
  - [Components](#components)
  - [Hardware Abstraction](#hardware-abstraction)
  - [Activity Diagrams](#activity-diagrams)
    - [Setup](#setup)
    - [Perform Instruction](#perform-instruction)
    - [Perform instruction to locked qubits](#perform-instruction-to-locked-qubits)
  - [Interfaces](#interfaces)
    - [Hardware](#hardware)
    - [Software](#software)


## Introduction
Real-Time Controller is a thin wrapper for Rule Engine to manipulate peripherals such as qubit controller, classical network interface.

## Components
- contoller.rs: A main process that communicates with RS, HW and Hardware Drivers
- instruction_converter.rs: Convert high level instructions into hardware dependent instruction sets.
  - Should be configurable with external config file
- hal_wrapper: Hardware abstraction layer wrapper to assume virtual hardwares are existeing


## Hardware Abstraction
In order for higher layer components to manipulate low layer devices such as qubit memories and real-time communication devices, 

## Activity Diagrams
### Setup
Related Components: RTC, HM, RE, Hardware Driver (HD)

```mermaid
sequenceDiagram
autonumber

participant rtc as Real-Time Controller
participant qnic as HD/QNIC
participant qubit as HD/Qubit
participant re as Rule Engine
participant hm as Hardware Monitor

Note over rtc: Boot process
qnic -->> qubit: Ownership/Control?
rtc ->> qnic: Check profiles

re ->> rtc: Get hardware profiles
hm ->> rtc: Get hardware profiles

rtc ->> qnic: Initialization
qnic ->> qubit: Initialization
qnic ->> rtc: Ready
rtc ->> hm: Hardware Ready

```

### Perform Instruction
Related Components: RTC, HM, RE, HD

```mermaid
sequenceDiagram
autonumber

participant rtc as Real-Time Controller
participant hd as  Hardware Driver
participant re as Rule Engine
participant hm as Hardware Monitor

Note over rtc: Wait for api call
hm ->> rtc: (e.g.) Request photon emission (qubit id and timing) -- link

Note over rtc: Lock qubit
Note over rtc: Schedule photon emission
rtc ->> hd: Photon emission
Note over hd: Perform
hd ->> rtc: Done
Note over hd: Unlock Qubit
rtc ->> hm: Performed

re ->> rtc: Perform X gate (qubit id) -- ruleset
Note over rtc: Lock Qubit
rtc ->> hd: Request X gate
Note over hd: Perform
hd ->> rtc: Done
Note over rtc: Unlock Qubit
rtc ->> re: Performed
```

### Perform instruction to locked qubits
Related Components: RTC, HM, RE, HD

The instructions must be properly managed by higher components (such as RE, HM), however, in the case where there is multithreading, they might perform instructions to locked and used qubits.
Each instruction request must have timeout that specifies when the gate operation request is expired.

In the case where the instruction is scheduled but not performed yet, the qubit is still locked to ensure the exclusivity.

```mermaid
sequenceDiagram
autonumber

participant rtc as Real-Time Controller
participant hd as Hardware Driver
participant re as RuleEngine

re ->> rtc: Perform CX gate (qubit ids, timeout)
Note over rtc: Check lock status (Locked)
Note over rtc: Wait for unlock
hd ->> rtc: Done
Note over rtc: Unlock qubit
Note over rtc: Lock qubits
rtc ->> hd: Perform CX gate
Note over hd: Perform
hd ->> rtc: Done
Note over rtc: Unlock qubit
```

If the timeout exceeds, RTC returns error to corresponding components


## Interfaces

### Hardware
In this level, the granularity of the instruction is still vague. Actual operations are derived from these instructions.

- Stationary Qubit: matter qubits to store the quantum information
  - EmitPhoton: Emit a flying qubit entangled with stationary qubit.
  - GateX: X gate operation
  - GateY: Y gate operation
  - GateZ: Z gate operation
  - GateH: H gate operation
  - GateS: S gate operation
  - GateSdg: S dagger gate operation
  - GateT: T gate operation
  - GateTdg: T dagger gate operation
  - GateCX: CX gate operation
  - GateCX: CZ gate operation
  - Lock: Lock qubit to keep exclusiveness
  - Unlock: Unlock qubit for other thread to perform instructions
- Internal Flying BSA: Perform BSA for flying qubits
  - OpenDetector: Open photon detector to detect incoming photon
  - CloseDetector: Close photon detector
  - ExtractResult: Get detection results out of BSA
  - StreamResult (?): 
- Internal Stationary BSA: Bell state analyzer to peform internal Bell state measurement on stationary quantum memories
  - PerformBSA: Perform Bell state measurement between two stationary memories and return measurement results.
- ...

### Software
- RuleEngine, HardwareMonitor:
  - PerformInstruction: RuleEngine, HardwareMonitor can manipulate this API to perform instructions listed above
  - GetHardwareInformation: RE, HM can get hardware information
