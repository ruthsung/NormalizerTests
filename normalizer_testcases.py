# Ruth Sung 
# Test Cases for normalizer.py using pytest


# I ran out of time to write test cases for input and output data functions 
# input_data(input_file)
# output_data(data, output_file)

# My strategy for testing the input & output functions would be to 
# 1) test them after the data normalizing functions are working since it manipulates the data
# 2) create several input files to test with to cover cases including
# - edge cases: empty file, large/max file size  
# - graceful failure: corrupted csv files, wronge file type, wrong / missing columns of data  
# - happy path: average file 
# - handle unexpected input: contents that are not utf-8 compatible 
 
# The requirement for the TotalDuration column is not verified  
#   - The TotalDuration column is filled with garbage data. For each row, 
#   please replace the value of TotalDuration with the sum of FooDuration 
#   and BarDuration.


import pytest 
import normalizer

#   - The Timestamp column should be formatted in RFC3339 format.
#   - The Timestamp column should be assumed to be in US/Pacific time; 
#   please convert it to US/Eastern.  You can assume that the input document 
#   is in UTF-8 and that any times that are missing timezone information are 
#   in US/Pacific.
@pytest.mark.parametrize("datestamp, expectedDatestamp", 
	[("2019-10-12T07:20:50.524-07:00","2019-10-12T10:20:50.524000-04:00"), #RFC3339 input, happy path
	("4/1/11 11:00:00 AM","2011-04-01T14:00:00-04:00"), #input not in RFC3339 format
	("3:00pm MST June 7, 20", "2020-06-07T18:00:00-04:00"), #input not in RFC3339 format
	("May 1st", "2020-05-01T03:00:00-04:00"), #partial input
	("7:27 am Jan 5", "2020-01-05T10:27:00-05:00"), #partial input,
	("1985-04-12T20:20:50.52","1985-04-12T23:20:50.520000-05:00"), #RFC3339 input, no timezone info
	("14-01-12T12:44:37.980-15:00","2012-01-14T15:44:37.980000-05:00"), #RFC3339 input, wrong timezone info read as PT
	("",""), #empty input
	("7/7/03, ???", "") #handling an error, unclear expected output?
	])

def test_convert_timestamp(datestamp, expectedDatestamp):
	assert normalizer.convert_timestamp(datestamp) == expectedDatestamp


#   - All ZIP codes should be formatted as 5 digits. If there are less than 
#   5 digits, assume 0 as the prefix.
@pytest.mark.parametrize("zip, expectedZip",
 	[("","00000"),
    ("0","00000"),
    ("21", "00021"),
    ("384", "00384"),
    ("9057", "09057"),
    ("56708", "56708"),
    ("94040-1877", "94040"), #over 5 digits 
    ("nonsense", "") #nonsense input handling
	])

def test_verify_zipcode(zip, expectedZip):
	assert normalizer.verify_zipcode(zip) == expectedZip


#   - The FullName column should be converted to uppercase. There will be 
#   non-English names.
@pytest.mark.parametrize("name, expectedName",
 	[("",""),
    ("a","A"),
    ("Jane Doe", "JANE DOE"),
    ("First-Mid-Last Jr.", "FIRST-MID-LAST JR."),
    ("áçëæ123!!", "ÁÇËÆ123!!"),
    ("f  m  l  sr.", "F  M  L  SR."),
    ("superlong, namewithmany, letters", "SUPERLONG, NAMEWITHMANY, LETTERS")
	])

def test_parse_name(name, expectedName):
	assert normalizer.parse_name(name) == expectedName


#   - The Address column should be passed through as is, except for Unicode 
#   validation. Please note there are commas in the Address field; your CSV 
#   parsing will need to take that into account. Commas will only be present 
#   inside a quoted string.
@pytest.mark.parametrize("address, expectedAddress",
 	[("123 test ave, city, state 00000","123 test ave, city, state 00000"),
 	("",""),
 	("garbage content","garbage content"),
 	("áçëæ123","áçëæ123")
	])

def test_parse_address(address, expectedAddress):
	assert normalizer.parse_address(address) == expectedAddress


#   - The FooDuration and BarDuration columns are in HH:MM:SS.MS format (where 
#   	MS is milliseconds); please convert them to the total number of seconds 
#   expressed in floating point format. You should not round the result.
@pytest.mark.parametrize("duration, expectedDuration",
 	[("12:34:56.78",45296.78),
 	("00:00:00.01", 0.01),
 	("00:00:00.00", 0.00), #minimum
 	("23:59:59.99", 86399.99), #maximum
 	("24:60:60.15", 0.00), #out of range  
 	("23:12", 0.00), #invalide format
 	("15:23:33", 0.00), #invalide format
 	("47.23", 0.00), #invalide format
 	("garbage", 0.00), # invalid input 
 	("", 0.00) # no input 
	])

def test_parse_duration(duration, expectedDuration):
	assert normalizer.parse_duration(duration) == expectedDuration


#   - The Notes column is free form text input by end-users; please do not 
#   perform any transformations on this column. If there are invalid UTF-8 
#   characters, please replace them with the Unicode Replacement Character.
@pytest.mark.parametrize("notes, expectedNotes",
 	[(None, None),
 	("",""),
 	("garbage","garbage"),
 	("áçëæ123","áçëæ123"),
 	("long NOTE - string with more conent!!!??", "long NOTE - string with more conent!!!??")
	])

def test_parse_notes(notes, expectedNotes):
	assert normalizer.parse_notes(notes) == expectedNotes

