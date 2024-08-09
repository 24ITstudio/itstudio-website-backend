"called by .settings"

from os import getenv, pathsep
from email.utils import parseaddr

def init_by(settings_, key):
    "do nothing if env `key` is not set."
    val = getenv(key)
    if val is not None:
        settings_[key] = val


def chk_init_by(settings_, key):
    "Raises OSError if env `key` is not set."
    val = getenv(key)
    if val is not None:
        settings_[key] = val
    else:
        raise OSError("the envvar '"+key+"' is not set, cannot send email")

def parse_bool(s):
    "returns None if fails"
    sl = s.lower()
    if sl == "true":
        return True
    elif sl == "false":
        return False

def parse_bool_like(val) -> bool:
    err_msg = "bool or 1/0 expected, but got {}"
    def err():
        raise ValueError(err_msg.format(val))
    le = len(val)
    if le == 0:
        err()
    if val[0] in {'t', 'T', 'f', 'F'}:
        # might be bool
        b = parse_bool(val)
        if b is None:
            err()
        return b
    else:
        if le != 1:
            err()
        c = val[0]
        if c == '1': return True
        if c == '0': return False
        err()


def init_list_env(setting_, name: str, env_name=None, mapper=None) -> bool:
    if env_name is None: env_name = name
    val = getenv(env_name)
    if val is None: return False
    ls = val.split(pathsep)
    if mapper is not None:
        ls = list(map(mapper, ls))
    setting_[name] = ls
    return True

DEBUG_ENV = "WEBSITE_DEBUG"
ADMINS_ENV = "WEBSITE_ADMINS"
def init_debug(settings_):
    """get env WEBSITE_DEBUG.
    if true, then get ALLOWED_HOSTS, use os.pathsep split it.
    
    may raise OSError"""
    key = DEBUG_ENV
    val = getenv(key)
    if val is None:
        return
    debug = parse_bool_like(val)
    settings_["DEBUG"] = debug
    if debug:
        return
    hosts_env = 'ALLOWED_HOSTS'
    if not init_list_env(settings_, "ALLOWED_HOSTS"):
        raise OSError("if not DEBUG, you must set "+hosts_env)
    
    def parse_admin(s: str):
        return parseaddr(s)
    init_list_env(settings_, "ADMINS", env_name=ADMINS_ENV,
                  mapper=parse_admin)


chk_init_envs = [

]

init_envs = [

]


def init(settings):
    init_debug(settings)
    for k in chk_init_envs: chk_init_by(settings, k)
    for k in init_envs: chk_init_by(settings, k)
