<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Ana Sayfa</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
  <header class="container">
    <h1>Python Projeleri</h1>
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
    <section>
      <h2>Hoş geldin<?php echo $user ? ' ' . htmlspecialchars($user['username']) : ''; ?>!</h2>
      <p>Python projelerim için üyelik satın alabilir, blog yazılarımı okuyabilir ve projelerimin görsellerine göz atabilirsin.</p>
    </section>

    <section>
      <h3>Son Blog Yazıları</h3>
      <div class="grid">
        <?php foreach (getRecentPosts(3) as $post): ?>
          <article class="card">
            <?php if ($post['image_path']): ?>
              <img src="<?php echo htmlspecialchars($post['image_path']); ?>" alt="Kapak" />
            <?php endif; ?>
                         <h4><a href="/post.php?id=<?php echo (int)$post['id']; ?>"><?php echo htmlspecialchars($post['title']); ?></a></h4>
            <p class="muted"><?php echo date('d.m.Y H:i', strtotime($post['created_at'])); ?></p>
          </article>
        <?php endforeach; ?>
      </div>
    </section>
  </main>

  <script src="/js/main.js"></script>
</body>
</html>