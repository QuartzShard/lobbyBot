## This file is what gets called on `import lib`
## The contents here determine what is available directly from lib,
## and what is available as lib.<module>

## Expose contents as part of lib
from .common import *

## Expose contents as part of lib.<module>
from . import role
