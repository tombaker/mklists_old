from dataclasses import dataclass

class XError(Exception): pass

@dataclass
class Rule:
    source: str = None
    target: str = None

    initialized = False
    sources = []

    @classmethod
    def register(cls, self):
        if not cls.initialized:
            cls.sources.append(self.source)
            cls.initialized = True
            print('appending to Rule.sources and changing flag to True')
        if self.source not in cls.sources:
            print(f"Oh no! {self.source} is not one of {cls.sources}!")
            raise XError
        if self.target not in cls.sources:
            cls.sources.append(self.target)
        print(cls.sources)

if __name__ == "__main__":
    x = Rule('asdf', 'jkl')
    Rule.register(x)
    y = Rule('asdf', 'uiop')
    Rule.register(y)
    z = Rule('wer', 'uiop')
    Rule.register(z)
