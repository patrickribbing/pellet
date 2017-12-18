<!DOCTYPE html>
<html>
<head>
<title>Pellets</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Pellets measurer</h1>
<p>Current value: 
<?php
echo file_get_contents("./distance.html");
?> cm
</p>
</body>
</html>
