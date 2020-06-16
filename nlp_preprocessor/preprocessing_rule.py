class PreprocessingRule:

    def __init__(self, pattern, repl="", callback=None, desc=None):
        self.pattern = pattern
        self.repl = repl
        self.callback = callback
        self.desc = desc

    def __call__(self, text):
        """Apply a preprocessing rule. If the callback attribute of rule is None,
        then it will return a string using the rule pattern.sub method.
        If callback is not None, then then callback function will be executed using
        the the resulting match as an argument.
        """
        # If the rule just has a repl attribute,
        # Just return a simple re.sub
        if self.callback is None:
            return self.pattern.sub(self.repl, text)

        match = self.pattern.search(text)
        if match is None:
            return text
        return self.callback(match)
