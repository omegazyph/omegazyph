# Network Scanner Script (Ping Sweep)

**Author**: Wayne Stock  
**Date**: May 20, 2025  

## Description

This Bash script performs a simple **ping sweep** to identify live hosts within a `/24` subnet. It sequentially pings IP addresses from `.1` to `.254` using the specified subnet prefix and returns the active hosts that respond.

## Usage

```bash
./ipsweep.sh <subnet-prefix>
