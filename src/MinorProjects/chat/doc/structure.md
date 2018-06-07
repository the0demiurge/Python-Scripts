# P2P Protocol

## Connection Method

socket, UDP(/TCP)

## Client Request

```python
(
    ('username', 'ip', port, request, 'request_data'),
    'Markdown message',
    (('binary object name', 'binary object data'), (...))
)
```

Where request contains:

- message
- hello : `(('available time', int), ('erase after noconnection', int))`, if always available, set it to -1; if do not available, set to 0
- RSA pubkey
- AES key
- erase history
- erase keys
- erase all
- heart beat

## Server handling
- Add timestamp to first tuple
- Use 'ast.literal_eval' to parse client request

## Encryption, Decryption

Use ECDHE, RSA, AES, PSK

# Saved Files

Config must be encrypted by self RSA pubkey, and privkey should be stored securily, thus configs cannot be pried without keys

## Contacts

```python
{
    'contact name':[
        pubkey,
        ('host', port),
        aes_key
        ]
}

```
## Messages
```python
{
    ('contact name', 'host', port):[

    ]
}
```


## Client and Server configs
```python
{
    'item':value
}
```

# Group Chat Protocol

Broadcast message to all network by traverse the graph, maintain a cluster shared contact list.