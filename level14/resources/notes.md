# level14

## Goal

Retrieve the final token by reverse engineering and manipulating the `getflag` binary at runtime.

---

## Recon

The home directory does not contain a level-specific executable:

```bash
ls -la
```

No SUID file owned by `level14` was found:

```bash
find / -user level14 -perm -4000 2>/dev/null
```

The interesting target is the global `getflag` binary:

```bash
which getflag
strings $(which getflag)
```

Interesting strings:

```text
LD_PRELOAD detected
You should not reverse this
Check flag.Here is your token :
You are root are you that dumb ?
Nope there is no token here for you sorry. Try again :)
```

---

## Analysis

`getflag` contains anti-debugging logic using `ptrace`.

Relevant assembly:

```asm
call ptrace@plt
test eax,eax
jns  <continue>
```

When running under GDB, `ptrace()` fails and the program exits with:

```text
You should not reverse this
```

This protection can be bypassed by modifying the return value of `ptrace()` or by continuing execution after the check.

---

## UID Check

Later, `getflag` calls `getuid()`:

```asm
0x8048afd  call getuid@plt
0x8048b02  mov %eax,0x18(%esp)
0x8048b06  mov 0x18(%esp),%eax
0x8048b0a  cmp $0xbbe,%eax
```

The binary selects which token to print based on the UID.

The UID of `flag14` is:

```bash
id flag14
```

Output:

```text
uid=3014(flag14)
```

Decimal and hexadecimal:

```text
3014 = 0xbc6
```

---

## Exploitation

Open `getflag` in GDB:

```bash
gdb /bin/getflag
```

Bypass or pass the anti-debugging check, then break after the `getuid()` result is loaded:

```gdb
break *0x8048b0a
run
```

At the breakpoint, force the UID value:

```gdb
set $eax = 3014
continue
```

Output:

```text
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbp
```

---

## Why It Works

On x86, function return values are stored in the `EAX` register.

`getflag` uses the value returned by `getuid()` to decide which token to decrypt and print.

By changing `EAX` before the UID comparisons, the program believes it was executed by `flag14` and prints the corresponding token.

---

## Important Notes

Setting `$eax = 0` triggers the root case:

```text
You are root are you that dumb ?
```

The correct UID is not root, but `flag14`:

```text
3014
```

Breaking directly on `getuid` is not enough, because the function overwrites `$eax` before returning. The register must be modified after `getuid()` returns.

---

## Useful Commands

Disable broken GDB TUI layout:

```gdb
tui disable
```

or:

```text
Ctrl-x a
```

Disassemble:

```gdb
set disassembly-flavor intel
disassemble main
```

Breakpoint after UID check setup:

```gdb
break *0x8048b0a
```

Modify UID:

```gdb
set $eax = 3014
continue
```

---

## Vulnerability Category

* Reverse Engineering
* Anti-debug Bypass
* Runtime Register Manipulation
* Authorization Bypass
