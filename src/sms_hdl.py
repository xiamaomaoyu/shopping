import nexmo


MY_NUMBER = "LITTLEGEND"
sms_client = nexmo.Client(key='7e1f7b82', secret='azy57VbJwb0XgPTs')


def send_customer(phone_number, text):
    return send_message(MY_NUMBER, phone_number, text)


def send_message(send_from, send_to, text):
    send_to = process_phone_number(send_to)
    result = sms_client.send_message({'from': send_from, 'to': send_to, 'text': text})
    print(result)
    return result


def process_phone_number(send_to):
    if send_to[0] == '4':
        return '+61' + send_to
    elif send_to[0] == '1':
        return '+86' + send_to
    else:
        return send_to