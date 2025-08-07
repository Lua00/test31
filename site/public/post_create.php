<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
if (!$user) {
  header('Location: /login.php');
  exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
  header('Location: /site/public/blog.php');
  exit;
}

$title = trim($_POST['title'] ?? '');
$content = trim($_POST['content'] ?? '');
$imagePath = null;

if (!empty($_FILES['image']['name'])) {
  $allowed = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'];
  $type = mime_content_type($_FILES['image']['tmp_name']);
  if (!isset($allowed[$type])) {
    $_SESSION['flash_error'] = 'Görsel tipi desteklenmiyor';
    header('Location: /site/public/blog.php');
    exit;
  }
  $ext = $allowed[$type];
  $safeName = bin2hex(random_bytes(8)) . '.' . $ext;
  $target = __DIR__ . '/uploads/' . $safeName;
  if (!move_uploaded_file($_FILES['image']['tmp_name'], $target)) {
    $_SESSION['flash_error'] = 'Görsel yüklenemedi';
    header('Location: /blog.php');
    exit;
  }
  $imagePath = '/uploads/' . $safeName;
}

$postId = createPost($user['id'], $title, $content, $imagePath);
header('Location: /post.php?id=' . $postId);