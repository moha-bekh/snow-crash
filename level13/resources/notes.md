# level13

## Goal

Bypass a UID check inside a SUID binary and retrieve the token for `level14`.

---

## Recon

List files:

```bash
ls -la
```

Output:

```text
-rwsr-sr-x 1 flag13 level13 7303 Aug 30 2015 level13
```

The binary is:

* SUID
* dynamically linked
* not stripped

```bash
file level13
```

Output:

```text
setuid setgid ELF 32-bit LSB executable, dynamically linked, not stripped
```

Running the binary:

```bash
./level13
```

produces:

```text
UID 2013 started us but we expect 4242
```

---

## Static Analysis

Useful strings:

```bash
strings level13
```

Interesting output:

```text
getuid
UID %d started us but we expect %d
your token is %s
```

This strongly suggests that the program:

1. calls `getuid()`;
2. compares the returned value with `4242`;
3. prints a token if the comparison succeeds.

---

## Reverse Engineering

Open the binary with GDB:

```bash
gdb ./level13
```

Disassembly of `main`:

```asm
0x8048595    call   getuid@plt
0x804859a    cmp    $0x1092,%eax
0x804859f    je     0x80485cb
```

Where:

```text
0x1092 = 4242
```

Equivalent logic:

```c
if (getuid() == 4242)
{
    print_token();
}
else
{
    printf("UID %d started us but we expect 4242\n");
    exit(1);
}
```

---

## Vulnerability

The application relies exclusively on the return value of `getuid()`.

By modifying the register containing the return value during execution, the check can be bypassed.

This is a classic reverse engineering / runtime manipulation challenge.

---

## Exploitation

Start GDB:

```bash
gdb ./level13
```

Set a breakpoint immediately after the `getuid()` call:

```gdb
break *0x804859a
```

Run the program:

```gdb
run
```

Execution stops just before:

```asm
cmp $0x1092,%eax
```

Force the return value:

```gdb
set $eax = 4242
```

Continue execution:

```gdb
continue
```

Output:

```text
your token is 2A31L79asukciNyi8uppkEuSx
```

Use the token to access the next level:

```bash
su level14
```

---

## Why It Works

On x86, function return values are stored in the `EAX` register.

After:

```asm
call getuid
```

the UID returned by `getuid()` is stored in `EAX`.

The program immediately compares:

```asm
cmp $0x1092,%eax
```

Changing `EAX` before the comparison makes the program believe that `getuid()` returned `4242`, allowing execution to follow the success path without modifying the binary.

---

## Security Lessons

* Client-side or runtime checks can be bypassed through debugging.
* Never rely solely on a user-controlled or easily hookable function for security decisions.
* Reverse engineering tools such as GDB can modify registers and memory at runtime.
* Protecting privileged code requires more than a simple UID comparison.

---

## Useful Commands

Inspect strings:

```bash
strings level13
```

Open in GDB:

```bash
gdb ./level13
```

Set breakpoint:

```gdb
break *0x804859a
```

Run:

```gdb
run
```

Modify register:

```gdb
set $eax = 4242
```

Continue:

```gdb
continue
```

---

## Vulnerability Category

* Reverse Engineering
* Runtime State Manipulation
* Authentication / Authorization Bypass
