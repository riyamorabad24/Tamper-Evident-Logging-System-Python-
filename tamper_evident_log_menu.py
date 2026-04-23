"""
Tamper-Evident Logging System (Menu Version)
=============================================
Each log entry is cryptographically linked to the previous one using SHA-256 hashing.
Any modification, deletion, or reordering of entries will be detected during verification.

Author: [Your Name]
"""

import hashlib
import json
import os
from datetime import datetime, timezone


LOG_FILE = "secure_log.json"


# ─────────────────────────────────────────────
# CORE HASHING
# ─────────────────────────────────────────────

def compute_hash(entry: dict) -> str:
    """
    Compute SHA-256 hash of a log entry (excluding the 'entry_hash' field itself).
    The hash covers: index, timestamp, event_type, description, previous_hash.
    """
    data = {
        "index":         entry["index"],
        "timestamp":     entry["timestamp"],
        "event_type":    entry["event_type"],
        "description":   entry["description"],
        "previous_hash": entry["previous_hash"],
    }
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


# ─────────────────────────────────────────────
# ADD LOG ENTRY
# ─────────────────────────────────────────────

def add_log(event_type: str, description: str) -> dict:
    """Append a new tamper-evident entry to the log chain."""
    chain = load_chain()

    previous_hash = chain[-1]["entry_hash"] if chain else "GENESIS"

    entry = {
        "index":         len(chain),
        "timestamp":     datetime.now(timezone.utc).isoformat(),
        "event_type":    event_type.upper(),
        "description":   description,
        "previous_hash": previous_hash,
        "entry_hash":    "",
    }
    entry["entry_hash"] = compute_hash(entry)

    chain.append(entry)
    save_chain(chain)

    print(f"\n[+] Entry #{entry['index']} added successfully!")
    print(f"    Hash: {entry['entry_hash'][:32]}...")
    return entry


# ─────────────────────────────────────────────
# VERIFY CHAIN INTEGRITY
# ─────────────────────────────────────────────

def verify_chain() -> bool:
    """Walk every entry and verify the chain is intact."""
    chain = load_chain()

    if not chain:
        print("\n[!] Log is empty — nothing to verify.")
        return True

    print("\n" + "=" * 60)
    print("  CHAIN INTEGRITY VERIFICATION")
    print("=" * 60)

    all_valid = True

    for i, entry in enumerate(chain):
        issues = []

        expected_hash = compute_hash(entry)
        if entry["entry_hash"] != expected_hash:
            issues.append("CONTENT TAMPERED (hash mismatch)")

        if i == 0:
            if entry["previous_hash"] != "GENESIS":
                issues.append("GENESIS LINK BROKEN")
        else:
            if entry["previous_hash"] != chain[i - 1]["entry_hash"]:
                issues.append("CHAIN LINK BROKEN (deletion or reorder detected)")

        if issues:
            all_valid = False
            print(f"  [FAIL] Entry #{i:03d} | {', '.join(issues)}")
            print(f"         Event   : {entry['event_type']}")
            print(f"         Time    : {entry['timestamp']}")
        else:
            print(f"  [ OK ] Entry #{i:03d} | {entry['event_type']:20s} | {entry['timestamp']}")

    print("=" * 60)
    if all_valid:
        print(f"  RESULT : ✅  All {len(chain)} entries are INTACT.")
    else:
        print("  RESULT : ❌  TAMPERING DETECTED — chain is compromised!")
    print("=" * 60 + "\n")

    return all_valid


# ─────────────────────────────────────────────
# VIEW LOG
# ─────────────────────────────────────────────

def view_log():
    """Pretty-print every log entry currently stored."""
    chain = load_chain()

    if not chain:
        print("\n[!] Log is empty — add some entries first.")
        return

    print("\n" + "=" * 60)
    print("  LOG ENTRIES")
    print("=" * 60)
    for entry in chain:
        print(f"  Index       : {entry['index']}")
        print(f"  Timestamp   : {entry['timestamp']}")
        print(f"  Event Type  : {entry['event_type']}")
        print(f"  Description : {entry['description']}")
        print(f"  Prev Hash   : {entry['previous_hash'][:32]}...")
        print(f"  Entry Hash  : {entry['entry_hash'][:32]}...")
        print("-" * 60)


# ─────────────────────────────────────────────
# SIMULATE TAMPERING
# ─────────────────────────────────────────────

def simulate_tampering():
    """Silently modify an entry on disk to simulate an attacker."""
    chain = load_chain()

    if len(chain) < 2:
        print("\n[!] Need at least 2 entries to simulate tampering.")
        print("    Please add more log entries first.")
        return

    print("\n" + "=" * 60)
    print("  SIMULATING TAMPERING")
    print("=" * 60)
    print("  [!] An attacker is secretly modifying Entry #1 on disk...")
    chain[1]["description"] = "*** TAMPERED BY ATTACKER ***"
    save_chain(chain)
    print("  [!] Entry #1 description has been silently changed.")
    print("  [!] Now run option 3 to verify and catch the tampering!")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────
# FILE I/O
# ─────────────────────────────────────────────

def load_chain() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def save_chain(chain: list):
    with open(LOG_FILE, "w") as f:
        json.dump(chain, f, indent=2)


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────

def show_menu():
    print("\n" + "=" * 60)
    print("  TAMPER-EVIDENT LOGGING SYSTEM")
    print("=" * 60)
    print("  1. Add a log entry")
    print("  2. View all log entries")
    print("  3. Verify chain integrity")
    print("  4. Simulate tampering (attacker demo)")
    print("  5. Clear all logs (fresh start)")
    print("  6. Exit")
    print("=" * 60)


def main():
    print("\nWelcome to the Tamper-Evident Logging System!")

    while True:
        show_menu()
        choice = input("  Choose option (1-6): ").strip()

        if choice == "1":
            print("\n-- ADD LOG ENTRY --")
            event = input("  Enter event type (e.g. LOGIN, LOGOUT, TRANSACTION): ").strip()
            desc  = input("  Enter description: ").strip()
            if event and desc:
                add_log(event, desc)
            else:
                print("[!] Event type and description cannot be empty.")

        elif choice == "2":
            view_log()

        elif choice == "3":
            verify_chain()

        elif choice == "4":
            simulate_tampering()

        elif choice == "5":
            confirm = input("  Are you sure you want to clear all logs? (yes/no): ").strip().lower()
            if confirm == "yes":
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                print("\n[+] All logs cleared. Fresh start!")
            else:
                print("\n[!] Cancelled.")

        elif choice == "6":
            print("\nGoodbye!\n")
            break

        else:
            print("\n[!] Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
