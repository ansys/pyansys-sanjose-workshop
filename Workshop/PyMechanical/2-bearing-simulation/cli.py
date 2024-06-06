import argparse
import json
import os
import typing

from lib import run

def parse_args():
    parser = argparse.ArgumentParser(description='cli-based bearing simulation command line')
    parser.add_argument('--model', help='Path to template model, "*.mechdb" and "*.mechdat" format are supported.')
    parser.add_argument('--input', help='Path to input json file containing AUTO_BEARING data.')
    parser.add_argument('--velocities', help='Comma delimited list of velocities to use in the rotational velocity boundary condition.')
    parser.add_argument('--solve-point', type=int, help='Solve point of the deformation result. It is a 1-based index of the velocities argument')
    parser.add_argument('--mode', type=int, help='Mode number, from 1 to 6')
    parser.add_argument('--output', help='Output image file path')

    args = parser.parse_args()
    return args

def split_velocity_arg(arg: str) -> typing.List[float]:
    try:
        velocities = [float(velocity) for velocity in arg.split(',')]
    except:
        raise Exception("ERROR: --velocities argument is not a comma delimited list of floating point values!")
    return velocities

def load_input_json(arg: str) -> typing.Dict[str, str]:
    if not os.path.isfile(arg):
        raise Exception("ERROR: the input given in the --input argument is not a file!")

    if not arg.endswith(".json"):
        raise Exception("ERROR: The given input (--input) is not a json file!")

    with open(arg) as f:
        try:
            json_data: typing.Dict[str, str] = json.load(f)
        except:
            raise Exception("ERROR: --input argument is not a valid json file!")
        def _expect_key(key: str):
            assert key in json_data, f"ERROR: --input json does not contain a {key} key!"
        [_expect_key(key) for key in ["k11", "k22", "k12", "k21", "c11", "c22", "c12", "c21"]]
    return json_data


def validate_args(args) -> typing.Tuple[typing.List[float], int, int, str, typing.Dict[str, str], str]:
    velocities: typing.List[float] = split_velocity_arg(args.velocities)
    mode: int = args.mode
    solve_point: int = args.solve_point
    model: str = args.model
    input_dict: typing.Dict[str, str] = load_input_json(args.input)
    output: str = args.output

    if mode < 1 or mode > 6:
        raise Exception("ERROR: --mode argument must be between 1 and 6, inclusive!")

    num_velocities = len(velocities)
    if num_velocities < 1:
        raise Exception("ERROR: must include at least one velocity in the --velocities argument!")

    if solve_point < 1:
        raise Exception("ERROR: solve point (via --solve-point) must be greater than zero!")

    if solve_point > num_velocities:
        raise Exception("ERROR: the given solve point (via --solve-point) is greater than the number of velocities!")

    if not os.path.isfile(model):
        raise Exception("ERROR: the model given in the --model argument is not a file!")

    if not (model.endswith(".mechdb") or model.endswith(".mechdat")):
        raise Exception("ERROR: The given model (--model) is not a valid file format. It must end in `.mechdb` or `.mechdat`!")

    output = os.path.abspath(output)

    return velocities, mode, solve_point, model, input_dict, output


if __name__ == "__main__":
    args = parse_args()
    velocities, mode, solve_point, model, input_dict, output = validate_args(args)
    run(velocities, mode, solve_point, model, input_dict, output)

