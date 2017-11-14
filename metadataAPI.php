<?php
$filename = "FFMetadata20171101_commasRemoved.csv";

ini_set('memory_limit', '1024M');

$categories = array(new_name, varlab, old_name, type, warning, group, q_group_N, topic1,	topic2,	source,	respondent, wave,	scope,	section,	leaf,	q_group_list,	value1,	label1,	value2,	label2,	value3,	label3,	value4,	label4,	value5,	label5,	value6,	label6,	value7,	label7,	value8,	label8,	value9,	label9,	value10,	label10,	value11,	label11,	value12,	label12,	value13,	label13,	value14,	label14,	value15,	label15,	value16,	label16,	value17,	label17,	value18,	label18,	value19,	label19,	value20,	label20,	value21,	label21,	value22,	label22,	value23,	label23,	value24,	label24,	value25,	label25,	value26,	label26,	value27,	label27,	value28, label28,	value29,	label29,	value30,	label30,	value31,	label31,	value32,	label32,	value33, label33,	value34,	label34,	value35,	label35,	value36,	label36,	value37,	label37,	value38,	label38,	value39,	label39,	value40,	label40,	value41,	label41,	value42,	label42,	value43,	label43,	value44,	label44,	value45,	label45,	value46,	label46,	value47,	label47,	value48,	label48,	value49,	label49,	value50,	label50,	value51,	label51,	value52,	label52,	value53,	label53,	value54,	label54,	value55,	label55,	value56,	label56,	value57,	label57,	value58,	label58,	value59,	label59,	value60,	label60,	value61,	label61,	value62,	label62,	value63,	label63,	value64,	label64,	value65,	label65,	value66,	label66,	value67,	label67,	value68,	label68);

//metadata is an array where each index is a line in the CSV
class metadataFile
{
	private $metadataArray;
	// private $filename;
	function __construct($filename)
	{
		global $filename, $categories, $metadataArray;
		try 
		{
			if ($metadata = file($filename, FILE_IGNORE_NEW_LINES))
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
	// public function getMetadata()
	// {
	// 	global $metadataArray;
	// 	// var_dump($metadataArray);
	// 	return json_encode($metadataArray, JSON_FORCE_OBJECT);
	// }

	public function getVariable($varName)
	{
		global $metadataArray;
		$variable = $metadataArray[$varName];
		return json_encode($variable);
	}

	public function selectMetadata($varName, $fieldName)
	{
		global $metadataArray;
		$varField = $metadataArray[$varName][$fieldName];
		return json_encode($varField);
	}

	public function filterMetadata($filter_json)
	{
		global $metadataArray;
		$filtersArr = json_decode($filter_json, true);
		$filteredList = array();
		$firstFilterCounter = 0;


		foreach ($filtersArr as $filter => $value) {
			foreach ($metadataArray as $variable) {
				if ($variable[$filter] == $value)
				{
					$filteredList[$variable["new_name"]] = $variable;
					// array_push($filteredList, $variable);
				}
			}
			unset($filtersArr[$filter]);
			break;
		}
		foreach ($filtersArr as $filter => $value) {
			foreach ($filteredList as $variable) {
				if ($variable[$filter] != $value) 
					{
						unset($filteredList[$variable["new_name"]]);
					}
			}
		}
		// var_dump($filteredList);
		return json_encode($filteredList);
	}

	public function searchMetadata($query, $fieldName, $searchBody = null)
	{
		global $metadataArray;
		if (is_null($searchBody))
		{
			$searchBody = $metadataArray;
		}
		$searchResult = array();
		foreach ($searchBody as $variable)
		{
			if (strpos($variable[$fieldName], $query) != false)
			{
				$searchResult[$variable["new_name"]] = $variable;
			}
		}
		return json_encode($searchResult);
	}

	// public function getOldName($newName)
	// {
	// 	global $metadataArray;
	// 	// $oldNme = $metadataArray[$newName][old_name];
	// 	// $jsonArr = json_encode($oldName);
	// 	// echo $jsonArr;
	// 	return $metadataArray[$newName][old_name];
	// }

	// public function getNewName($oldName)
	// {
	// 	global $metadataArray;
	// 	foreach ($metadataArray as $arr)
	// 	{
	// 		if ($arr[old_name] == $oldName) return $arr[new_name];
	// 	}
	// 	return -1;
	// }
}

$metadataFile = new metadataFile($filename);
// var_dump($argv);
// print_r("one1111");
if (isset($_GET['function']))
{
	$fname = $_GET['function'];
	if ($fname == "getVariable")
	{
		$varName = $_GET['params'];
		fwrite(STDOUT, $metadataFile->getVariable($varName));
	}
	elseif($fname == "selectMetadata")
	{
		$params = explode(',', $_GET['params']);
		fwrite(STDOUT, $metadataFile->selectMetadata($params[0], $params[1]));
	}

	//unfinished: figure out json format issue. get size of get array, parse params into array
	//to become json
	elseif($fname == "filterMetadata")
	{
		$params = explode(',', $_GET['params']);
		$size = count($params);
		$arrayToJson = array();
		foreach ($i = 0; $i < $size; $i++) 
		{
			//will create an issue when there is a colon in the field
			$pairs = explode(":", $params[$i]);
			$arrayToJson[$pairs[0]] = $pairs[1];
		}
		fwrite(STDOUT, $metadataFile->filterMetadata(json_encode($arrayToJson)));
	}
	elseif($fname == "searchMetadata")
	{
		$params = explode(',', $_GET['params']);
		if ($params[2] != null)
		{
			fwrite(STDOUT, $metadataFile->searchMetadata($params[0], $params[1], $params[2]));
		}
		else 
		{
			fwrite(STDOUT, $metadataFile->searchMetadata($params[0], $params[1]));
		}
	}
	else fwrite(STDOUT, null);
}

// if ($argv[1] == "getVariable")
// {
// 	if($argv[2] != null)
// 	{
// 		print_r("x");
// 		fwrite(STDOUT, $metadataFile->getVariable($argv[2]));
// 	}
// 	else
// 	{
// 		fwrite(STDOUT, null);
// 	}
// }

// private function testGetMetadata()
// {

// }
// private function testGetVariable()
// {

// }
// private function testSelectMetadata()
// {

// }
// private function testFilterMetadata()
// {

// }
// private function testSearchMetadata()
// {

// }


// global $metadataArray;
// $metadataFile = new metadataFile($filename);
// $metadataFile->getMetadata();
// print_r($metadataFile->getVariable(cf1ethrace));
// print_r($metadataFile->selectMetadata(cf1ethrace, "type"));
// print_r("\n");
// print_r($metadataFile->selectMetadata(cf2id, "old_name"));
// // print_r("\n");

// $testFilters = array("group" => "1966", "varlab" => "Father race (all waves combined report)");
// $jsonFilter =  json_encode($testFilters);
// print_r($metadataFile->filterMetadata($jsonFilter));

// $filtered = $metadataFile->filterMetadata($jsonFilter)
// echo count(filtered[]);
// $metadataFile->getOldName(f4e12);
// $metadataFile->getVariable(f4e12);

/* returns private error 
print_r($metadataFile->metadataArray);*/

// function 

?>