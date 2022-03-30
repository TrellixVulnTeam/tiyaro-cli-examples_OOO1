from tiyaro_handler.model_handler import TiyaroHandler

import os
import sys
import json
import yaml
import traceback
import validators
import requests
import shutil

FROM_CONFIG = 'from-config'
MODEL_CONFIG = './tiyaro_handler/model_manifest.yml'
FIELD = 'pretrained_model_url'


def get_pretrained_file_path(x):
    def local_file(x, err_msg):
        if os.path.isfile(x):
            return x
        else:
            raise ValueError(err_msg)

    if x == FROM_CONFIG:
        # read from yaml
        # if url, download to /tmp and return path
        # if local path, return path
        with open(MODEL_CONFIG, 'r') as file:
            contents = yaml.safe_load(file)
            value = contents[FIELD]
            if (
                (value is None) 
                or (not isinstance(value, str)) 
                or (not value.strip())
                ):
                raise ValueError(f'Please set a valid model {FIELD} in {MODEL_CONFIG}')
            if validators.url(value):
                r = requests.get(value, stream = True)
                file_path = '/tmp/pre_trained.pth'
                print(f'DOWNLOADING - pretrained file to {file_path} from: {value}')
                if r.status_code == 200:
                    with open(file_path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    print('DOWNLOAD - Done')
                    return file_path
                else:
                    raise RuntimeError(f'Unable to download pretrained file from: {value}')
            else:
                return local_file(x, 'Expected valid local file path or url')

    return local_file(x, 'Expected valid local file path')

def get_input_json(x):
    if os.path.isfile(x):
        with open(x, 'r') as f:
            return json.load(f)
    if isinstance(x, str):
        return json.loads(x)
    
    raise ValueError('Expected Valid JSON input string or file path')

if __name__ == "__main__":
    try:
        file_path = get_pretrained_file_path(sys.argv[1])
        input_json = get_input_json(sys.argv[2])

        ob = TiyaroHandler()
        ob.setup_model(pretrained_file_path=file_path)
        ob.declareSchema()
        print(f'INIT - Done')

        ob.inputSchema().load(input_json)
        print(f'INPUT - Validation Done')

        print(f'INFERENCE - Started')
        output = ob.infer(json_input=input_json)
        print(f'INFERENCE - Done')

        output = ob.outputSchema().load(output)
        print(f'OUTPUT - Validation Done')
        print('OUTPUT STARTS - {}'.format('*'*50))
        print(json.dumps(output, indent=4, sort_keys=True))
        print('OUTPUT ENDS - {}'.format('*'*50))

    except Exception as e:
        print(f'ERROR - {e}')
        traceback.print_exc()
        exit(-1)
