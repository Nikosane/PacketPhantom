# PacketPhantom

## Overview
This project demonstrates ARP poisoning to facilitate a Man-in-the-Middle (MITM) attack. It redirects traffic between a victim and a gateway to the attacker's machine, allowing packet interception or modification.

⚠️ **Ethical Use Only:** Use this tool responsibly and only with explicit permission on networks you own or are authorized to test.

## Features
- ARP spoofing to redirect traffic.
- IP forwarding to maintain network connectivity.
- Automatic restoration of ARP tables after the attack.

## Requirements
- Python 3.8 or higher
- Root or Administrator privileges
- `scapy` library

## Setup
1. Clone the repository:
```
git clone https://github.com/Nikosane/PacketPhantom.git
```

2. Navigate to the project directory:
```
cd PacketPhanton
```
3. Install dependencies:
```
pip install -r requirements.txt
```
---
## Usage
1. Run the script as root:
```
sudo python3 arp_poisoning.py
```
2. Enter the target IP and gateway IP when prompted.
3. Press `Ctrl+C` to stop the attack and restore the ARP tables.

## Legal Disclaimer
This tool is intended for authorized security assessments only. Unauthorized use of this tool is illegal and unethical. The author is not responsible for any misuse.
