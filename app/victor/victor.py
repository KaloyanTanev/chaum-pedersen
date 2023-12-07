from concurrent import futures
import logging
import os
import sys

import grpc
import redis

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import common.chaum_pedersen as cp
import cp_pb2
import cp_pb2_grpc

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

class Victor(cp_pb2_grpc.CpServicer):
    def __init__(self) -> None:
        # Setup Redis
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_password = os.getenv('REDIS_PASSWORD', 'dummy')
        try:
            self.redis = redis.Redis(host=str(redis_host), password=redis_password, health_check_interval=10, socket_connect_timeout=10, socket_keepalive=True)
            self.redis.ping()
        except Exception as ex:
            logging.error(f"Could not connect to Redis {ex}")
            sys.exit(1)
        self.g = cp.get_g()
        self.h = cp.get_h()

    def Register(self, request, context):
        logging.info("Registering flow initiated")
        id = cp.calcualte_id(request.y1, request.y2, request.p)
        try:
            logging.info("Writing id to Redis...")
            self.redis.set(id, f'{request.y1} {request.y2} {request.p}')
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            return cp_pb2.RegisterResponse(id="", error=err)

        logging.info("Register flow completed\n")
        return cp_pb2.RegisterResponse(id=id, error="")

    def LoginRoundOne(self, request, context):
        logging.info("Logging round 1 flow initiated")
        try:
            logging.info("Reading id from Redis...")
            y1y2p = self.redis.get(request.id)
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            return cp_pb2.LoginResponseRoundOne(c="", error=err)

        if y1y2p == None:
            err = f"Id {request.id} not found"
            logging.error(err)
            return cp_pb2.LoginResponseRoundOne(c="", error=err)

        try:
            existing_comm = self.redis.get(f"{request.id}-comm")
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            return cp_pb2.LoginResponseRoundOne(c="", error=err)

        if existing_comm != None:
            err = f"Commitment already submitted for id {request.id}"
            logging.error(err)
            return cp_pb2.LoginResponseRoundOne(c="", error=err)

        logging.info("Picking random c...")
        c = str(cp.random_number())
        try:
            self.redis.set(f"{request.id}-comm", f"{c} {request.r1} {request.r2}")
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            return cp_pb2.LoginResponseRoundOne(c="", error=err)

        logging.info("Logging round 1 flow completed\n")
        return cp_pb2.LoginResponseRoundOne(c=c, error="")

    def LoginRoundTwo(self, request, context):
        logging.info("Logging round 2 flow initiated")
        try:
            logging.info("Reading commitment, r1 and r2 from Redis...")
            comm = self.redis.get(f"{request.id}-comm")
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error=err)

        if comm == None:
            err = f"commitment for id {request.id} not found"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error=err)

        commArray = str.split(comm.decode("utf-8"))
        c = int(commArray[0])
        r1 = int(commArray[1])
        r2 = int(commArray[2])

        try:
            logging.info("Reading y1, y2 and prime from Redis...")
            y1y2p = self.redis.get(f"{request.id}")
        except Exception as ex:
            err = f"Redis: unexpected exception {ex}"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error=err)

        if y1y2p == None:
            err = f"id {request.id} not found"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error=err)

        y1y2pArray = str.split(y1y2p.decode("utf-8"))
        y1 = int(y1y2pArray[0])
        y2 = int(y1y2pArray[1])
        p = int(y1y2pArray[2])

        s = int(request.s)

        logging.info("Calculating server-side r1...")
        r1_comp = (pow(self.g, s, p) * pow(y1, c, p)) % p
        if(r1_comp != r1):
            err = "Server and client side r1 do not match"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error="")

        logging.info("Calculating server-side r2...")
        r2_comp = (pow(self.h, s, p) * pow(y2, c, p)) % p
        if(r2_comp != r2):
            err = "Server and client side r2 do not match"
            logging.error(err)
            self.redis.delete(f"{request.id}-comm")
            return cp_pb2.LoginResponseRoundTwo(b=False, error="")
        self.redis.delete(f"{request.id}-comm")

        logging.info("Logging round 2 flow completed\n")
        return cp_pb2.LoginResponseRoundTwo(b=True, error="")

def serve():
    port = os.getenv("SERVER_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cp_pb2_grpc.add_CpServicer_to_server(Victor(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info(f'Server started, listening on {port}\n')
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
