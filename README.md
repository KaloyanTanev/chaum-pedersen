# Chaum-Pedersen ZKP

## Introduction

Chaum-Pedersen zero knowledge proof implementation in Python. Quick implementation of the protocol is available `chaum_pedersen.py`. It serves only as demonstrational purposes for the background calculations.

In `/app` there is an implementation of client-server communication via gRPC.

## Run locally

### Prepare environment

```sh
scripts/update_proto.sh
scripts/venv_setup.sh
source venv/bin/activate
docker-compose up -d redis # or your local Redis instance

python3 app/victor/victor.py
```

### Use client

#### Register

Client is accepting a number (secret), registers it with the server and returns the random prime number generated. This prime number should be stored, so it can be reused later on for logging in.

```sh
python3 app/peggy/peggy.py register -s ${SECRET}
```

Example request:

```sh
python3 app/peggy/peggy.py register -s 123
```

Example response:

```sh
157360668734434990285839916876951699033602410454308426433468085480284003817301482464165455037654048596347789589086255823400592679731982756027484164480954597575310097972589187852240388920290281011504939640293166111231509991974534860763163500734488993174560764639540033076095728568655453279638565710498651806239
```

#### Login

Client is accepting a number (secret), and a prime number. It checks with the server if it can login.

```sh
python3 app/peggy/peggy.py login -s ${SECRET} -p ${PRIME}
```

Example request:

```sh
python3 app/peggy/peggy.py login -s 123 -p 157360668734434990285839916876951699033602410454308426433468085480284003817301482464165455037654048596347789589086255823400592679731982756027484164480954597575310097972589187852240388920290281011504939640293166111231509991974534860763163500734488993174560764639540033076095728568655453279638565710498651806239
```

Example response:

```sh
True
```

## Run in Docker

### Prepare environment

```sh
scripts/update_proto.sh
docker-compose up
```

### Use client

#### Register

Client is accepting a number (secret), registers it with the server and returns the random prime number generated. This prime number should be stored, so it can be reused later on for logging in.

```sh
docker exec peggy python3 app/peggy/peggy.py register -s ${SECRET}
```

Example request:

```sh
docker exec peggy python3 app/peggy/peggy.py register -s 123
```

Example response:

```sh
157360668734434990285839916876951699033602410454308426433468085480284003817301482464165455037654048596347789589086255823400592679731982756027484164480954597575310097972589187852240388920290281011504939640293166111231509991974534860763163500734488993174560764639540033076095728568655453279638565710498651806239
```

#### Login

Client is accepting a number (secret), and a prime number. It checks with the server if it can login.

```sh
docker exec peggy python3 app/peggy/peggy.py login -s ${SECRET} -p ${PRIME}
```

Example request:

```sh
docker exec peggy python3 app/peggy/peggy.py login -s 123 -p 157360668734434990285839916876951699033602410454308426433468085480284003817301482464165455037654048596347789589086255823400592679731982756027484164480954597575310097972589187852240388920290281011504939640293166111231509991974534860763163500734488993174560764639540033076095728568655453279638565710498651806239
```

Example response:

```sh
True
```

## Run unit tests

```sh
./scripts/unit_test.sh
```

## Further work and improvements

- Prime number can be saved in a database on client's side. This way client won't be required to provide the prime number;
- Bad weather unit tests;
- Integration, e2e and coverage tests;
- Improved env variables handling;
- Healthcheck endpoints;
- Randomly choose generators g and h. Right now I have them as environment variables with default values 4 and 9. However, it would be better to select random generators on start. More literature on this:
  - [Cryptography: An Introduction (3rd Edition) by Nigel Smart](https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf)
  - [Notes on ZKP by Jorge L. Villar](https://web.mat.upc.edu/jorge.villar/doc/notes/DataProt/zk.pdf)
  - [Lecture on Proofs by Susan Hohenberger](https://www.cs.jhu.edu/~susan/600.641/scribes/lecture10.pdf).
