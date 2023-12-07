import argparse
import logging
import os
import sys

import grpc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import common.chaum_pedersen as cp
import cp_pb2
import cp_pb2_grpc

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

host = os.getenv("SERVER_HOST", "localhost")
port = os.getenv("SERVER_PORT", "50051")

def grpc_req_register(y1, y2, p):

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = cp_pb2_grpc.CpStub(channel)
        resp = stub.Register(cp_pb2.RegisterRequest(y1=str(y1), y2=str(y2), p=str(p)))
    return resp

def grpc_req_login_r1(id, r1, r2):

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = cp_pb2_grpc.CpStub(channel)
        resp = stub.LoginRoundOne(cp_pb2.LoginRequestRoundOne(id=id, r1=str(r1), r2=str(r2)))

    return resp

def grpc_req_login_r2(id, s):

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        stub = cp_pb2_grpc.CpStub(channel)
        resp = stub.LoginRoundTwo(cp_pb2.LoginRequestRoundTwo(id=id, s=str(s)))

    return resp

def Register(x):
    logging.info("Registering flow initiated")
    logging.info("Generating safe prime number...")
    p = cp.generate_safe_prime()

    g = cp.get_g()
    h = cp.get_h()

    logging.info("Calculating y1 and y2...")
    y1 = pow(g, x, p)
    y2 = pow(h, x, p)

    logging.info("Sending request to server")
    response = grpc_req_register(y1, y2, p)
    if response.error != "":
        err = f"Error on register {response.error}"
        logging.error(err)
        return err

    logging.info("Register flow completed")
    logging.info("Secret registered\n")
    return p

def Login(x, p):
    logging.info("Logging flow initiated")
    g = cp.get_g()
    h = cp.get_h()

    logging.info("Re-calculating y1 and y2...")
    y1 = pow(g, x, p)
    y2 = pow(h, x, p)
    id = cp.calcualte_id(y1, y2, p)

    logging.info("Picking random k...")
    k = cp.random_number()
    logging.info("Calculating client-side r1...")
    r1 = pow(g, k, p)
    logging.info("Calculating client-side r2...")
    r2 = pow(h, k, p)

    logging.info("Sending round 1 request to server")
    responseRoundOne = grpc_req_login_r1(id, r1, r2)
    if responseRoundOne.error != "":
        err = f"Error on round 1 {responseRoundOne.error}"
        logging.error(err)
        return err

    c = int(responseRoundOne.c)
    q = (p-1)//2
    logging.info("Calculating s...")
    s = (k - (c*x)) % q

    logging.info("Sending round 2 request to server")
    responseRoundTwo = grpc_req_login_r2(id, s)
    if responseRoundTwo.error != "":
        err = f"Error on round 2 {responseRoundTwo.error}"
        logging.error(err)
        return err

    logging.info("Register flow completed")
    logging.info(f"Login allowed: {responseRoundTwo.b}\n")
    return responseRoundTwo.b

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Make request for chaum_pedersen')
    parser.add_argument('action', nargs='?', default=None)
    parser.add_argument('-s', '--secret', dest='secret', type=str, help="secret value")
    parser.add_argument('-p', '--prime', dest='prime', type=str, help="secret prime for login")

    args = parser.parse_args()
    if (args.action == 'register'):
        if(args.secret == None):
            logging.error("secret not supplied")
            sys.exit(1)
        try:
            secret_int = int(args.secret)
        except ValueError:
            logging.error("secret should be an integer")
            sys.exit(1)
        res = Register(secret_int)
        print(res)
        sys.exit(0)
    elif (args.action == 'login'):
        if(args.secret == None):
            logging.error("secret not supplied")
            sys.exit(1)
        if(args.prime == None):
            logging.error("id not supplied")
            sys.exit(1)
        try:
            secret_int = int(args.secret)
            prime_int = int(args.prime)
        except ValueError:
            logging.error("secret and prime should be integers")
            sys.exit(1)
        res = Login(secret_int, prime_int)
        print(res)
        sys.exit(0)
    else:
        logging.error("Unknown action: " + args.action + " available actions are login and register")
