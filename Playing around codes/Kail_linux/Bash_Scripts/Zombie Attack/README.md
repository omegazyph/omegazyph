# Zombie Attack Script (`Zombie_Attack.sh`)

This repository contains a simple Bash script designed to **demonstrate rapid system resource exhaustion** by continuously launching background processes, aptly named "Zombie Attack" due to the way it spawns numerous background (or "zombie-like") processes.

**🚨 WARNING: Running this script can severely impact your system's performance and stability, potentially leading to unresponsiveness or crashes. It is NOT intended for legitimate system operations and should be used with extreme caution in isolated environments only.**

---

## What It Does

The `Zombie_Attack.sh` script works by:

1. Entering an **infinite loop** (`while true`).
2. In each loop, it launches a new instance of the `yes` command.
3. The `yes` command runs with `nohup` (making it immune to terminal hangups) and is sent to the background (`&`).
4. Its output (endless 'y' characters) and any errors are redirected to `/dev/null` to prevent them from flooding your console.

Because each `yes` process runs independently in the background and never stops, this script quickly spawns hundreds, thousands, or even millions of processes. Each process consumes a small amount of **CPU** and **memory**. However, their sheer number will rapidly exhaust your system's resources, potentially leading to:

* Extreme system slowdown
* Inability to run new commands or open applications
* Potential system freezes or crashes
* Exhaustion of available Process IDs (PIDs)

---

## How to Run (and Why You Probably Shouldn't)

You can run this script like any other Bash script:

```bash
./Zombie_Attack.sh

However, it's strongly advised NOT to run this script on any system you value or rely on. Only execute this in a virtual machine or a disposable test environment where system instability is acceptable.

How to Stop It (If You Accidentally Run It)

If you've accidentally run this script and your system is becoming unresponsive, follow these steps to terminate the processes:

    Open a new terminal (if possible).

    Identify the script's main process and the spawned yes processes:
    Bash

ps aux | grep "Zombie_Attack.sh" | grep -v grep
ps aux | grep "yes" | grep -v grep

Look for the PID (Process ID) in the output.

Kill the main script process:
Bash

kill -9 <PID_of_the_script_bash_process>

Kill all yes processes:
Bash

    killall yes

    (You can also use pkill -f "yes" -U $(whoami) to kill only your user's yes processes.)

Purpose

This script serves as an educational example to illustrate:

    The behavior of infinite loops (while true).

    The use of nohup for running processes independently of a terminal session.

    Backgrounding processes using &.

    Input/output redirection (>, 2>&1, /dev/null).

    Crucially, the dangers of unchecked resource consumption in scripting.

Please use this responsibly and only for educational or testing purposes in controlled environments.
