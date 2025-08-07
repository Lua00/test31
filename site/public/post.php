<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$post = getPostById($id);
if (!$post) {
  http_response_code(404);
  echo 'Yazı bulunamadı';
  exit;
}
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title><?php echo htmlspecialchars($post['title']); ?></title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<header class="container">
  <h1><a href="/blog.php"><?php echo htmlspecialchars($post['title']); ?></a></h1>
  <nav>
    <a href="/index.php">Ana Sayfa</a>
    <a href="/blog.php">Blog</a>
  </nav>
</header>
<main class="container">
  <article class="card pad">
    <?php if ($post['image_path']): ?>
      <img class="mb" src="<?php echo htmlspecialchars($post['image_path']); ?>" alt="Kapak" />
    <?php endif; ?>
    <p class="muted"><?php echo date('d.m.Y H:i', strtotime($post['created_at'])); ?></p>
    <div>
      <?php echo nl2br(htmlspecialchars($post['content'])); ?>
    </div>
  </article>
</main>
</body>
</html>