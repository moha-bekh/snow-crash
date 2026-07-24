# level09

## Goal

Recover the password stored in the `token` file by reversing the custom encoding implemented by the SUID binary.

## Enumeration

List the available files:

```bash
ls -l
```

Output:

```text
-rwsr-sr-x 1 flag09 level09 level09
----r--r-- 1 flag09 level09 token
```

Inspect the binary:

```bash
file level09
strings level09
```

The binary contains anti-reverse-engineering checks (`LD_PRELOAD`, `ptrace`, `/proc/self/maps`) but no obvious vulnerability.

## Analysis

Executing the binary with a simple string:

```bash
./level09 token
```

produces:

```text
tpmhr
```

Comparing the input and output:

| Input | Output | Offset |
| ----- | ------ | ------ |
| t     | t      | +0     |
| o     | p      | +1     |
| k     | m      | +2     |
| e     | h      | +3     |
| n     | r      | +4     |

Each character is shifted by its position in the string:

```text
encoded[i] = original[i] + i
```

To recover the original password, the operation must be reversed:

```text
original[i] = encoded[i] - i
```

## Exploitation

Create a small Python script:

```python
#!/usr/bin/env python

data = open("/home/user/level09/token", "rb").read().strip()

out = ""

for i, c in enumerate(data):
    out += chr(ord(c) - i)

print(out)
```

Execute it:

```bash
python /tmp/test
```

Output:

```text
f3iji1ju5yuevaus41q1afiuq
```

## Validation

Use the recovered password:

```bash
su flag09
getflag
```

Output:

```text
Check flag.Here is your token :
s5cAJpM8ev6XHw998pRWG728z
```

The returned token is the password for `level10`.

## Concept

Encoding algorithm:

```text
Original string
        ↓
For each character:
char + index
        ↓
Encoded string
```

Decoding algorithm:

```text
Encoded string
        ↓
For each character:
char - index
        ↓
Original string
```

## Security Impact

This level demonstrates that **custom encoding is not encryption**.

Because the transformation is deterministic and reversible, anyone who understands the algorithm can recover the original secret.

Sensitive data should always be protected using established cryptographic algorithms instead of proprietary encoding schemes.

## Resources

Useful commands:

```bash
./level09 token
cat token
python /tmp/test

su flag09
getflag
```
