import redis
import argparse
import json

def process(msg, bad_guys):
    message = json.loads(msg)
    from_ac = message['metadata']['from']
    to_ac = message['metadata']['to']
    amount = message['amount']

    if to_ac in bad_guys and amount > 0:
        message['metadata']['from'] = to_ac
        message['metadata']['to'] = from_ac

    return json.dumps(message)

def main(bad_guys):
    redis_con = redis.Redis(host="localhost", port=6379, db=0)
    pubsub = redis_con.pubsub()
    pubsub.subscribe('transactions')

    for i in pubsub.listen():
        if i['type'] == 'message':
            new_msg = process(i['data'], bad_guys)
            print(new_msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--mal_accounts', type=str, required=True, help='comma-separated list of bad guys account numbers')
    argguments = parser.parse_args()
    b_guys = argguments.mal_accounts.split(',')

    main(b_guys)