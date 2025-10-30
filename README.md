# Cyber Escape Room

A Python CLI-based escape room game simulating blue-team cybersecurity defense operations. Players collect tokens by solving security-themed puzzles across five rooms, each representing a different aspect of incident response and threat hunting.

## About

This escape room compresses the spectrum of security operations into five simplified challenges:

| Room | Challenge | Real-World Parallel |
|------|-----------|---------------------|
| **SOC Triage Desk** | Log parsing & anomaly detection | Analysts review auth logs for brute force attacks |
| **DNS Closet** | Config analysis & decoding | Incident responders decode obfuscated hints in configs |
| **Vault Corridor** | Regex search & validation | Forensics sift through dumps for valid artifacts |
| **Malware Lab** | Graph traversal | Threat hunters trace malware process trees |
| **Final Gate** | Verification & reporting | Teams package findings into cryptographic proofs |

## How to Play

### Starting the Game

1. Clone the repository:

```bash
git clone git@github.com:John-Popovici/MCYSD-19-escape-room.git
```

2. Set up environment

```bash
uv sync
```

3. Run the project

```bash
uv run src/escape.py
```

### Game Flow

1. **Start in the Intro Lobby** - The central hub connecting all rooms
2. **Move between rooms** - Navigate to SOC, DNS, Vault, or Malware Lab
3. **Inspect items** - Examine files to trigger puzzle-solving logic
4. **Collect tokens** - Each room yields one token upon successful completion
5. **Reach the Final Gate** - Combine all four tokens in the correct order
6. **Complete verification** - Output the combined message with HMAC for instructor verification

### Room Objectives

#### Room 1: Intro Lobby
**Token:** None  
**Purpose:** Game engine initialization and navigation hub

#### Room 2: SOC Triage Desk (`auth.log`)
**Token:** KEYPAD  
**Task:** Parse SSH authentication logs to identify brute-force attacks. Find the /24 subnet with the most failures and extract the keypad code from the most frequent attacking IP.

#### Room 3: DNS Closet (`dns.cfg`)
**Token:** DNS  
**Task:** Decode base64-encoded hints from a configuration file. Use the `token_tag` to identify which hint contains the valid token (last word of decoded string).

#### Room 4: Vault Corridor (`vault_dump.txt`)
**Token:** SAFE  
**Task:** Search a noisy text dump for `SAFE{a-b-c}` patterns using regex. Validate that only one candidate satisfies the checksum `a + b = c`.

#### Room 5: Malware Lab (`proc_tree.jsonl`)
**Token:** PID  
**Task:** Build a process tree from JSON-lines data. Use DFS/BFS traversal to find malicious chains ending in exfiltration commands (`curl` or `scp`). Return the terminal PID.

#### Final Gate (`final_gate.txt`)
**Token:** ESCAPE  
**Task:** Read the token order, group ID, and expected HMAC. Combine tokens in the specified order: `group_id|token1-token2-token3-token4`. Output for verification.

## Commands

### Game Commands

| Command | Description | Example |
|---------|-------------|---------|
| `look` | Examine your current room and see available exits | `> look` |
| `move <room>` | Navigate to another room | `> move soc` |
| `inventory` | Display collected tokens | `> inventory` |
| `help` | Show available commands | `> help` |
| `save <file>` | Save game progress to JSON file | `> save save1.json` |
| `load <file>` | Load game progress from JSON file | `> load save1.json` |
| `quit` | Exit the game and write transcript | `> quit` |

### Room Commands

| Command | Description | Example |
|---------|-------------|---------|
| `inspect <item>` | Examine a file/item to solve the room's puzzle | `> inspect auth.log` |
| `use <item>` | Use an item (e.g., attempt Final Gate with collected tokens) | `> use gate` |
| `hint` | Request a hint for the current room | `> hint` |