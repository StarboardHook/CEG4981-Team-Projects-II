<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>    
    <style>
        <?php include "Style.css" ?>
    </style>
    <?php 
        include("imageFunc.php");
        
        $Folder = "Images/";

        echo "<pre>";
        $fullList = Flist();
        $fileCount = FCount();

        echo "</pre>";
        //for loop adds the images in a grid
        echo "<div class='imgContainer'>";
        for($i=0;$i<$fileCount;$i = $i+1){
            $image1 = $fullList[$i];
            echo"<div class='imageSection'>";   
            echo "<img src='Images/$image1'>";
            echo"</div>";
        }
        echo "</div>";

    ?>
</body>
</html>