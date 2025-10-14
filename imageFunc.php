<?php
    //FCount is what counts the amount of images 
    function Fcount(){
        $Folder = "Images/";
        $FP = scandir($Folder);
        $FC = count($FP)-2;
        return $FC;
    }

    //Flist makes an array of the filenames
    function Flist(){
        $Folder = "Images/";
        $FP = scandir($Folder);
        $FA = array_diff($FP,[".",".."]);
        $FA = array_values($FA);
        return $FA;

    }
    //renames the file
    function Frename($IName, $fileArr, $arrSize){
        $inputNum = 1;
        $extension=pathinfo($IName, PATHINFO_EXTENSION);
        $INName = "DeathStar"  . $inputNum . "." . $extension;
        for($i=0;$i<$arrSize;$i=$i+1){
            $imgFile = $fileArr[$i];
            if($fileArr[$i]== $INName){
                $inputNum++;
                $INName = "DeathStar"  . $inputNum . "." . $extension;
            }
        }
        return $INName;
    }
?>