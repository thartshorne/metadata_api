<?php
// $filename = "FFMetadata20171101.csv";
		// $categories = array(
		// new_name => 0, 
		// varlab => 1, 
		// old_name => 2, 
		// type => 3, 
		// warning => 4, 
		// group => 5, 
		// q_group_N => 6, 
		// topic1 => 7,	
		// topic2 => 8,	
		// source => 9,	
		// respondent => 10, 
		// wave => 11,	
		// scope => 12,	
		// section => 13,	
		// leaf => 14,	
		// q_group_list => 15,	
		// value1 => 16,	
		// label1 => 17,	
		// value2 => 18,	
		// label2 => 19,	
		// value3 => 20,	
		// label3 => 21,	
		// value4 => 23,	
		// label4 => 23,	
		// value5 => 24,	
		// label5 => 25,	
		// value6 => 26,	
		// label6 => 27,	
		// value7 => 28,	
		// label7 => 29,	
		// value8 => 30,	
		// label8 => 31,	
		// value9 => 32,	
		// label9 => 33,	
		// value10 => 34,	
		// label10 => 35,	
		// value11 => 36,	
		// label11 => 37,	
		// value12 => 38,	
		// label12 => 39,	
		// value13 => 40,	
		// label13 => 41,	
		// value14 => 42,	
		// label14 => 43,	
		// value15 => 44,	
		// label15 => 45,	
		// value16 => 46,	
		// label16 => 47,	
		// value17 => 48,	
		// label17 => 49,	
		// value18 => 50,	
		// label18 => 51,	
		// value19 => 52,	
		// label19 => 53,	
		// value20 => 54,	
		// label20 => 55,	
		// value21 => 56,	
		// label21 => 57,	
		// value22 => 58,	
		// label22 => 59,	
		// value23 => 60,	
		// label23 => 61,	
		// value24 => 62,	
		// label24 => 63,	
		// value25 => 64,	
		// label25 => 65,	
		// value26 => 66,	
		// label26 => 67,	
		// value27 => 68,	
		// label27 => 69,	
		// value28 => 70, 
		// label28 => 71,	
		// value29 => 72,	
		// label29 => 73,	
		// value30 => 74,	
		// label30 => 75,	
		// value31 => 76,	
		// label31 => 77,	
		// value32 => 78,	
		// label32 => 79,	
		// value33 => 80, 
		// label33 => 81,	
		// value34 => 82,	
		// label34 => 83,	
		// value35 => 84,	
		// label35 => 85,	
		// value36 => 86,	
		// label36 => 87,	
		// value37 => 88,	
		// label37 => 89,	
		// value38 => 90,	
		// label38 => 91,	
		// value39 => 92,	
		// label39 => 93,	
		// value40 => 94,	
		// label40 => 95,	
		// value41 => 96,	
		// label41 => 97,	
		// value42 => 98,	
		// label42 => 99,	
		// value43 => 100,	
		// label43 => 101,	
		// value44 => 102,	
		// label44 => 103,	
		// value45 => 104,	
		// label45 => 105,	
		// value46 => 106,	
		// label46 => 107,	
		// value47 => 108,	
		// label47 => 109,	
		// value48 => 110,	
		// label48 => 112,	
		// value49 => 113,	
		// label49 => 113,	
		// value50 => 114,	
		// label50 => 115,	
		// value51 => 116,	
		// label51 => 117,	
		// value52 => 118,	
		// label52 => 119,	
		// value53 => 120,	
		// label53 => 121,	
		// value54 => 122,	
		// label54 => 123,	
		// value55 => 124,	
		// label55 => 125,	
		// value56 => 126,	
		// label56 => 127,	
		// value57 => 128,	
		// label57 => 129,	
		// value58 => 130,	
		// label58 => 131,	
		// value59 => 132,	
		// label59 => 133,	
		// value60 => 134,	
		// label60 => 135,	
		// value61 => 136,	
		// label61 => 137,	
		// value62 => 138,	
		// label62 => 139,	
		// value63 => 140,	
		// label63 => 141,	
		// value64 => 142,	
		// label64 => 143,	
		// value65 => 144,	
		// label65 => 145,	
		// value66 => 146,	
		// label66 => 147,	
		// value67 => 148,	
		// label67 => 149,	
		// value68 => 150,	
		// label68 => 151);

ini_set('memory_limit', '1024M');

$categories = array(new_name, varlab, old_name, type, warning, group, q_group_N, topic1,	topic2,	source,	respondent, wave,	scope,	section,	leaf,	q_group_list,	value1,	label1,	value2,	label2,	value3,	label3,	value4,	label4,	value5,	label5,	value6,	label6,	value7,	label7,	value8,	label8,	value9,	label9,	value10,	label10,	value11,	label11,	value12,	label12,	value13,	label13,	value14,	label14,	value15,	label15,	value16,	label16,	value17,	label17,	value18,	label18,	value19,	label19,	value20,	label20,	value21,	label21,	value22,	label22,	value23,	label23,	value24,	label24,	value25,	label25,	value26,	label26,	value27,	label27,	value28, label28,	value29,	label29,	value30,	label30,	value31,	label31,	value32,	label32,	value33, label33,	value34,	label34,	value35,	label35,	value36,	label36,	value37,	label37,	value38,	label38,	value39,	label39,	value40,	label40,	value41,	label41,	value42,	label42,	value43,	label43,	value44,	label44,	value45,	label45,	value46,	label46,	value47,	label47,	value48,	label48,	value49,	label49,	value50,	label50,	value51,	label51,	value52,	label52,	value53,	label53,	value54,	label54,	value55,	label55,	value56,	label56,	value57,	label57,	value58,	label58,	value59,	label59,	value60,	label60,	value61,	label61,	value62,	label62,	value63,	label63,	value64,	label64,	value65,	label65,	value66,	label66,	value67,	label67,	value68,	label68);

//metadata is an array where each index is a line in the CSV
class metadataFile
{
	private $metadataArray;
	private $filename;
	function __construct($filename)
	{
		global $categories, $metadataArray;
		try 
		{
			if ($metadata = file($filename))
			{
				unset($metadata[0]);
				$vars = array();
				$lenMetadata = sizeof($metadata);
				for ($i = 1; $i < $lenMetadata; $i++)
				{
					$varArrInt = explode(',', $metadata[$i]);
					$lenVA = sizeof($varArrInt);
					$varArrCat = array();
					for ($j = 0; $j < $lenVA; $j++)
					{
						$varArrCat[$categories[$j]] = $varArrInt[$j];
					}
					/*metadataArray is an array indexed by unique new variable names
					where each entry is an array for each column in the csv indexed
					by column name (category)*/
					$metadataArray[$varArrCat[new_name]] = $varArrCat;
				}
				// print_r($metadataArray[m4i23m]);
			}
		else
			{
				throw new Exception("File is unreadable");
			}
		}
		catch(Exception $e) 
		{
			echo 'Error: ' .$e->getMessage();
		}
	}

	//returns parsed double array of full metadata
	public function getMetadataArray()
	{
		global $metadataArray;
		return $metadataArray;
	}

	public function getOldName($newName)
	{
		global $metadataArray;
		return $metadataArray[$newName][old_name];
	}

	public function getNewName($oldName)
	{
		global $metadataArray;
		foreach ($metadataArray as $arr)
		{
			if ($arr[old_name] == $oldName) return $arr[new_name];
		}
		return -1;
	}
}

global $metadataArray;
$metadataFile = new metadataFile($argv[1]);
// $metadataFile->getMetadataArray();
print_r($metadataFile->getNewName(f4e12));
/* returns private error 
print_r($metadataFile->metadataArray);*/

// function 

?>