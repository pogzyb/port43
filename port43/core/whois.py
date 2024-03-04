import shutil
import subprocess

from asyncwhois import whois, aio_whois


class WhoisError(Exception): ...


def get_whois_raw(domain: str) -> str:
    cmd = do_whois_command(domain)
    if cmd.returncode != 0:
        raise WhoisError(
            f"Command, whois {domain}, returned non-zero. stderr: {cmd.stderr}"
        )
    else:
        return cmd.stdout.decode(errors="ignore")


def do_whois_command(name: str):
    whois_exec = shutil.which("whois")
    if not whois_exec:
        raise FileNotFoundError("whois not found in $PATH")
    cmd = subprocess.run([whois_exec, "-HI", name], capture_output=True)
    return cmd


def get_whois(term: str, **kwargs) -> str:
    q, _ = whois(term, authoritative_only=True, **kwargs)
    # return json.dumps(parsed, default=lambda x: x.isoformat() if isinstance(x, datetime) else x)
    return q


async def aget_whois(term: str, **kwargs) -> str:
    q, _ = await aio_whois(term, authoritative_only=True, **kwargs)
    # return json.dumps(parsed, default=lambda x: x.isoformat() if isinstance(x, datetime) else x)
    return q
