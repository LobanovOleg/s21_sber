import json
import redis
import random
import logging

def main():
    redis_con = redis.Redis(host="localhost", port=6379, db=0)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formater = logging.Formatter('%(message)s')
    handler.setFormatter(formater)
    logger.addHandler(handler)

    def generate():
        from_ac = str(random.randint(1000000000, 9999999999))
        to_ac = str(random.randint(1000000000, 9999999999))
        amount = random.randint(-10000, 10000)
        message = {
            "metadata": {
                "from": from_ac,
                "to": to_ac
            },
            "amount": amount
        }
        return json.dumps(message)
    
    for i in range(10):
        msg = generate()
        redis_con.publish('transactions', msg)
        logger.info(f"{msg}")
        redis_con.set(i, msg)

if __name__ == '__main__':
    main()