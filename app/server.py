import socket
import threading
import os
import sys
import sqlite3
from collections import defaultdict
from root_dir import ROOT_DIR 

class Server(object):
    def __init__(self, HOST='localhost', PORT=7734, V='P2P-CI/1.0'):
        self.HOST = HOST
        self.PORT = PORT
        self.V = V
        self.peers = defaultdict(set)
        self.rfcs = {}
        self.lock = threading.Lock()
        self.setup_database()

    def setup_database(self):
        self.conn = sqlite3.connect(os.path.join(ROOT_DIR , 'users.db'))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def verify_user(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = self.cursor.fetchone()
        return user is not None

    # start listening
    def start(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.HOST, self.PORT))
            self.s.listen(5)
            print('\n\n---------------Server %s is listening on port %s--------------' %
                  (self.V, self.PORT))

            while True:
                soc, addr = self.s.accept()
                print('%s:%s connected' % (addr[0], addr[1]))
                thread = threading.Thread(
                    target=self.handler, args=(soc, addr))
                thread.start()
        except KeyboardInterrupt:
            print('\n---------------Shutting down the server..-----------------\n---------------Good Bye!-----------------\n\n')
            self.conn.close()  # Close the database connection
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    # connect with a client
    def handler(self, soc, addr):
        host = None
        port = None
        while True:
            try:
                req = soc.recv(1024).decode()
                print('Receive request:\n%s' % req)
                lines = req.splitlines()
                version = lines[0].split()[-1]

                if version != self.V:
                    soc.sendall(str.encode(
                        self.V + ' 505 P2P-CI Version Not Supported\n'))
                else:
                    method = lines[0].split()[0]
                    if method == 'ADD':
                        host = lines[1].split(None, 1)[1]
                        port = int(lines[2].split(None, 1)[1])
                        num = int(lines[0].split()[-2])
                        title = lines[3].split(None, 1)[1]
                        self.addRecord(soc, (host, port), num, title)
                    elif method == 'LOOKUP':
                        num = int(lines[0].split()[-2])
                        self.getPeersOfRfc(soc, num)
                    elif method == 'LIST':
                        self.getAllRecords(soc)
                    elif method == 'LOGIN':
                        username = lines[1].split(None, 1)[1]
                        password = lines[2].split(None, 1)[1]
                        if self.verify_user(username, password):
                            soc.sendall(str.encode(self.V + ' 200 Login Successful\n'))
                        else:
                            soc.sendall(str.encode(self.V + ' 401 Unauthorized\n'))
                    elif method == 'SIGNUP':
                        username = lines[1].split(None, 1)[1]
                        password = lines[2].split(None, 1)[1]
                        if self.add_user(username, password):
                            soc.sendall (str.encode(self.V + ' 201 Signup Successful\n'))
                        else:
                            soc.sendall(str.encode(self.V + ' 409 Conflict: Username already exists\n'))
                    else:
                        raise AttributeError('Method Not Match')
            except ConnectionError:
                print('%s:%s left' % (addr[0], addr[1]))
                if host and port:
                    self.clear(host, port)
                soc.close()
                break
            except BaseException:
                try:
                    soc.sendall(str.encode(self.V + ' 400 Bad Request\n'))
                except ConnectionError:
                    print('%s:%s left' % (addr[0], addr[1]))
                    if host and port:
                        self.clear(host, port)
                    soc.close()
                    break

    def clear(self, host, port):
        self.lock.acquire()
        nums = self.peers[(host, port)]
        for num in nums:
            self.rfcs[num][1].discard((host, port))
        if not self.rfcs[num][1]:
            self.rfcs.pop(num, None)
        self.peers.pop((host, port), None)
        self.lock.release()

    def addRecord(self, soc, peer, num, title):
        self.lock.acquire()
        try:
            self.peers[peer].add(num)
            self.rfcs.setdefault(num, (title, set()))[1].add(peer)
        finally:
            self.lock.release()
        header = self.V + ' 200 OK\n'
        header += 'RFC %s %s %s %s\n' % (num, self.rfcs[num][0], peer[0], peer[1])
        soc.sendall(str.encode(header))

    def getPeersOfRfc(self, soc, num):
        self.lock.acquire()
        try:
            if num not in self.rfcs:
                header = self.V + ' 404 Not Found\n'
            else:
                header = self.V + ' 200 OK\n'
                title = self.rfcs[num][0]
                for peer in self.rfcs[num][1]:
                    header += 'RFC %s %s %s %s\n' % (num, title, peer[0], peer[1])
        finally:
            self.lock.release()
        soc.sendall(str.encode(header))

    def getAllRecords(self, soc):
        self.lock.acquire()
        try:
            if not self.rfcs:
                header = self.V + ' 404 Not Found\n'
            else:
                header = self.V + ' 200 OK\n'
                for num in self.rfcs:
                    title = self.rfcs[num][0]
                    for peer in self.rfcs[num][1]:
                        header += 'RFC %s %s %s %s\n' % (num, title, peer[0], peer[1])
        finally:
            self.lock.release()
        soc.sendall(str.encode(header))


if __name__ == '__main__':
    s = Server()
    s.start()