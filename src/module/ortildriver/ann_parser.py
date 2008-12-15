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
            print ('error:OrTilDriver: failed to evaluate expression: "%s"' % text)
            print ' --> %s: %s' % (e.__class__.__name__, e)
            sys.exit(1)
        return val

    #------------------------------------------------------------

    def parse(self, text):
        '''
        Parse the given text to extract variable-value pairs.
        The given code text has the following syntax:
          <var1> = <num1>, <var2> = <num2>, ...
        '''

        # remember the given code text
        orig_text = text

        # regular expressions
        __num_re = r'\s*(\d+)\s*'
        __var_re = r'\s*([A-Za-z_]\w*)\s*'
        __comma_re = r'\s*,\s*'
        __equal_re = r'\s*=\s*'

        # initialize the data structure to store all variable-value pairs
        var_val_pairs = []

        # get all variable-value pairs
        while True:
            if (not text) or text.isspace():
                break
            m = re.match(__var_re, text)
            if not m:
                print 'error:OrTilDriver: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            text = text[m.end():]
            var = m.group(1)
            m = re.match(__equal_re, text)
            if not m:
                print 'error:OrTilDriver: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            text = text[m.end():]
            m = re.match(__var_re, text)
            if not m:
                m = re.match(__num_re, text)
            if not m:
                print 'error:OrTilDriver: annotation syntax error: "%s"' % orig_text
                sys.exit(1)
            text = text[m.end():]
            val = m.group(1)
            var_val_pairs.append((var, val))
            m = re.match(__comma_re, text)
            if m:
                text = text[m.end():]

        # evaluate all values and check their semantics
        n_var_val_pairs = []
        for var, val in var_val_pairs:
            val = self.__evalExp(val)
            if not isinstance(val, int) or val <= 0:
                print 'error:OrTilDriver: variable value must be a positive integer'
                sys.exit(1)
            n_var_val_pairs.append((var, val))
        var_val_pairs = n_var_val_pairs

        # return all variable value pairs
        return var_val_pairs
