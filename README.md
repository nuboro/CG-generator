# autocg

autocg generates a VISL CG-3 compatible Constraint Grammar file that
can be used for part-of-speech disambiguation. It takes an annotated
corpus in [Apertium stream
format](http://wiki.apertium.org/wiki/Apertium_stream_format) as an
input.

### Usage

Install [streamparser](https://github.com/apertium/streamparser) to
your computer. Then run:

```
$ ./autocg.py <annotated-corpus> -t <threshold> -m <min-count>
```

To get the documentation of the command line options run

```
$ ./autocg.py -h
```

### License

autocg is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

autocg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with autocg.  If not, see <http://www.gnu.org/licenses/>.
