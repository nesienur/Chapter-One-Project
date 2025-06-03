<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

// Database connection settings — UPDATE THESE!
$host = 'localhost';
$dbname = 'chapter_one_db'; // <-- Your database name
$username = 'root';         // Default for MAMP
$password = 'root';         // Default for MAMP (NOT empty)

try {
    // Connect using PDO
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode([
        'status' => 'error',
        'message' => 'Database connection failed: ' . $e->getMessage()
    ]);
    exit;
}

// Handle POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $expectations = trim($_POST['expectations'] ?? '');

    if (!$name || !$email) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Name and email are required.'
        ]);
        exit;
    }

    try {
        // Prepare and insert data
        $stmt = $pdo->prepare("INSERT INTO participants (name, email, expectations) VALUES (?, ?, ?)");
        $stmt->execute([$name, $email, $expectations]);

        echo json_encode([
            'status' => 'success',
            'message' => 'Registration successful and saved to database!'
        ]);
        exit;
    } catch (PDOException $e) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Failed to save: ' . $e->getMessage()
        ]);
        exit;
    }
} else {
    echo json_encode([
        'status' => 'error',
        'message' => 'Invalid request method.'
    ]);
    exit;
}
?>
