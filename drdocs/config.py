# -*- coding: utf-8 -*-
# constants below often assume fractional values so make py2/py3 float division the default
from __future__ import division


# TODO: replace this with actually configurable values once defaults are figured out

# The mccabe library used by this library uses a calculation of E - N + 2. Picking a ratio
# of comments to complexity is somewhat arbitrary so this author is picking a personal
# preference based on guesswork.
# https://en.wikipedia.org/wiki/Cyclomatic_complexity
INLINE_COMMENTS_PER_COMPLEXITY = 1 // 4
# so there should be 1 comment for every 4 complexity (roughly representing 4 lines of code or at least paths)
