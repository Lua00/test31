<?php
require_once __DIR__ . '/../includes/db.php';
initSchema();
echo "DB initialized at " . realpath(__DIR__ . '/../data/app.sqlite') . PHP_EOL;