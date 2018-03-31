# Build
```
docker build -t doc2audiobook .
```

# Run
```
sudo docker run -v /Users/danielpalma/doc2audiobook/data:/data:rw -v /Users/danielpalma/doc2audiobook/.secrets/client_secret.json:/.secrets/client_secret.json:ro doc2audiobook -v /Users/danielpalma/doc2audiobook/log:/log:rw
```