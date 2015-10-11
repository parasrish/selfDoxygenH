# selfDoxygenH
This is a python script that generates a file, with doxygen headers added for the methods declarations. This serves as a tool for minimising the documentation effort.

The generated doxygen headers can then be filled with the desired comments.

******
USAGE:
******
Usage : genDoxygenC.py <cpp/h source file>

Example - If "genDoxygenC.py sample_source.h", then sample_source.h.doxygen will be created. When taken diff of the two files, you can well visualize the added headers of doxygen, with placeholders for adding comments.

[test folder] : This contains some of the sample files, used for validating the parsing concept. Both header and cpp source samples. The script "addDoxygen4.py" was used for debugging the main script code snippets.

In the main script, currently "RE_M_DECLERATION" is enabled, which parses and adds doxygen headers to the method declarations. However, there is another macro, "RE_M_DEFINITION" which will parse and add doxygen-headers to the method definitions.

*****
NOTE:
*****
The script developed using the regular expression, is just a proof of concept. There could be syntatic-cases, which are not handled and therefore can be skipped. Also, can cause regular expression based method extraction and processing, to have run-time errors. The Error handling needs to be improvised, to make stable and deterministic exits.
