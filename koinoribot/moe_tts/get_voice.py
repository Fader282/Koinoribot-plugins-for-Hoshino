import json

import websockets

import hoshino


async def get_tts_voice(fx_index, msg, speaker):
    """
    fx_index: 数字
    msg: 字符串
    speaker: 字符串
    """
    post = f'"fn_index":{fx_index},"data":["' + msg + '","' + speaker + '",1,false],"session_hash":"6rxpn4f4kix"'
    data = "{" + post + "}"
    hoshino.logger.info(data)
    hash_post = '{session_hash:"6rxpn4f4kix",fn_index:' + fx_index + '}'

    async with websockets.connect('wss://skytnt-moe-tts.hf.space/queue/join') as websocket:
        # data = {"fn_index": fx_index, "data": [msg, speaker, 1, false]}
        await websocket.send(str(data))
        while True:
            response = await websocket.recv()
            resp_dict = json.loads(response)
            # hoshino.logger.info(response)
            if resp_dict['msg'] == 'send_data':
                await websocket.send(str(data))
            if resp_dict['msg'] == 'process_completed':
                tts_b64 = resp_dict['output']['data'][1]
                tts_b64 = tts_b64.strip('data:audio/wav;base64,')
                record_cqcode = f'[CQ:record,file=base64://{tts_b64}]'
                break
        return record_cqcode