<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
if (!$user || !$user['is_member']) {
  http_response_code(403);
  echo 'Erişim engellendi';
  exit;
}

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$dl = getDownloadById($id);
if (!$dl) {
  http_response_code(404);
  echo 'Dosya bulunamadı';
  exit;
}

$protectedDir = realpath(__DIR__ . '/../protected/downloads');
$filePath = realpath($protectedDir . '/' . $dl['stored_filename']);
if (!$filePath || strpos($filePath, $protectedDir) !== 0 || !is_file($filePath)) {
  http_response_code(404);
  echo 'Dosya yok';
  exit;
}

$mime = $dl['mime_type'] ?: 'application/octet-stream';
$orig = $dl['original_filename'];
header('Content-Description: File Transfer');
header('Content-Type: ' . $mime);
header('Content-Disposition: attachment; filename="' . rawbasename($orig) . '"');
header('Content-Length: ' . filesize($filePath));
header('Cache-Control: no-store');
readfile($filePath);
exit;

function rawbasename($filename) {
  $basename = basename(str_replace(['\\'], '/', $filename));
  return $basename;
}