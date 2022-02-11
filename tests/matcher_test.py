# from ..modules.matcher import NameMatcher
from modules.matcher import NameMatcher


matcher = NameMatcher()
# matcher.set_config(
#     source_file='data/full_names.json',
#     out_file='ai-models/matcher.mdl')
# matcher.fit()
# matcher.dump()

matcher.load('ai-models/matcher.mdl')
print(
    matcher.source[:5]
)