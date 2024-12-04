# P2P File Sharing Application

## Overview
This is a Peer-to-Peer (P2P) File Sharing application built in Python, featuring user authentication via SQLite and a comprehensive file sharing system with multiple functionalities.

## Features
- User Authentication (Login/Signup)
- RFC (Request for Comments) File Sharing
- Peer Discovery
- File Upload
- File Search
- File Download
- Shareable File Repository

## Technologies Used
- Python
- Socket Programming
- SQLite
- Threading
- Platform-independent Design

## Prerequisites
- Python 3.7+
- Standard Python Libraries (socket, threading, sqlite3)

## Project Structure
```
p2p-file-sharing/
│
├── server.py            # Main server implementation
├── client.py            # Main client implementation
├── root_dir.py          # Root directory configuration
├── SHARED_FILES/        # Default directory for shared files
├── screenshots/         # Screenshots of application
└── README.md            # Project documentation
```

## Setup and Installation

1. Clone the Repository
```bash
git clone https://github.com/yourusername/p2p-file-sharing.git
cd p2p-file-sharing
```

2. Install Dependencies
```bash
# No external dependencies required
```

3. Run the Server
```bash
python server.py
```

4. Run the Client
```bash
python client.py
```

## User Workflow

### Authentication
1. Run the client application
2. Choose between Login, Signup, or Quit
3. After successful authentication, access the main menu

### Main Menu Options
1. **Upload**: Share a file with the P2P network
2. **Search**: Find files by RFC number
3. **List All**: View all available files in the network
4. **Download**: Download files from peers
5. **Shut Down**: Exit the application

## Screenshots

### Directory Structure
![Directory Structure](screenshots/directory_structure.jpeg)

### Login Screen
![Login Screen](screenshots/login_screen.png)

### Main Menu
![Main Menu](screenshots/main_menu.png)

### File Upload
![File Upload](screenshots/file_upload.png)

### File Search
![File Search](screenshots/file_search.png)

### Download Process
![Download Process](screenshots/download_process.png)

## Security Notes
- Passwords are stored in SQLite database
- Basic authentication mechanism
- Recommended to enhance security in production

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Learning Outcomes
This Peer-to-Peer File Sharing project serves as an excellent demonstration of distributed systems principles, showcasing:

Practical implementation of socket programming
User authentication mechanisms
Distributed file discovery and sharing
Concurrent network communication using threading

## Reflection
This project provides a foundational understanding of how peer-to-peer networks operate, demonstrating the power of decentralized file-sharing systems. It highlights the importance of network programming, concurrent processing, and distributed system design.
By breaking down complex networking concepts into manageable components, this application serves as both a learning tool and a proof of concept for distributed file-sharing technologies.
