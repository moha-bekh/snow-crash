# level02

## Goal

Recover the password of the `flag02` account from a packet capture.

## Enumeration

Open `level02.pcap` with Wireshark.

Select the Telnet conversation and use:

**Follow → TCP Stream**

## Analysis

The TCP stream shows the login sequence and the password keystrokes.

The stream contains `0x7f` bytes, corresponding to the DEL / Backspace key.

Original keystrokes:

```text
ft_wandr<DEL><DEL><DEL>NDRel<DEL>L0L
```

Replaying the keystrokes gives the final password:

```text
ft_waNDReL0L
```

## Validation

```bash
su flag02
getflag
```

The token returned by `getflag` is the password for `level03`.

## Concept

This level demonstrates why Telnet is insecure:

- credentials are transmitted in clear text;
- editing keys are also transmitted;
- a packet capture is enough to reconstruct the final password.
