<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
$posts = getRecentPosts(20);
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Blog</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<header class="container">
  <h1>Blog</h1>
  <nav>
    <a href="/index.php">Ana Sayfa</a>
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
  <?php if ($user): ?>
    <section class="card pad">
      <h2>Yeni Yazı</h2>
      <form method="post" action="/post_create.php" enctype="multipart/form-data">
        <label>Başlık
          <input required type="text" name="title" />
        </label>
        <label>İçerik
          <textarea required name="content" rows="6"></textarea>
        </label>
        <label>Kapak Görseli (isteğe bağlı)
          <input type="file" name="image" accept="image/*" />
        </label>
        <button type="submit">Yayınla</button>
      </form>
    </section>
  <?php endif; ?>

  <section>
    <h2>Yazılar</h2>
    <div class="grid">
      <?php foreach ($posts as $post): ?>
        <article class="card">
          <?php if ($post['image_path']): ?>
            <img src="<?php echo htmlspecialchars($post['image_path']); ?>" alt="Kapak" />
          <?php endif; ?>
          <h3><a href="/post.php?id=<?php echo (int)$post['id']; ?>"><?php echo htmlspecialchars($post['title']); ?></a></h3>
          <p class="muted"><?php echo date('d.m.Y H:i', strtotime($post['created_at'])); ?></p>
        </article>
      <?php endforeach; ?>
    </div>
  </section>
</main>
</body>
</html>