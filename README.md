# pythoncommons

## Introduction

Python commons, or more stylishly, pythoncommons, is a collection of mostly
functional, generic, useful utilities libraries. This package is used heavily in both
Harness platform packages - mars and harness.

These libraries are separated into behavior sets, for example, mongo utilities,
record reader utilities, property reader utilities, etc. These libraries should
resist becoming too large

## Development

Pythoncommons is stable, and perhaps not perfectly organized, but should contain
functional behavior related to the harness platform that can be reused.

When modules begin getting too large, or too diverse, they should be organized into subpackages -
for example, we have a mongo utilities package, but if we were to add support for an in memory
database, such as mdb, or another type of database, we should probably make a subpackage called
databse_utils, which then can top-level import for namespace purposes or interface purposes
database specific properties.

Or as another example, we have property reader and writer utils. These could probably be grouped into
a property utils subpackage.

Also, the general_utils holds utilities for which we don't have enough behavior to create an entire library yet.
As singular functions are added and become groups of functions, groups should develop and be added to existing
libraries or new behavioral libraries.

## License

MIT Standard

Copyright 2016-2020 Ryan Berkheimer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
