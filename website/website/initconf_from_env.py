"called by .settings"

from os import getenv, pathsep
from email.utils import parseaddr

_LOG = True  # default value

def log_init_if(name, val, env_name=None, log=_LOG):
    if log:
        if env_name is None:
            env_name = name
        print(f"[settings] init {name}={val!r} from env {env_name} \t({__name__})")

def init_by(settings_, key, log=_LOG) -> bool:
    "do nothing if env `key` is not set."
    val = getenv(key)
    if val is not None:
        log_init_if(key, val, log=log)
        settings_[key] = val
        return True
    else:
        return False


def chk_init_by(settings_, key, log=_LOG):
    "Raises OSError if env `key` is not set."
    if not init_by(settings_, key, log=log):
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

def init_list_env(setting_, name: str, env_name=None, mapper=None, log=_LOG) -> bool:
    if env_name is None: env_name = name
    val = getenv(env_name)
    if val is None: return False
    ls = val.split(pathsep)
    if mapper is not None:
        ls = list(map(mapper, ls))
    log_init_if(name, ls, env_name=env_name, log=log)
    setting_[name] = ls
    return True

DEBUG_ENV = "WEBSITE_DEBUG"
ADMINS_ENV = "WEBSITE_ADMINS"
def init_debug(settings_, log=_LOG):
    """get env WEBSITE_DEBUG.
    if true, then get ALLOWED_HOSTS, use os.pathsep split it.
    
    may raise OSError"""
    key = DEBUG_ENV
    val = getenv(key)
    if val is None:
        return
    debug = parse_bool_like(val)
    settings_["DEBUG"] = debug
    log_init_if("DEBUG", debug, env_name=DEBUG_ENV, log=log)
    if debug:
        return
    hosts_env = 'ALLOWED_HOSTS'
    if not init_list_env(settings_, "ALLOWED_HOSTS", log=log):
        raise OSError("if not DEBUG, you must set "+hosts_env)
    
    def parse_admin(s: str):
        return parseaddr(s)
    init_list_env(settings_, "ADMINS", env_name=ADMINS_ENV,
                  mapper=parse_admin, log=_LOG)


chk_init_envs = [

]

init_envs = [
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "DEFAULT_FROM_EMAIL",
]


def init(settings, log=_LOG):
    init_debug(settings, log=log)
    for k in chk_init_envs: chk_init_by(settings, k, log=log)
    for k in init_envs: init_by(settings, k, log=log)
