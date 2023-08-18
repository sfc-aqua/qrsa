from typing import Union
from ipaddress import IPv4Address, IPv6Address


IpAddressType = Union[IPv4Address, IPv6Address, str]
