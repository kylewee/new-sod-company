<?php
// Contact Form Handler - Sod.Company
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

// Get POST data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// If form data instead of JSON
if (empty($data)) {
    $data = $_POST;
}

// Validate required fields
if (empty($data['name']) || empty($data['phone'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Name and phone required']);
    exit;
}

// Sanitize
$lead = [
    'id' => 'lead-' . time() . '-' . rand(1000, 9999),
    'name' => htmlspecialchars($data['name'] ?? ''),
    'phone' => htmlspecialchars($data['phone'] ?? ''),
    'email' => htmlspecialchars($data['email'] ?? ''),
    'city' => htmlspecialchars($data['city'] ?? ''),
    'state' => htmlspecialchars($data['state'] ?? ''),
    'lawn_size' => htmlspecialchars($data['lawn_size'] ?? ''),
    'grass_type' => htmlspecialchars($data['grass_type'] ?? ''),
    'message' => htmlspecialchars($data['message'] ?? ''),
    'source' => htmlspecialchars($data['source'] ?? 'form'),
    'page' => htmlspecialchars($data['page'] ?? $_SERVER['HTTP_REFERER'] ?? ''),
    'timestamp' => date('Y-m-d H:i:s'),
    'ip' => $_SERVER['REMOTE_ADDR']
];

// Save to file
$leadsDir = __DIR__ . '/leads';
if (!is_dir($leadsDir)) {
    mkdir($leadsDir, 0755, true);
}
file_put_contents("$leadsDir/{$lead['id']}.json", json_encode($lead, JSON_PRETTY_PRINT));

// Send email notification
$to = 'leads@sod.company'; // CHANGE THIS
$subject = "New Lead: {$lead['name']} - {$lead['city']}";
$message = "
NEW SOD INSTALLATION LEAD

Name: {$lead['name']}
Phone: {$lead['phone']}
Email: {$lead['email']}
City: {$lead['city']}, {$lead['state']}
Lawn Size: {$lead['lawn_size']}
Grass Type: {$lead['grass_type']}
Message: {$lead['message']}

Source: {$lead['source']}
Page: {$lead['page']}
Time: {$lead['timestamp']}

FOLLOW UP IMMEDIATELY!
";

$headers = "From: noreply@sod.company\r\n";
$headers .= "Reply-To: {$lead['email']}\r\n";

@mail($to, $subject, $message, $headers);

// Return success
echo json_encode([
    'success' => true,
    'leadId' => $lead['id'],
    'message' => 'Thank you! We will contact you shortly.'
]);
