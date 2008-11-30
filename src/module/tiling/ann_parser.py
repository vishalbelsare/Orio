#
# The implementation of annotation parser
#

import re, sys

#----------------------------------------------------------------

class AnnParser:
    '''The class definition for the annotation parser'''

    def __init__(self, perf_params):
        '''To instantiate the annotation parser'''

        self.perf_params = perf_params
    
    #------------------------------------------------------------

    def __evalExp(self, text):
        '''To evaluate the given expression text'''

        try:
            val = eval(text, self.perf_params)
        except Exception, e:
            print ('error:Tiling: failed to evaluate expression: "%s"' % text)
            print ' --> %s: %s' % (e.__class__.__name__, e)
            sys.exit(1)
        return val

    #------------------------------------------------------------

    def parse(self, text):
        '''
        Parse the given text to extract tiling information.
        The given code text has the following syntax:
          <num-tiling-level> : (<loop-iter>, ...) : (<tile-size>, ...), ...
        '''

        # remember the given code text
        orig_text = text

        # regular expressions
        __num_re = r'\s*(\d+)\s*'
        __var_re = r'\s*([A-Za-z_]\w*)\s*'
        __colon_re = r'\s*:\s*'
        __comma_re = r'\s*,\s*'
        __oparenth_re = r'\s*\(\s*'
        __cparenth_re = r'\s*\)\s*'

        # get the number of tiling levels
        m = re.match(__num_re, text)
        if not m:
            m = re.match(__var_re, text)
        if not m:
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)
        text = text[m.end():]
        num_level = m.group(1)
        num_level = self.__evalExp(num_level)

        # check the semantic of the number of tiling levels
        if not isinstance(num_level, int) or num_level <= 0:
            print 'error:Tiling: the number of tiling levels must be a positive integer'
            sys.exit(1)

        # get a colon
        m = re.match(__colon_re, text)
        if not m:
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)
        text = text[m.end():]

        # get the list of iterator names of the loops to be tiled
        m = re.match(__oparenth_re, text)
        if not m:
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)
        text = text[m.end():]        
        m = re.search(__cparenth_re, text)
        if not m:
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)
        itext = text[:m.end()-1]
        text = text[m.end():]
        iter_names = [] 
        while True:
            if (not itext) or itext.isspace():
                break
            m = re.match(__var_re, itext)
            if not m:
                print 'error:Tiling: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            iter_names.append(m.group(1))
            itext = itext[m.end():]
            m = re.match(__comma_re, itext)
            if m:
                itext = itext[m.end():]

        # create a data structure to store the tiling information
        tiling_table = {}
        for i in iter_names:
            tiling_table[i] = []
        tiling_info = (num_level, tiling_table)

        # check if the tile sizes are specified or not
        if (not text) or text.isspace():
            return tiling_info

        # get a colon
        m = re.match(__colon_re, text)
        if not m:
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)
        text = text[m.end():]

        # get the tile sizes
        tile_sizes = []
        for tlevel in range(1,num_level+1):
            m = re.match(__oparenth_re, text)
            if not m:
                print 'error:Tiling: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            text = text[m.end():]        
            m = re.search(__cparenth_re, text)
            if not m:
                print 'error:Tiling: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            itext = text[:m.end()-1]
            text = text[m.end():]
            m = re.match(__comma_re, text)
            if m:
                text = text[m.end():]
            tile_sizes.append([])
            for iname in iter_names:
                m = re.match(__num_re, itext)
                if not m:
                    m = re.match(__var_re, itext)
                if not m:
                    print 'error:Tiling: annotation syntax error: "%s"' % orig_text
                    sys.exit(1)
                tsize = self.__evalExp(m.group(1))
                tile_sizes[-1].append(tsize)
                itext = itext[m.end():]
                m = re.match(__comma_re, itext)
                if m:
                    itext = itext[m.end():]
            if itext and not itext.isspace():
                print 'error:Tiling: annotation syntax error: "%s"' % orig_text
                sys.exit(1)

        # is there any trailing texts?
        if text and not text.isspace():
            print 'error:Tiling: annotation syntax error: "%s"' % orig_text
            sys.exit(1)

        # update the tiling information with tile sizes
        tile_sizes = zip(*tile_sizes)
        for i, iname in enumerate(iter_names):
            tiling_table[iname].extend(tile_sizes[i])

        # check the semantics of the tile sizes
        for iname in iter_names:
            tsizes = tiling_table[iname]
            for t in tsizes:
                if not isinstance(t, int) or t <= 0:
                    print 'error:Tiling: a tile size must be a positive integer, obtained: "%s"' % t
                    sys.exit(1)
            for i, cur_t in enumerate(tsizes):
                for j, next_t in enumerate(tsizes[i+1:]):
                    if cur_t % next_t != 0:
                        print (('error:Tiling: level-%s tile size of %s must be divisible by ' +
                               'level-%s tile size of %s') % (i+1, cur_t, i+1+j+1, next_t))
                        sys.exit(1)
        
        # return the tiling information
        return tiling_info





