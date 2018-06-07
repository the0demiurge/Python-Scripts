# P2P Protocol

## Connection Method
socket, UDP(/TCP)
## Client Request
`(('username', 'ip', port, request, 'request_data'), 'Markdown message', (('binary object name', 'binary object data'), ...))`

Where request contains:

- message
- hello : `(('available time', int), ('erase after noconnection', int))`, if always available, set it to -1; if do not available, set to 0
- rsa pubkey
- AES key
- erase history
- erase keys
- erase all
- heart beat

## Server handling
- Add timestamp to first tuple
- Use 'ast.literal_eval' to parse client request

## Encryption, Decryption

Sender:

First connection: receive RSA key and save to contact

- Generate temp AES key
- Randomly choose iter times and print iter times
- Use RSA pubkey encrypt AES key plus salt with itertimes
- Uses AES when Transfering data
- Received hello message

Receiver:

First connection: send RSA pubkey encrypted by base64

- Receive encrypted AES key
- Use private key, salt and iter times decrypt AES key
- send hello message

# Saved Files
Config must be encrypted by self RSA pubkey, and privkey will be stored securily
## Contacts
## Messages
## Client and Server configs