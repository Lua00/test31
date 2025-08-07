<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
$downloads = getAllDownloads();
$isMember = $user && $user['is_member'];
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>İndirilebilirler</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<header class="container">
  <h1>İndirilebilirler</h1>
  <nav>
    <a href="/index.php">Ana Sayfa</a>
    <a href="/blog.php">Blog</a>
    <a href="/store.php">Üyelik Satın Al</a>
    <?php if ($user): ?>
      <a href="/dashboard.php">Panel</a>
      <form class="inline" method="post" action="/logout.php">
        <button type="submit">Çıkış</button>
      </form>
    <?php else: ?>
      <a href="/login.php">Giriş</a>
      <a href="/register.php">Kayıt Ol</a>
    <?php endif; ?>
  </nav>
</header>
<main class="container">
  <?php if (!$isMember): ?>
    <section class="card pad">
      <p>Bu alan yalnızca aktif üyeler içindir. Lütfen üyelik satın alın.</p>
      <p><a class="button" href="/store.php">Üyelik Satın Al</a></p>
    </section>
  <?php else: ?>
    <?php if ($user && isAdmin($user)): ?>
      <p><a class="button" href="/download_upload.php">Yeni Dosya Yükle (Admin)</a></p>
    <?php endif; ?>
    <div class="grid">
      <?php foreach ($downloads as $dl): ?>
        <article class="card pad">
          <h3><?php echo htmlspecialchars($dl['title']); ?></h3>
          <?php if (!empty($dl['description'])): ?>
            <p class="mb"><?php echo nl2br(htmlspecialchars($dl['description'])); ?></p>
          <?php endif; ?>
          <p class="muted">Boyut: <?php echo number_format((int)$dl['file_size'] / 1024, 1); ?> KB</p>
          <p><a class="button" href="/download.php?id=<?php echo (int)$dl['id']; ?>">İndir</a></p>
        </article>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>
</main>
</body>
</html>