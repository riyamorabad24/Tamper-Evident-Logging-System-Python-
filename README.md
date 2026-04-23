# Tamper-Evident-Logging-System-Python-
A Python-based tamper-evident logging system using SHA-256 hashing to ensure log integrity and detect unauthorized modifications.

📌 Overview
This project implements a tamper-evident logging system using SHA-256 hashing to ensure log integrity.
Each log entry is cryptographically linked to the previous one, forming a secure chain similar to blockchain principles.
Any unauthorized modification, deletion, or reordering of logs is automatically detected.

🎯 Objectives
Create secure, tamper-proof logs
Detect unauthorized modifications
Demonstrate chain integrity verification
Simulate attacker behavior

🛠️ Technologies Used
Python
SHA-256 Hashing
JSON (for log storage)

⚙️ Features
Add log entries (LOGIN, LOGOUT, TRANSACTION)
View complete log chain
Verify integrity of logs
Detect tampering using hash mismatch
Simulate attacker modifying logs
Clear logs (reset system)

🚀 How It Works
Each log entry contains:
Index
Timestamp
Event Type
Description
Previous Hash
Entry Hash

👉 Each entry hash is calculated using:
SHA-256(index + timestamp + event + description + previous_hash)
This ensures:
If one entry changes → entire chain breaks
Tampering becomes instantly detectable

▶️ Running the Project
python tamper_evident_log_menu.py

🧪 Demonstration
🔹 Menu Interface
🔹 Viewing Log Entries
🔹 Integrity Verification (Valid)
🔹 Tampering Simulation
🔹 Tampering Detection

🔍 Sample Output
✅ All entries intact → System secure
❌ Tampering detected → Chain compromised

📂 Project Structure
.
├── tamper_evident_log_menu.py
├── secure_log.json
├── images/
└── README.md

📊 Learning Outcomes
Understanding of cryptographic hashing
Concept of chained data integrity (blockchain basics)
Detection of unauthorized data modification
Secure logging practices

⚠️ Disclaimer
This project is for educational purposes only and demonstrates basic security concepts.
