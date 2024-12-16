from types import NoneType
from werkzeug.datastructures.structures import ImmutableMultiDict, MultiDict
from enum import Enum


class CheckArgsEnum(Enum):
    none_max_size_arg = None
    none_only_new_arg = None
    off_only_new_arg = False
    on_only_new_arg = True

    none_enable_filter_by_price_arg = None
    off_enable_filter_by_price_arg = False
    on_enable_filter_by_price_arg = True

    none_enable_filter_by_name_arg = None
    off_enable_filter_by_name_arg = False
    on_enable_filter_by_name_arg = True


class RequestArgsMiddleware:

    def __init__(self, args: ImmutableMultiDict[str, str] | MultiDict[str, str]):
        self.args: ImmutableMultiDict[str, str] | MultiDict[str, str] = args

    def checking_allowed_request_args(self):
        all_args = self.args.keys()
        allowed_args: set[str] = {'q', 'ms', 'on', 'epf', 'enf', 'ew'}

        if len(all_args - allowed_args) > 0:
            return False
        else:
            return True

    def checking_overlapping_arguments(self) -> bool:
        enable_name_filter: NoneType | str = self.args.get('enf')
        query: None | str = self.args.get('q')
        exclusion_word: None | str = self.args.get('ew')

        if enable_name_filter in [None, NoneType, 'on'] and all([exclusion_word, query]):
            if exclusion_word.strip().lower() in [x.lower() for x in query.split()]:
                return False
            else:
                return True
        return True

    def checking_max_size_arg(self) -> CheckArgsEnum | int:
        max_size_arg: None | int = self.args.get('ms')
        if max_size_arg in [NoneType, None]:
            return CheckArgsEnum.none_max_size_arg
        else:
            try:
                map(int, [max_size_arg])
                if not (0 < int(max_size_arg) <= 40):
                    raise ValueError
            except ValueError:
                return False
            else:
                return int(max_size_arg)

    def checking_only_new_arg(self) -> bool | CheckArgsEnum:
        only_new_arg: None | str = self.args.get('on')
        if only_new_arg not in [None, NoneType, "off", "on"]:
            return False
        else:

            match only_new_arg:
                case "off":
                    only_new: CheckArgsEnum = CheckArgsEnum.off_only_new_arg
                case "on":
                    only_new: CheckArgsEnum = CheckArgsEnum.on_only_new_arg
                case _:
                    only_new: CheckArgsEnum = CheckArgsEnum.on_only_new_arg
            return only_new

    def checking_enable_filter_by_price_arg(self) -> bool | CheckArgsEnum:
        enable_filter_by_price_arg: None | str | CheckArgsEnum = self.args.get('epf')
        if enable_filter_by_price_arg not in [None, NoneType, "off", "on"]:
            return False
        else:
            match enable_filter_by_price_arg:
                case "off":
                    enable_filter_by_price_arg: CheckArgsEnum = CheckArgsEnum.off_enable_filter_by_price_arg
                case "on":
                    enable_filter_by_price_arg: CheckArgsEnum = CheckArgsEnum.on_enable_filter_by_price_arg
                case _:
                    enable_filter_by_price_arg: CheckArgsEnum = CheckArgsEnum.on_enable_filter_by_price_arg
            return enable_filter_by_price_arg

    def checking_enable_filter_by_name_arg(self) -> bool | CheckArgsEnum:
        enable_filter_by_name_arg: None | str | CheckArgsEnum = self.args.get('enf')
        if enable_filter_by_name_arg not in [None, NoneType, "off", "on"]:
            return False
        else:
            match enable_filter_by_name_arg:
                case "off":
                    enable_filter_by_name_arg: CheckArgsEnum = CheckArgsEnum.off_enable_filter_by_name_arg
                case "on":
                    enable_filter_by_name_arg: CheckArgsEnum = CheckArgsEnum.on_enable_filter_by_name_arg
                case _:
                    enable_filter_by_name_arg: CheckArgsEnum = CheckArgsEnum.on_enable_filter_by_name_arg
            return enable_filter_by_name_arg

    def checking_query_arg(self) -> bool | str:
        query_arg: None | str = self.args.get('q')
        if query_arg is None:
            return False
        else:
            return query_arg.replace('+', ' ')

    def checking_exclusion_word_arg(self) -> bool | str:
        exclusion_word: None | str = self.args.get('ew')
        if exclusion_word is None:
            return True
        else:
            return exclusion_word
