from types import NoneType
from werkzeug.datastructures.structures import ImmutableMultiDict, MultiDict
from enum import Enum


class CheckArgsEnum(Enum):
    none_max_size_arg = None
    none_only_new_arg = None


class RequestArgsMiddleware:

    def __init__(self, args: ImmutableMultiDict[str, str] | MultiDict[str, str]):
        self.args: ImmutableMultiDict[str, str] | MultiDict[str, str] = args

    def check_allowed_request_args(self):
        all_args = self.args.keys()
        allowed_args: set[str] = {'q', 'ms', 'on'}

        if len(all_args - allowed_args) > 0:
            return False
        else:
            return True

    def check_max_size_arg(self) -> CheckArgsEnum | int:
        max_size_arg = self.args.get('ms')
        if max_size_arg in [NoneType, None]:
            return CheckArgsEnum.none_max_size_arg
        else:
            try:
                map(int, max_size_arg)
                if not (0 <= int(max_size_arg) <= 21):
                    raise ValueError
            except ValueError:
                return False
            else:
                return int(max_size_arg)

    def check_only_new_arg(self) -> bool | int:
        only_new_arg = self.args.get('on')
        if only_new_arg not in [None, NoneType, "0", "1"]:
            return False
        else:
            match only_new_arg:
                case "0":
                    only_new = False
                case "1":
                    only_new = True
                case _:
                    only_new = True
            return only_new

    def check_query_arg(self) -> bool | str:
        query_arg = self.args.get('q')
        if query_arg is None:
            return False
        else:
            return query_arg.replace('+', ' ')

