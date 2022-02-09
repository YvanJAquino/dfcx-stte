from secrets import SystemRandom
from modules.matcher import NameMatcher

matcher = NameMatcher.from_file('ai-models/matcher.mdl')
picker = SystemRandom()
sample = picker.choice(matcher.source)
res = matcher.match(sample)
print(res)