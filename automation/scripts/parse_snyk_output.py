import argparse
import json
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--snyk-output-file',
                        required=True,
                        help='path to the raw snyk output file')

    parser.add_argument('--resulting-file',
                        required=True,
                        help='path to the file in which parsed output should be saved')

    args = parser.parse_args()

    return args


def parse_output(path_to_raw_output: str, path_to_result_file: str) -> int:
    with open(path_to_raw_output, 'r', encoding='utf-8') as output_file:
        data = output_file.read()
        json_start = data.find('{')
        json_end = data.rfind('}') + 1
        parsed = json.loads(data[json_start:json_end])

    print(parsed.get('ok'))
    print(type(parsed.get('ok')))
    if parsed.get('ok', 0):
        return 1

    with open(path_to_result_file, 'w', encoding='utf-8') as result_file:
        json.dump(parsed, result_file)

    return 0


if __name__ == '__main__':
    input_args = parse_arguments()
    sys.exit(parse_output(input_args.snyk_output_file, input_args.resulting_file))
