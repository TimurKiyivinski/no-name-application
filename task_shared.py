#!/usr/bin/env python2

#Wraps a string
def wrapString(string, wrapper):
    wrapEnd = ''
    if wrapper == '[':
        wrapEnd = ']'
    elif wrapper == '{':
        wrapEnd = '}'
    elif wrapper == '(':
        wrapEnd = ')'
    elif wrapper == '<':
        wrapEnd = '>'
    else:
        return string
    return wrapper + string + wrapEnd

if __name__ == '__main__':
    print 'Please load this as a module.'
else:
    print 'Loaded as module: %s' % __name__
