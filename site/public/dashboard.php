<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

$user = getAuthenticatedUser();
if (!$user) {
  header('Location: /login.php');
  exit;
}
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Panel</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<header class="container">
  <h1>Panel</h1>
  <nav>
    <a href="/index.php">Ana Sayfa</a>
    <a href="/blog.php">Blog</a>
    <a href="/downloads.php">İndirilebilirler</a>
    <form class="inline" method="post" action="/logout.php">
      <button type="submit">Çıkış</button>
    </form>
  </nav>
</header>
<main class="container">
  <section class="card pad">
    <h2>Merhaba, <?php echo htmlspecialchars($user['username']); ?></h2>
    <p>Üyelik Durumu: <strong><?php echo $user['is_member'] ? 'Aktif' : 'Yok'; ?></strong></p>
    <?php if (!$user['is_member']): ?>
      <p><a class="button" href="/store.php">Üyelik Satın Al</a></p>
    <?php endif; ?>
  </section>
</main>
</body>
</html>