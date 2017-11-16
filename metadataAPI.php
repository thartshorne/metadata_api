<?php
$filename = "FFMetadata20171101_commasRemoved.csv";

ini_set('memory_limit', '1024M');

$categories = array(new_name, varlab, old_name, type, warning, group, q_group_N, topic1,	topic2,	source,	respondent, wave,	scope,	section,	leaf,	q_group_list,	value1,	label1,	value2,	label2,	value3,	label3,	value4,	label4,	value5,	label5,	value6,	label6,	value7,	label7,	value8,	label8,	value9,	label9,	value10,	label10,	value11,	label11,	value12,	label12,	value13,	label13,	value14,	label14,	value15,	label15,	value16,	label16,	value17,	label17,	value18,	label18,	value19,	label19,	value20,	label20,	value21,	label21,	value22,	label22,	value23,	label23,	value24,	label24,	value25,	label25,	value26,	label26,	value27,	label27,	value28, label28,	value29,	label29,	value30,	label30,	value31,	label31,	value32,	label32,	value33, label33,	value34,	label34,	value35,	label35,	value36,	label36,	value37,	label37,	value38,	label38,	value39,	label39,	value40,	label40,	value41,	label41,	value42,	label42,	value43,	label43,	value44,	label44,	value45,	label45,	value46,	label46,	value47,	label47,	value48,	label48,	value49,	label49,	value50,	label50,	value51,	label51,	value52,	label52,	value53,	label53,	value54,	label54,	value55,	label55,	value56,	label56,	value57,	label57,	value58,	label58,	value59,	label59,	value60,	label60,	value61,	label61,	value62,	label62,	value63,	label63,	value64,	label64,	value65,	label65,	value66,	label66,	value67,	label67,	value68,	label68);

//metadata is an array where each index is a line in the CSV
class metadataFile
{
	private $metadataArray;
	function __construct()
	{
		global $filename, $categories, $metadataArray;
		try 
		{
			if ($metadata = file($filename, FILE_IGNORE_NEW_LINES))
			{
				unset($metadata[0]);
				$vars = array();
				$lenMetadata = sizeof($metadata);
				for ($i = 1; $i <= $lenMetadata; $i++)
				{
					$varArrInt = explode(',', $metadata[$i]);
					$lenVA = sizeof($varArrInt);
					$varArrCat = array();
					for ($j = 0; $j < $lenVA; $j++)
					{
						if (strpos($varArrInt[$j], '&&') != false)
						{
							$varArrInt[$j] = str_replace('&&', ',', $varArrInt[$j]);
						}
						$varArrCat[$categories[$j]] = $varArrInt[$j];
					}
					/*metadataArray is an array indexed by unique new variable names
					where each entry is an array for each column in the csv indexed
					by column name (category)*/
					$metadataArray[$varArrCat[new_name]] = $varArrCat;
				}
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

	public function selectMetadata($varName, $fieldName)
	{
		global $metadataArray;
		if ($fieldName == null)
		{
			$fullVar = $metadataArray[$varName];
			if ($fullVar == null)
			{
				return "[]";
			}
			return json_encode($fullVar);
		}
		$varField = $metadataArray[$varName][$fieldName];
		if ($varField != null)
		{
			return json_encode($varField);
		}
		else return "[]";
	}

	public function filterMetadata($filtersArr)
	{
		global $metadataArray;
		$filteredList = array();

		if ($filtersArr == null)
		{
			foreach ($metadataArray as $variable) 
			{
				$filteredList[$variable["new_name"]] = $variable;
				print_r(json_encode($variable));
			}
		}
		else
		{
			$filtersArr = json_decode($filtersArr, true);
			foreach ($filtersArr as $filter => $value) 
			{
				foreach ($metadataArray as $variable) 
				{
					if ($variable[$filter] == $value)
					{
						$filteredList[$variable["new_name"]] = $variable;
					}
				}
				unset($filtersArr[$filter]);
				break;
			}
			foreach ($filtersArr as $filter => $value) 
			{
				foreach ($filteredList as $variable) 
				{
					if ($variable[$filter] != $value) 
					{
						unset($filteredList[$variable["new_name"]]);
					}
				}
			}
		}
		foreach ($filteredList as $variable) {
			print_r(json_encode($variable));
		}
		if (empty($filteredList))
		{
			return "[]";
		}
		else
		{
			return;
		}
	}

	public function searchMetadata($query, $fieldName, $searchBody = null)
	{
		global $metadataArray;
		if (is_null($searchBody))
		{
			$searchBody = $metadataArray;
		}
		else
		{
			print_r($searchBody);
			$newSearch = array();
			$searchFile = file_get_contents($searchBody);
			if ($searchFile == false)
			{
				return 0;
			}
			$linesFile = str_replace("}", "}\n", $searchFile);
			foreach(preg_split("/((\r?\n)|(\r\n?))/", $linesFile) as $line)
			{
				$element = json_decode($line, true);
				$newSearch[$element["new_name"]] = $element;
			}
			$searchBody = $newSearch;
		}
		$searchResult = array();
		foreach ($searchBody as $variable)
		{
			if ($query == null)
			{
				$allResults = $searchResult[$variable["new_name"]] = $variable;
				print_r(json_encode($variable));
			}
			elseif (strpos($variable[$fieldName], $query) !== false)
			{
				$searchResult[$variable["new_name"]] = $variable;
				print_r(json_encode($variable));
			}
		}
		if (empty($searchResult))
		{
			return "[]";
		}
		else 
		{
			return;
		}
	}

}

// $metadataFile = new metadataFile($filename);
// global $metadataArray;

// print_r($metadataFile->selectMetadata(cf2id, "old_name"));
// print_r("\n\n");

// $testFilters = array("group" => "1966", "varlab" => "Father race (all waves combined report)");
// $jsonFilter =  json_encode($testFilters);
// print_r($metadataFile->filterMetadata($jsonFilter));
// print_r("\n\n");

// print_r($metadataFile->searchMetadata("policing", "topic1"));

/* returns private error 
print_r($metadataFile->metadataArray);*/

?>