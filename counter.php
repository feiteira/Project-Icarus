<?php
$counter_file = '/var/www/exapix/counter.txt';
$visits = @file_get_contents($counter_file);
if ($visits === false) $visits = 0;
$visits++;
file_put_contents($counter_file, $visits);
echo $visits;
?>