<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = trim($_POST['username'] ?? '');
  $password = $_POST['password'] ?? '';
  $user = findUserByUsername($username);
  if ($user && password_verify($password, $user['password_hash'])) {
    $_SESSION['user_id'] = $user['id'];
         header('Location: /dashboard.php');
    exit;
  } else {
    $error = 'Geçersiz kullanıcı adı veya şifre';
  }
}
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Giriş</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<main class="container narrow">
  <h1>Giriş</h1>
  <?php if (!empty($error)): ?><p class="error"><?php echo htmlspecialchars($error); ?></p><?php endif; ?>
  <form method="post">
    <label>Kullanıcı Adı
      <input required type="text" name="username" />
    </label>
    <label>Şifre
      <input required type="password" name="password" />
    </label>
    <button type="submit">Giriş Yap</button>
  </form>
  <p>Hesabın yok mu? <a href="/register.php">Kayıt ol</a></p>
</main>
</body>
</html>