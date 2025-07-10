<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");


$host = 'localhost';
$dbname = 'chapter_one_db'; 
$username = 'root';         
$password = 'root';        

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
    $which_event = trim($_POST['which_event_will_you_be_attending'] ?? null);
    $expectations = trim($_POST['expectations'] ?? '');


    if (!$name || !$email) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Name and email are required.'
        ]);
        exit;
    }

    try {
        
        $stmt = $pdo->prepare("INSERT INTO participants (name, email, expectations, which_event_will_you_be_attending) VALUES (?, ?, ?, ?)");
        $stmt->execute([$name, $email, $expectations, $which_event]);

        echo json_encode([
            'status' => 'success',
            'message' => 'Registration successful!'
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

