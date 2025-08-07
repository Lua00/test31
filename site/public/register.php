<?php
session_start();
require_once __DIR__ . '/../includes/db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $username = trim($_POST['username'] ?? '');
  $password = $_POST['password'] ?? '';
  $password2 = $_POST['password2'] ?? '';
  if ($password !== $password2) {
    $error = 'Şifreler eşleşmiyor';
  } elseif (strlen($username) < 3 || strlen($password) < 6) {
    $error = 'Kullanıcı adı en az 3, şifre en az 6 karakter olmalı';
  } elseif (findUserByUsername($username)) {
    $error = 'Bu kullanıcı adı zaten alınmış';
  } else {
    $hash = password_hash($password, PASSWORD_DEFAULT);
    $userId = createUser($username, $hash);
    $_SESSION['user_id'] = $userId;
    header('Location: /dashboard.php');
    exit;
  }
}
?>
<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Kayıt Ol</title>
  <link rel="stylesheet" href="/css/styles.css" />
</head>
<body>
<main class="container narrow">
  <h1>Kayıt Ol</h1>
  <?php if (!empty($error)): ?><p class="error"><?php echo htmlspecialchars($error); ?></p><?php endif; ?>
  <form method="post">
    <label>Kullanıcı Adı
      <input required type="text" name="username" />
    </label>
    <label>Şifre
      <input required type="password" name="password" />
    </label>
    <label>Şifre (Tekrar)
      <input required type="password" name="password2" />
    </label>
    <button type="submit">Kayıt Ol</button>
  </form>
  <p>Hesabın var mı? <a href="/login.php">Giriş yap</a></p>
</main>
</body>
</html>