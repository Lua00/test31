<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
if (!$user) {
  header('Location: /login.php');
  exit;
}

activateMembership($user['id']);
header('Location: /dashboard.php');