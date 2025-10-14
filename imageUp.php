<?php 
    include("imageFunc.php");
    
    header('Location: main.html');
    $Filepath = "Images/";
    $IName = $_FILES['inImage']['name'];
    $ITName = $_FILES['inImage']['tmp_name'];
    $inputNum = 1;

    $fileArr = Flist();
    $arrSize = Fcount();

    //changes the filename from what was uploaded to DeathStar$.<extension>
    $inputNewName = Frename($IName, $fileArr, $arrSize);


    //moves the file over to the image folder under the new name
    $imageUpload = move_uploaded_file($ITName, $Filepath.$inputNewName);

?>