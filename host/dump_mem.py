"""
Adapted from hhttps://github.com/dhylands/json-ipc/blob/master/dump_mem.py

MIT License

Copyright (c) 2016 Dave Hylands

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""Provides the dump_mem function, which dumps memory in hex/ASCII."""

import sys
if sys.implementation.name == 'micropython':
    import ubinascii
    def hexlify(buf):
        return ubinascii.hexlify(buf, ' ')
else:
    def hexlify(buf):
        # CPython's hexlify doesn't have the notion of a seperator character
        # so we just do this the old fashioned way
        return bytes(' '.join(['{:02x}'.format(b) for b in buf]), 'ascii')


def dump_mem(buf, prefix='', address=0, line_width=16, show_ascii=True,
             show_addr=True, log=print):
    """Dumps out a hex/ASCII representation of the given buffer."""
    if line_width < 0:
        line_width = 16
    if len(prefix) > 0:
        prefix += ':'
    if len(buf) == 0:
        log(prefix + 'No data')
        return
    buf_len = len(buf)
    mv = memoryview(buf)
    
    prefix_bytes = bytes(prefix, 'utf-8')
    prefix_len = len(prefix_bytes)
    out_len = prefix_len
    if show_addr:
        out_len += 6
    hex_offset = out_len
    out_len += line_width * 3
    if show_ascii:
        ascii_offset = out_len + 1
        out_len += line_width + 1
    out_line = memoryview(bytearray(out_len))
    out_line[0:prefix_len] = prefix_bytes

    line_hex = out_line[hex_offset:hex_offset + (line_width * 3)]
    line_hex[0] = ord(' ')
    if show_ascii:
        out_line[ascii_offset - 1] = ord(' ')
        line_ascii = out_line[ascii_offset:ascii_offset + line_width]

    for offset in range(0, buf_len, line_width):
        if show_addr:
            out_line[prefix_len:prefix_len + 6] = bytes(' {:04x}:'.format(address), 'ascii')
        line_bytes = min(buf_len - offset, line_width)
        line_hex[1:(line_bytes * 3)] = hexlify(mv[offset:offset+line_bytes])
        if line_bytes < line_width:
            line_hex[line_bytes * 3:] = b'   ' * (line_width - line_bytes)
        if show_ascii:
            line_ascii[0:line_bytes] = mv[offset:offset + line_bytes]
            if line_bytes < line_width:
                line_ascii[line_bytes:] = b' ' * (line_width - line_bytes)
            for i in range(line_bytes):
                char = line_ascii[i]
                if char < 0x20 or char > 0x7e:
                    line_ascii[i] = ord('.')
        log(bytes(out_line).decode('utf-8'))
        address += line_width
