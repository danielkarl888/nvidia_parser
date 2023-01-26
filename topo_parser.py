# Created by Daniel Karl
import sys
import re


def parse_topology(file):
    current_switch = ""
    # Initialize an empty dictionary to store the topology
    topology = {}
    b = False
    # Open the topology file
    with open(file, "r") as f2:
        lines = f2.readlines()
        for i, line in enumerate(lines):
            if "Switch" in line:
                b = True
                current_switch = re.search(r'"(.*?)"', line).group(1).replace("S-", "")
                continue
            if "caguid" in line:
                print(f"Parsing progress: 100%")
                break
            if b:
                try:
                    split_string = line.split('\t')
                    # Extract the switch number and name
                    switch_number = split_string[0].strip('[]')
                    switch_name = split_string[1].split('[')[0].replace('"', '')
                    topology[(switch_name, switch_number)] = current_switch
                    # Print the progress
                    print(f"Parsing progress: {i / len(lines) * 100:.2f}%")
                except:
                    continue
    parse_to_file(topology)


def parse_to_file(topo):
    with open("parse.txt", "w") as file:
        for key, value in sorted(topo.items(), key=lambda item: item[1]):
            file.write(f"{key[0]}, {key[1]}, {value}\n")


def print_topo(topo):
    for key, value in topo.items():
        # print(f"father: {value}, name: {key[0].strip('-S').strip('-H')}, port: {key[1]}")
        if key[0][0] == "S":
            print("Switch\n")
        else:
            print("Host\n")
        print(
            f"sysimgguid=0x{key[0].strip('-S').strip('-H')}\nPort_id:"
            f"={key[0].strip('S-').strip('H-')}\nConnected to switch:switchguid=0x{value.strip()}({value.strip()})"
            f", port ={key[1]}\n\n")


# Press the green button in the gutter to run the script.
def from_parse_file_to_dict():
    try:
        topology = {}
        with open("parse.txt", "r") as f:
            for line in f:
                elements = line.strip().split(",")
                key = (elements[0], elements[1])
                value = elements[2]
                topology[key] = value
            return topology
    except FileNotFoundError:
        print("Please run the command topo_parser –f topofile.topo before trying to print")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse_topology(sys.argv[2])
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == "-h":
                print("You should run the command 'topo_parser –f topofile.topo' to parse your file.\n"
                      "After it, a parsed file named parse.txt is being created. with the format a,b,c for each line\n"
                      "when 'a' is device, 'b' is the port and 'c' is the switch that the device is connected to.\n"
                      "If you want to print the parsed topology - run the command 'topo_parser –p'.\n"
                      "(You must parse the file before printing)")
            else:
                if sys.argv[1] == "-p":
                    topo2 = from_parse_file_to_dict()
                    if topo2 is not None:
                        print_topo(topo2)
