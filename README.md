# qrsa
Quantum Repeater/Router Software Architecture (QRSA) is a software architectural proposal for recursive quantum networks [^VAN2022] (https://github.com/sfc-aqua/qrsa/tree/main#references).

## Design
The main software components in current version of QRSA are listed as follow [^SAT2022](https://github.com/sfc-aqua/qrsa/tree/main#references): 
1. [ConnectionManager(CM)](https://github.com/sfc-aqua/qrsa/tree/main/qrsa/src/connection_manager)
1. [HardwareMonitor(HM)](https://github.com/sfc-aqua/qrsa/tree/main/qrsa/src/hardware_monitor)
1. [Real-TimeController(RTC)](https://github.com/sfc-aqua/qrsa/tree/main/qrsa/src/realtime_controller)
1. [RoutingDaemon(RD)](https://github.com/sfc-aqua/qrsa/tree/main/qrsa/src/routing_daemon)
1. [RuleEngine(RE)](https://github.com/sfc-aqua/qrsa/tree/main/qrsa/src/rule_engine)

## Implementation


## Test strategy
### Unittesting

### Integrated test

### CI/CD
We could use [self-hosted runner](https://docs.github.com/ja/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) for Rasberry Pi Test?


## Compile options
- Debug
- Simulation
- Deployable

## References
- [^VAN2022](https://ieeexplore.ieee.org/abstract/document/9951258) Van Meter, Rodney, et al. "A quantum internet architecture." 2022 IEEE International Conference on Quantum Computing and Engineering (QCE). IEEE, 2022. 
- [^SAT2022](https://ieeexplore.ieee.org/abstract/document/9951186) Ryosuke Satoh, et al. "Quisp: a quantum internet simulation package." 2022 IEEE International Conference on Quantum Computing and Engineering (QCE). IEEE, 2022. 



