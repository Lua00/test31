<?php

function getDb(): PDO {
  static $pdo = null;
  if ($pdo) return $pdo;
  $dbPath = __DIR__ . '/../data/app.sqlite';
  $pdo = new PDO('sqlite:' . $dbPath);
  $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  return $pdo;
}

function initSchema(): void {
  $db = getDb();
  $db->exec('PRAGMA foreign_keys = ON');
  $db->exec('CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_member INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )');
  $db->exec('CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_path TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
  )');
  $db->exec('CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    stored_filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    mime_type TEXT,
    file_size INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )');
}

function getAuthenticatedUser(): ?array {
  if (empty($_SESSION['user_id'])) return null;
  $db = getDb();
  $stmt = $db->prepare('SELECT * FROM users WHERE id = :id');
  $stmt->execute([':id' => $_SESSION['user_id']]);
  $user = $stmt->fetch(PDO::FETCH_ASSOC);
  return $user ?: null;
}

function isAdmin(array $user): bool {
  return isset($user['id']) && (int)$user['id'] === 1;
}

function findUserByUsername(string $username): ?array {
  $db = getDb();
  $stmt = $db->prepare('SELECT * FROM users WHERE username = :u');
  $stmt->execute([':u' => $username]);
  $user = $stmt->fetch(PDO::FETCH_ASSOC);
  return $user ?: null;
}

function createUser(string $username, string $passwordHash): int {
  $db = getDb();
  $stmt = $db->prepare('INSERT INTO users (username, password_hash) VALUES (:u, :p)');
  $stmt->execute([':u' => $username, ':p' => $passwordHash]);
  return (int)$db->lastInsertId();
}

function activateMembership(int $userId): void {
  $db = getDb();
  $stmt = $db->prepare('UPDATE users SET is_member = 1 WHERE id = :id');
  $stmt->execute([':id' => $userId]);
}

function createPost(int $userId, string $title, string $content, ?string $imagePath): int {
  $db = getDb();
  $stmt = $db->prepare('INSERT INTO posts (user_id, title, content, image_path) VALUES (:uid, :t, :c, :img)');
  $stmt->execute([
    ':uid' => $userId,
    ':t' => $title,
    ':c' => $content,
    ':img' => $imagePath
  ]);
  return (int)$db->lastInsertId();
}

function getRecentPosts(int $limit = 10): array {
  $db = getDb();
  $stmt = $db->prepare('SELECT * FROM posts ORDER BY created_at DESC LIMIT :lim');
  $stmt->bindValue(':lim', $limit, PDO::PARAM_INT);
  $stmt->execute();
  return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function getPostById(int $id): ?array {
  $db = getDb();
  $stmt = $db->prepare('SELECT * FROM posts WHERE id = :id');
  $stmt->execute([':id' => $id]);
  $post = $stmt->fetch(PDO::FETCH_ASSOC);
  return $post ?: null;
}

function createDownload(string $title, ?string $description, string $storedFilename, string $originalFilename, ?string $mimeType, int $fileSize): int {
  $db = getDb();
  $stmt = $db->prepare('INSERT INTO downloads (title, description, stored_filename, original_filename, mime_type, file_size) VALUES (:t, :d, :sf, :of, :mt, :sz)');
  $stmt->execute([
    ':t' => $title,
    ':d' => $description,
    ':sf' => $storedFilename,
    ':of' => $originalFilename,
    ':mt' => $mimeType,
    ':sz' => $fileSize,
  ]);
  return (int)$db->lastInsertId();
}

function getAllDownloads(): array {
  $db = getDb();
  $stmt = $db->query('SELECT * FROM downloads ORDER BY created_at DESC');
  return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function getDownloadById(int $id): ?array {
  $db = getDb();
  $stmt = $db->prepare('SELECT * FROM downloads WHERE id = :id');
  $stmt->execute([':id' => $id]);
  $dl = $stmt->fetch(PDO::FETCH_ASSOC);
  return $dl ?: null;
}

// Ensure schema exists for every request in dev
initSchema();