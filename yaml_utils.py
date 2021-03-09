import yaml
from os import path, environ
from attrdict import AttrDict

def load_yaml(fl, yaml_relpath):
    ret = AttrDict()
    ret.HOME = environ['HOME']
    ret.SCRIPTDIR = path.dirname(path.abspath(fl))
    yaml_path = path.join(ret.SCRIPTDIR, yaml_relpath)
    with open(yaml_path) as f:
        tmp = yaml.safe_load(f)
    ret.update(tmp)
    return ret

def hierarchical_load_yaml(
        fl,
        yaml_root_relpath,
        yaml_end_relpath,
        default_filename='default.yml',
        verbose=True
    ):
    from .utils import deepupdate
    ret = dict()
    scriptdir = path.dirname(path.abspath(fl))
    yaml_root_path = path.normpath(path.join(scriptdir, yaml_root_relpath))
    yaml_end_path = path.join(scriptdir, yaml_end_relpath)
    subpaths = path.relpath(yaml_end_path, yaml_root_path).split('/')
    tmp_path = yaml_root_path
    for subpath in subpaths:
        tmp_fl = path.join(tmp_path, default_filename)
        if path.isfile(tmp_fl):
            if verbose:
                print(f'LOAD: {tmp_fl}')
            with open(tmp_fl) as f:
                deepupdate(ret, yaml.safe_load(f))
        tmp_path = path.join(tmp_path, subpath)
    else:
        tmp_fl = tmp_path
        if verbose:
            print(f'LOAD: {tmp_fl}')
        with open(tmp_fl) as f:
            deepupdate(ret, yaml.safe_load(f))
    return AttrDict(ret)
