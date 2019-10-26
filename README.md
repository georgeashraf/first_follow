# First&Follow sets
Computes the first & follow sets for all variables for a given grammar.

#### Format of input file:
* non terminal colon production rules.
* all variables are space separated.
* Example: 
A : A c | A a d | b d 
#### Format of output file:
*  non terminal colon first colon follow.
*   all variables are space separated.
* Example:
A : a b c : a b $ 
##### How to run:-

   from command line:
   python "script_name" --file "text_file_name"

   Example:
   python First_and_Follow.py  --file Test7.txt