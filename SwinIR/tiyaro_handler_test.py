import json
import sys
import traceback

from tiyaro.sdk.test_utils.util import get_input_json, get_pretrained_file_path, save_test_input, save_test_output

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
        ob.declareSchema()
        print(f'INIT - Done')

        if ob.inputSchema:
            ob.inputSchema().load(input_json)
            save_test_input(input_json)
            print(f'INPUT - Validation Done')
        else:
            print('WARN - Input schema not defined')

        print(f'INFERENCE - Started')
        output = ob.infer(json_input=input_json)
        print(f'INFERENCE - Done')

        if ob.outputSchema:
            output = ob.outputSchema().load(output)
            save_test_output(output)
            print(f'OUTPUT - Validation Done')
        else:
            print('WARN - Output schema not defined')

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
