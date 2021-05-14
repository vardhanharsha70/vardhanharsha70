import json
import stomp
import os
import ssl


def lambda_handler(event=None, context=None):
    conn = None
    try:
        conn = stomp.Connection([(os.environ.get('ACTIVE_MQ_HOST'), os.environ.get('ACTIVE_MQ_PORT'))])
        conn.set_ssl(for_hosts=[(os.environ.get('ACTIVE_MQ_HOST'), os.environ.get('ACTIVE_MQ_PORT'))],
                     ssl_version=ssl.PROTOCOL_TLS)
        conn.connect(os.environ.get('ACTIVE_MQ_USERNAME'), os.environ.get('ACTIVE_MQ_PASSWORD'), wait=True)
        conn.send(type='ResourceOperationJsonMessage',
                  body=' {"mediaType":"application/json", "payload":"{\"name\":\"Nicholas Daver\"}"} ',
                  content_type='application/json', destination='/queue/test')
        print('====MESSAGE SENT====')
        return {
            'statusCode': 200,
            'body': json.dumps('ACTIVE MQ TEST SUCCESS')
        }
    except Exception as error:
        print('====ERROR====', error)
    finally:
        if conn is not None:
            conn.disconnect()
        print('====CLOSE CONNECTION===')
