# OpenVPN Connection Monitor

The **OpenVPN Connection Monitor** is a Python script designed to parse OpenVPN status data, track user connections, and generate an output file with connection statistics.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Overview

The OpenVPN Connection Monitor consists of a set of Python scripts that work together to achieve the following tasks:

1. **Parsing OpenVPN Status**: The script utilizes the `OpenVpnParser` class to parse OpenVPN status data from a specified input file.

2. **Storing Connections**: It uses the `ConnectionDB` class to manage connection information and store data in a database.

3. **Generating Connection Statistics**: The script generates connection statistics for each user, including daily, weekly, and monthly data usage. These statistics are then formatted and written to an output file.

4. **Multithreading**: The script utilizes threading to concurrently manage both data parsing and output generation.

## Installation

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/yourusername/openvpn-connection-monitor.git

## Usage

1.) Configure the script by modifying the config.py file to set your desired input and output file names, as well as other parameters.
2.) Run the main script to start monitoring OpenVPN connections and generating statistics.
    ```bash
    python main.py

The script will run indefinitely, parsing OpenVPN status data at specified intervals and generating the connection statistics output.

## Configuration

You can customize the behavior of the OpenVPN Connection Monitor by modifying the parameters in the `config.py` file. Here are some of the configurable options:

- `dbFileName`: Name of the connection database file.
- `inputFileName`: Name of the input file containing OpenVPN status data.
- `outputFileName`: Name of the output file for connection statistics.
- `inputFileParseInterval`: Interval (in seconds) at which the script should parse OpenVPN status data.
- `outputFileWriteInterval`: Interval (in seconds) at which the script should generate and update the output file.

## License

This project is licensed under the MIT License.
