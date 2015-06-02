# -*- coding: utf-8 -*-

import re


class BaseType(object):
    def __init__(self, name=None):
        self.name = name

    def complete(self, token, tokens, context):
        return []

    def match(self, word, context, partial_line=None):
        return False

    def partial_match(self, word, context, partial_line=None):
        return False

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return '<%s>' % self.name
        return '<%s>' % self.__class__.__name__

class OrType(object):
    def __init__(self, *types, **kwargs):
        self.types = types
        self.name = kwargs.get('name', None)

    def complete(self, token, tokens, context):
        completions = []
        for t in self.types:
            completions.extend(t.complete(token, tokens, context))
        return completions

    def match(self, word, context, partial_line=None):
        for t in self.types:
            if t.match(word, context, partial_line):
                return True
        return False

    def partial_match(self, word, context, partial_line=None):
        for t in self.types:
            if t.partial_match(word, context, partial_line):
                return True
        return False

    def __str__(self):
        if hasattr(self, 'name') and self.name:
            return '<%s>' % self.name
        return '<%s>' % self.__class__.__name__



class OptionsType(BaseType):
    def __init__(self, valid_options, name=None):
        super(OptionsType, self).__init__()
        self.name = name
        self.valid_options = valid_options

    def match(self, word, context, partial_line=None):
        return word in self.valid_options

    def partial_match(self, word, context, partial_line=None):
        for op in self.valid_options:
            if op.startswith(word):
                return True
        return False

    def complete(self, token, tokens, context):
        return [(option, True) for option in self.valid_options if option.startswith(token)]

    def __str__(self):
        if not self.name is None:
            return '<%s>' % self.name
        return '<%s>' % ('|'.join(self.valid_options))


class StringType(BaseType):

    def __init__(self, name=None):
        super(StringType, self).__init__(name)

    def match(self, word, context, partial_line=None):
        return True

    def partial_match(self, word, context, partial_line=None):
        return True

class BoolType(OptionsType):

    def __init__(self, name=None):
        super(BoolType, self).__init__(['true', 'false'], name)


class IntegerType(BaseType):

    def __init__(self, min=None, max=None, name=None):
        super(IntegerType, self).__init__(name)
        self.min = min
        self.max = max

    def match(self, word, context, partial_line=None):
        try:
            if self.min is not None:
                if int(word) <= self.min:
                    return False
            if self.max is not None:
                if int(word) >= self.max:
                    return False
            return True
        except ValueError as exc:
            return False
    def partial_match(self, word, context, partial_line=None):
        return self.match(word, context, partial_line)


class RegexType(BaseType):
    def __init__(self, regex, name=None):
        super(RegexType, self).__init__(name)
        self.regex = re.compile(regex)

    def match(self, word, context, partial_line=None):
        return not self.regex.match(word) is None

    def partial_match(self, word, context, partial_line=None):
        return self.match(word, partial_line)
