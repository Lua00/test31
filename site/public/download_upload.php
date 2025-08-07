<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
if (!$user || !isAdmin($user)) {
  http_response_code(403);
  echo 'Yetki yok';
  exit;
}

$error = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $title = trim($_POST['title'] ?? '');
  $description = trim($_POST['description'] ?? '');
  if ($title === '') {
    $error = 'Başlık gerekli';
  } elseif (empty($_FILES['file']['name'])) {
    $error = 'Dosya seçiniz';
  } else {
    $original = $_FILES['file']['name'];
    $size = (int)$_FILES['file']['size'];
    if ($size <= 0) {
      $error = 'Boş dosya';
    } else {
      $allowedExt = ['zip','tar','gz','bz2','xz','whl','py','txt','pdf','7z'];
      $ext = strtolower(pathinfo($original, PATHINFO_EXTENSION));
      if (!in_array($ext, $allowedExt, true)) {
        $error = 'Bu dosya türüne izin verilmiyor';
      } else {
        $mime = mime_content_type($_FILES['file']['tmp_name']) ?: 'application/octet-stream';
        $stored = bin2hex(random_bytes(12)) . '.' . $ext;
        $targetDir = __DIR__ . '/../protected/downloads';
        if (!is_dir($targetDir)) {
          mkdir($targetDir, 0775, true);
        }
        $target = $targetDir . '/' . $stored;
        if (!move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
          $error = 'Yükleme başarısız';
        } else {
          $id = createDownload($title, $description, $stored, $original, $mime, filesize($target));
          header('Location: /downloads.php');
          exit;
        }
      }
    }
  }
}
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dosya Yükle (Admin)</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<main class="container narrow">
  <h1>Dosya Yükle</h1>
  <?php if ($error): ?><p class="error"><?php echo htmlspecialchars($error); ?></p><?php endif; ?>
  <form method="post" enctype="multipart/form-data">
    <label>Başlık
      <input required type="text" name="title" />
    </label>
    <label>Açıklama
      <textarea name="description" rows="4"></textarea>
    </label>
    <label>Dosya
      <input required type="file" name="file" />
    </label>
    <button type="submit">Yükle</button>
  </form>
  <p><a href="/downloads.php">Geri dön</a></p>
</main>
</body>
</html>