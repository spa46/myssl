openssl s_client -connect localhost:4443 -servername valid.example.com -CAfile serverCA/ca-chain.pem

openssl s_client -connect localhost:4443 -servername expired.example.com -CAfile serverCA/ca-chain.pem

openssl s_client -connect localhost:4443 -servername revoked.example.com -CAfile serverCA/ca-chain.pem

openssl s_client -connect localhost:4443 -servername selfsigned.example.com -CAfile serverCA/ca-chain.pem
