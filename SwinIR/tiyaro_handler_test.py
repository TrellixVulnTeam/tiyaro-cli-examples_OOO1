import json
import sys
import traceback

from tiyaro.sdk.test_utils.util import get_input_json, get_pretrained_file_path, save_test_input_if_schema, save_test_output_if_schema

from tiyaro_handler.model_handler import TiyaroHandler

if __name__ == "__main__":
    try:
        file_path = get_pretrained_file_path(sys.argv[1])
        input_json = get_input_json(sys.argv[2])
        output_file = sys.argv[3]
        if output_file == "None":
            output_file = None

        ob = TiyaroHandler()
        ob.setup_model(pretrained_file_path=file_path)
        ob.declare_schema()
        print(f'INIT - Done')

        save_test_input_if_schema(ob, input_json)

        print(f'INFERENCE - Started')
        output = ob.infer(json_input=input_json)
        print(f'INFERENCE - Done')

        save_test_output_if_schema(ob, output)

        print('OUTPUT STARTS - {}'.format('*'*50))
        print(json.dumps(output, indent=4, sort_keys=True))
        print('OUTPUT ENDS - {}'.format('*'*50))

        if output_file:
            if not ".json" in output_file:
                output_file += ".json"
            with open(output_file, 'w+', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f'ERROR - {e}')
        traceback.print_exc()
        exit(-1)
