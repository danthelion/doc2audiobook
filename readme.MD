# doc2audiobook.py


`/data/input` holds all input files.
`/data/output` will hold all output files.


# Build
```
docker build -t doc2audiobook .
```

# Run
```
# List available voices
docker run \
-v /Users/danielpalma/doc2audiobook/data:/data:rw \
-v /Users/danielpalma/doc2audiobook/.secrets/client_secret.json:/.secrets/client_secret.json:ro \
doc2audiobook -list-voices

# Convert a document to an audiobook
sudo docker run \
-v /Users/danielpalma/doc2audiobook/data:/data:rw \
-v /Users/danielpalma/doc2audiobook/.secrets/client_secret.json:/.secrets/client_secret.json:ro \
doc2audiobook --voice en-GB-Standard-C
```