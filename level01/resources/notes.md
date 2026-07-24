# level01

## Goal

Recover the password of the `flag01` user and obtain the token for `level02`.

## Enumeration

Inspect `/etc/passwd`:

```bash
cat /etc/passwd | grep flag01
```

Output:

```text
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```

## Analysis

On a modern Linux system, the password field in `/etc/passwd` usually contains `x`, meaning the real password hash is stored in `/etc/shadow`.

Here, the hash is directly visible in `/etc/passwd`:

```text
42hDRfypTqqnw
```

This is a traditional Unix DES `crypt(3)` hash.

Because `/etc/passwd` is readable by all users, the hash can be extracted and cracked offline.

## Exploitation

Create a hash file:

```bash
echo "flag01:42hDRfypTqqnw" > hash.txt
```

Run John the Ripper on the host machine:

```bash
john hash.txt
```

Recovered password:

```text
abcdefg
```

## Validation

Switch to `flag01`:

```bash
su flag01
```

Password:

```text
abcdefg
```

Retrieve the token:

```bash
getflag
```

The token returned by `getflag` is the password for `level02`.

## Resources

- `crack.sh`: creates the hash file and runs John the Ripper.
