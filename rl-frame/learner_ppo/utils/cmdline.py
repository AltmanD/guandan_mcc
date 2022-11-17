def parse_cmdline_kwargs(args):
    """
    Copied from https://github.com/openai/baselines/blob/master/baselines/run.py
    convert a list of '='-spaced command-line arguments to a dictionary, evaluating python objects when possible
    """

    def parse(v):

        assert isinstance(v, str)
        try:
            return eval(v)
        except (NameError, SyntaxError):
            return v

    return {k: parse(v) for k, v in parse_unknown_args(args).items()}


def parse_unknown_args(args):
    """
    Copied from https://github.com/openai/baselines/blob/master/baselines/common/cmd_util.py
    Parse arguments not consumed by arg parser into a dictionary
    """
    retval = {}
    preceded_by_key = False
    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key = arg.split('=')[0][2:]
                value = arg.split('=')[1]
                retval[key] = value
            else:
                key = arg[2:]
                preceded_by_key = True
        elif preceded_by_key:
            retval[key] = arg
            preceded_by_key = False

    return retval
