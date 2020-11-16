
//// Instructions to run the test cases:

  make sure normalizer.py can be run on the machine
  download & unzip normalizer_testcases.py in same folder as normalizer.py

  run the following: 

  pip install pytest
  pytest ./normalizer_testcases.py 

  OR for shorter error messages 

  pytest --tb=short ./normalizer_testcases.py


//// Identified issues with normalize.py: 

Overall
   - Requirement is not being addressed in the code:
	   - If a character is invalid, replace it with the Unicode Replacement 
	   Character. If that replacement makes data invalid (for example, because 
	   it turns a date field into something unparseable), print a warning to 
	   stderr and drop the row from your output.
	   - As part of line 49, when using open(), set errors = 'replace' to replace invalid chars 
	   - each function should be checking inputs for unparseable data field, print warning to stderr & drop row from output 
	   - If characters are replaced in the address or notes, is the input still left unchanged? 
	   - https://docs.python.org/3/library/functions.html#open 
	- what should each function expect as the input, what edge cases / exceptions should be handled?

convert_timestamp(datestamp)
	- does not handle parser errors, https://dateutil.readthedocs.io/en/stable/parser.html

verify_zipcode(zip)
	- fails to handle zip codes over 5 digits in length
	- does not handle non digit inputs like letters, symbols etc.  

parse_name(name)
	- N/A

test_parse_address(address)
	- if the address should be passed through as is, there is no need to check that the input is a string or to try and decode it

parse_duration(duration)
	- datetime objects have expected maximums for hour, minute, and second
	- does that match the expected input ranges? 
	- https://docs.python.org/3/library/datetime.html#datetime.datetime

parse_notes(notes)
	- function is not being used in normalizer.py
	- function does not return anything










