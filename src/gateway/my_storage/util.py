import pika, json



def upload(f, fs, channel, access):
    '''
    This function uploads a file in MongoDB using gridfs and
    send a message in RabiitMQ channel 
    f - file
    fs - gridfs instance
    channel - RabbitMQ channel
    access - user's access 
    '''
    try:
        fid = fs.put(f)
    except Exception as err:
        return f"Internal MongoDB server error {err}", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs.delete(fid)
        return f"Internal RabbitMQ server error {err}", 500
