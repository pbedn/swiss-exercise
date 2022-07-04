import os
import argparse
import logging


def main(args):
    """"Main function"""

    input_files = read_input(args.input_path)

    result_dct = dict()

    if args.most_freq_ip:
        result_dct["most_freq_ip"] = calculate_most_freq_ip()
        print("Most frequent IP", result_dct["most_freq_ip"])

    if args.least_freq_ip:
        result_dct["least_freq_ip"] = calculate_least_freq_ip()
        print("Least frequent IP", result_dct["least_freq_ip"])

    if args.least_freq_ip:
        result_dct["events_sec"] = calculate_events_sec()
        print("Events per second", result_dct["events_sec"])

    if args.least_freq_ip:
        result_dct["total_bytes"] = calculate_total_bytes()
        print("Total amount of bytes exchanged", result_dct["total_bytes"])

    if result_dct:
        save_output(result_dct, args.output_path)
        print(f"Output saved to {args.output_path}")


def read_input(input_path):
    """Read input paths and return list of files.

    Assumption: path is absolute or relative to script location.

    Args:
        input_path (list): Path to one or more plain text files, or a directory.

    Returns:
        list: List of files.
    """
    res = []
    for fpath in input_path:
        if os.path.isfile(fpath):
            res.append(fpath)
        elif os.path.isdir(fpath):
            files = os.listdir(fpath)
            res.extend(files)
        else:
            logging.error("Path does not exist: %s", fpath)
    return res


def save_output(dct, output):
    """Save operations result to output file.

    Args:
        dct (dict): Operations result.
        output (str): Output path.
    """
    logging.info("Results saved to %s", output)


def calculate_most_freq_ip():
    """Calculate most frequent IP."""
    return 0


def calculate_least_freq_ip():
    """Calculate least frequent IP."""
    return 0


def calculate_events_sec():
    """Calculate events per second."""
    return 0


def calculate_total_bytes():
    """Calculate total amount of bytes exchanged."""
    return 0


def get_argument_parser():
    """Definition of cli arguments"""

    msg = "Command line tool to analyze the content of log files"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        dest="input_path",
        nargs='+',
        help="Path to one or more plain text files, or a directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output_path",
        help="Path to a file to save output in plain text JSON format",
    )
    parser.add_argument(
        "-m", "--most_freq_ip", action="store_true", dest="most_freq_ip", help="Most frequent IP"
    )
    parser.add_argument(
        "-l", "--least_freq_ip", action="store_true", dest="least_freq_ip", help="Least frequent IP"
    )
    parser.add_argument(
        "-e", "--events_sec", action="store_true", dest="events_sec", help="Events per second"
    )
    parser.add_argument(
        "-t", "--total_bytes", action="store_true", dest="total_bytes", help="Total amount of bytes exchanged"
    )
    return parser


if __name__ == '__main__':
    argument_parser = get_argument_parser()
    main(argument_parser.parse_args())
