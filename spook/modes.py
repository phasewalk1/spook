from enum import Enum

# used for help messages and descriptions
MODES = {
    "scripts (s)": "Collection of useful red-teaming scripts",
    "recon (r)": "Information Gathering and Reconnaissance Tools",
    "expl (e)": "Exploitation and Post-Exploitation Tools",
    "lateral (l)": "Lateral Movement and Privilege Escalation Tools",
}


class Mode(str, Enum):
    # fmt: off
    RECON = "recon"     or "r"
    EXPL = "expl"       or "e"
    LATERAL = "lateral" or "l"
    SCRIPTS = "scripts" or "s"
    # fmt: on

    @staticmethod
    def parse(s: str) -> Mode:
        s = s.lower()
        if s in ("recon", "r"):
            return Mode.RECON
        elif s in ("expl", "e"):
            return Mode.EXPL
        elif s in ("lateral", "l"):
            return Mode.LATERAL
        elif s in ("scripts", "s"):
            return Mode.SCRIPTS
        else:
            raise ValueError(f"Unknown mode: {s}")
