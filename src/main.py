import os
import argparse
import logging

import pandas

logging.basicConfig(level=logging.INFO)

DF_NAMES = ["timestamp", "header_bytes", "client_ip",
            "http_resp_code", "resp_size_bytes", "http_req_meth",
            "url", "username", "access_dest_ip", "res_type"]


def main(args):
    """Analyze the content of log files.

    Args:
        args: Populated namespace with arguments.
    """
    input_files = read_input(args.input_path)
    parsed_data = parse_squid_log_file(input_files)

    if args.most_freq_ip:
        most_freq_ip = calculate_most_freq_ip(parsed_data)
        print("Most frequent IP", most_freq_ip)
        save_output("Most frequent IP", most_freq_ip, args.output_path)

    if args.least_freq_ip:
        least_freq_ip = calculate_least_freq_ip(parsed_data)
        print("Least frequent IP", least_freq_ip)
        save_output("Least frequent IP", least_freq_ip, args.output_path)

    if args.least_freq_ip:
        events_sec = calculate_events_sec(parsed_data)
        print("Events per second", events_sec)
        save_output("Events per second", str(events_sec), args.output_path)

    if args.least_freq_ip:
        total_bytes = calculate_total_bytes(parsed_data)
        print("Total amount of bytes exchanged", total_bytes)
        save_output("Total amount of bytes exchanged", str(total_bytes), args.output_path)

    logging.info("Results saved to %s", args.output_path)


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
        logging.info("%s", os.path.abspath(fpath))
        if os.path.isfile(fpath):
            res.append(fpath)
        elif os.path.isdir(fpath):
            files = [os.path.join(fpath, f) for f in os.listdir(fpath)]
            res.extend(files)
        else:
            logging.error("Path does not exist: %s", fpath)
    if not res:
        exit()
    return res


def save_output(description, result, output):
    """Save operations result to output file.

    Args:
        description (str): Operations description.
        result (str): Operations result.
        output (str): Output path.
    """
    with open(output, 'a') as fout:
        fout.write(f"{description}: {result}\n")


def parse_squid_log_file(files):
    """Read log files into pandas Dataframe.

    Args:
        files (list):

    Returns:
        dataframe: Log files pandas Dataframe format
    """
    df = pandas.DataFrame()
    for file_path in files:
        logging.info("Processing: %s", file_path)
        new_df = pandas.read_csv(file_path,
                                 delim_whitespace=True,
                                 engine="python",
                                 on_bad_lines="warn",
                                 header=None,
                                 names=DF_NAMES)
        df = pandas.concat([df, new_df], axis=0)
    return df


def calculate_most_freq_ip(df):
    """Calculate most frequent IP.

    Args:
        df: Pandas Dataframe.

    Returns:
        str: Most frequent IP.
    """
    return df['client_ip'].value_counts().index[0]


def calculate_least_freq_ip(df):
    """Calculate least frequent IP.

    Args:
        df: Pandas Dataframe.

    Returns:
        str: Least frequent IP.
    """
    return df['client_ip'].value_counts().index[-1]


def calculate_events_sec(df):
    """Average number of EPS in 24-hour period.

    Assumption: Logs are from 24-hour period

    Source: https://www.ccexpert.us/security-monitoring/determining-your-events-per-second.html
    Step 1 Gather the logs for one or more 24-hour periods.
    Step 2 Count the number of lines in the file or files.
    Step 3 Divide the number of lines by the number of 24-hour periods the file contains.
    Step 4 Divide this number by 86,400.

    Args:
        df: Pandas Dataframe.

    Returns:
        int: Events per second.
    """
    df["time"] = pandas.to_datetime(df["timestamp"], unit='s')
    df["time"].dt.to_period("D")
    number_of_groups = df.groupby(pandas.Grouper(key='time', axis=0, freq='D')).ngroups
    return df.shape[0] / number_of_groups / 86400


def calculate_total_bytes(df):
    """Calculate total amount of bytes exchanged.

    Args:
        df: Pandas Dataframe.

    Returns:
        int: Total amount of bytes exchanged.
    """
    df_sum = df[["header_bytes", "resp_size_bytes"]].sum()
    return df_sum["header_bytes"] + df_sum["resp_size_bytes"]


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
        required=True,
        help="Path to one or more plain text files, or a directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output_path",
        required=True,
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
