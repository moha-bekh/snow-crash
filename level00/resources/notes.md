# level00

## Goal

Find the password required to access the `flag00` account and retrieve the token for the next level.

## Enumeration

Search for files owned by `flag00`:

```bash
find / -user flag00 2>/dev/null
```

Result:

```text
/usr/sbin/john
/rofs/usr/sbin/john
```

Read the file:

```bash
cat /usr/sbin/john
```

Content:

```text
cdiiddwpgswtgt
```

## Analysis

The filename `john` is a hint that the stored value is not directly usable.

The string is encoded using a **Caesar cipher** (ROT shift). Brute-forcing all 26 possible shifts reveals:

```text
Shift 11: nottoohardhere
```

## Exploitation

Switch to the `flag00` user:

```bash
su flag00
```

Password:

```text
nottoohardhere
```

Retrieve the token:

```bash
getflag
```

Output:

```text
Check flag. Here is your token:
x24ti5gi3x0ol2eh4esiuxias
```

## Result

The token returned by `getflag` is the password for the `level01` account.

```bash
su - level01
Password: x24ti5gi3x0ol2eh4esiuxias
```

## Resources

### Enumeration

```bash
find / -user flag00 2>/dev/null
cat /usr/sbin/john
```

### Decoder

A simple Caesar cipher brute-force script (`decode.py`) was used to test every possible shift and identify the plaintext.
