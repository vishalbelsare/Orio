#
# The class for loop transformation module
#

import sys
import codegen, module.module, parser, transformator

#-----------------------------------------

class Loop(module.module.Module):
    '''Loop transformation module'''
    
    def __init__(self, cmd_line_opts, perf_params, module_code, line_no,
                 indent_size, annot_body_code):
        '''To instantiate a loop transformation module'''
        
        module.module.Module.__init__(self, cmd_line_opts, perf_params, module_code, line_no,
                                      indent_size, annot_body_code)

    #---------------------------------------------------------------------
    
    def transform(self):
        '''To apply loop transformations on the annotated code'''

        # parse the code to get the AST
        stmts = parser.getParser(self.line_no).parse(self.module_code)

        # apply transformations
        t = transformator.Transformator(self.perf_params, self.verbose)
        transformed_stmts = t.transform(stmts)
        
        # generate code for the transformed ASTs
        indent = ' ' * self.indent_size
        extra_indent = '  '
        cgen = codegen.CodeGen()
        transformed_code = ''
        for s in transformed_stmts:
            transformed_code += cgen.generate(s, indent, extra_indent)

        # return the transformed code
        return transformed_code

