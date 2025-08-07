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
  <title>Üyelik Satın Al</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<header class="container">
  <h1>Üyelik</h1>
  <nav>
    <a href="/index.php">Ana Sayfa</a>
    <a href="/blog.php">Blog</a>
    <a href="/downloads.php">İndirilebilirler</a>
    <?php if ($user): ?>
             <a href="/dashboard.php">Panel</a>
    <?php else: ?>
             <a href="/login.php">Giriş</a>
    <?php endif; ?>
  </nav>
</header>
<main class="container">
  <section class="card pad">
    <h2>Üyelik Planı</h2>
    <ul>
      <li>Özel Python proje dosyaları</li>
      <li>Üyelere özel yazılar</li>
      <li>Güncellemeler</li>
    </ul>
    <?php if (!$user): ?>
      <p>Lütfen <a href="/login.php">giriş yap</a> ya da <a href="/register.php">kayıt ol</a>.</p>
    <?php elseif ($user['is_member']): ?>
      <p>Zaten aktifsin.</p>
    <?php else: ?>
      <form method="post" action="/purchase.php">
        <button type="submit">Satın Al (Mock)</button>
      </form>
    <?php endif; ?>
  </section>
</main>
</body>
</html>