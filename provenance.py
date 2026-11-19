"""Records the software environment with every analysis output (Chapter 3, §3.12: versions are recorded)."""
import platform, sys, datetime


def environment():
    """Python, platform and package versions, plus a UTC timestamp."""
    out = {'python': sys.version.split()[0], 'platform': platform.platform(),
           'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}
    for name in ('numpy', 'scipy', 'sklearn', 'matplotlib', 'openpyxl'):
        try:
            out[name] = __import__(name).__version__
        except Exception:          # package not installed in this environment
            out[name] = None
    return out
