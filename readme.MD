# doc2audiobook.py

Extract text from a document ([textract](https://textract.readthedocs.io)) and convert it into
a natural sounding synthesised speech ([Cloud Text-To-Speech](https://cloud.google.com/text-to-speech/)), which
is able to leverage Deepminds Wavenet models.

## Example

[Input](examples/woody.pdf)
[Output](examples/woody.mp3)

Available source formats (from `textract`)

- .csv
- .doc
- .docx
- .eml
- .epub
- .gif
- .jpg and .jpeg
- .json
- .html and .htm
- .mp3
- .msg
- .odt
- .ogg
- .pdf
- .png
- .pptx
- .ps
- .rtf
- .tiff
- .txt
- .wav
- .xlsx
- .xls

## Prerequisites

GCP
1. Select or create a Cloud Platform project.
2. Enable billing for your project.
3. Enable the Cloud Text-to-Speech API.
4. Setup Authentication using a Service Account.

Host Machine
1. Docker
2. `/doc2audiobook/data/input`: directory to hold all input files.
3. `/doc2audiobook/data/output`: directory to store all output files.
4. `/doc2audiobook/.secrets/client_secret.json`: GCP authentication token.

## Build

```
$ git clone git@github.com:danthelion/doc2audiobook.git
$ cd doc2audiobook
$ docker build -t doc2audiobook .
```

## Run

Make sure to put your documents in the folder that is mapped to `/data` before running!

List available voices
```
$ docker run \
$ -v /doc2audiobook/data:/data:rw \
$ -v /doc2audiobook/.secrets/client_secret.json:/.secrets/client_secret.json:ro \
$ doc2audiobook -list-voices
```

Convert a document to an audiobook using the _en-GB-Standard-C_ voice.
```
$ docker run \
$ -v /doc2audiobook/data:/data:rw \
$ -v /doc2audiobook/.secrets/client_secret.json:/.secrets/client_secret.json:ro \
$ doc2audiobook --voice en-GB-Standard-C
```