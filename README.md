# Tamper-Evident-Logging-System-Python-
A Python-based tamper-evident logging system using SHA-256 hashing to ensure log integrity and detect unauthorized modifications.

📌 Overview
This project implements a secure logging system where each log entry is linked using SHA-256 hashing.
Any modification in logs breaks the chain and is immediately detected.

🎯 Features
Add log entries (LOGIN, LOGOUT, TRANSACTION)
View complete logs
Verify chain integrity
Detect tampering
Simulate attacker modifications

⚙️ How It Works
Each log entry contains:
Index
Timestamp
Event Type
Description
Previous Hash
Entry Hash
Each entry is linked to the previous one using SHA-256 hashing, forming a secure chain.

▶️ Run the Project
python tamper_evident_log_menu.py

🧪 Output Screens
Add Log Entry
View Logs
Integrity Check (Valid)
Tampering Simulation
Tampering Detected

📊 Learning Outcomes
Cryptographic hashing (SHA-256)
Data integrity verification
Blockchain-like chaining concept
Security attack detection
