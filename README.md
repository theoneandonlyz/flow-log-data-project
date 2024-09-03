# Flow Log Data Processor

## Description

This program parses through a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a CSV file with three columns: `dstport`, `protocol`, and `tag`. The tag is chosen according to the `dstport` and `protocol` provided.

## More Information

- The inputted flow log data must be in a plain text (ASCII) file. Details on the flow log format can be found here: [AWS VPC Flow Log Records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html).
- Only the default log format and version 2 are supported.
- The output generates 3 separate csv files. One contains the lookup table. The second contains the count of matches for each tag, with two columns: `Tag`, `Count`. The third contains the count of matches for each port/protocol combination with three columns: `Port`, `Protocol`, `Count`.
- To test the integrity of the code, lines 116-120 in the log_file_processor.py can be uncommented to add an additional 10,000 mappings to the lookup table.

### Format

The format for the flow log data is assumed to be in the following order according to https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html  :

**Ordering of Flow Log Data:**
- **<Version>**: Log version
- **<Account ID>**: AWS account ID
- **<Interface ID>**: Network interface ID
- **<Source IP Address>**: IP address of the source
- **<Destination IP Address>**: IP address of the destination
- **<Source Port>**: Port used by the source
- **<Destination Port>**: Port used by the destination
- **<Protocol>**: Protocol number
- **<Number of Packets>**: Number of packets transferred
- **<Number of Bytes>**: Number of bytes transferred
- **<Start Time>**: Start time of the log entry
- **<End Time>**: End time of the log entry
- **<Action>**: Action taken (e.g., ACCEPT, REJECT)
- **<Log-status>**: Status of the log entry

## References

- To find the protocol name based on the `<Protocol>` field, the official assignment of protocol numbers from the IANA website is referenced through a CSV file. [IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
- To assign the appropriate tag name based on the `<Destination Port>` and `<Protocol>` combination, the "Service Name and Transport Protocol Port Number Registry" from the IANA website is referenced through a CSV file. [IANA Service Names and Port Numbers](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=3)

## Running the Program

Run the command in terminal:

python ./log_file_processor.py

The user will be prompted to input the file name, the extension of the file (i.e. '.txt', '.csv') should be included. In the folder, there is a default file called 'flow_logs.txt' with sample flow log data. If the user does not input anything or inputs an invalid file name, the default file 'flow_logs.txt' will be parsed through.

## Future work

For future improvements and refinements, the below may be considered:
- Refactor repetetitive file operations to improve extracting file handling logic
- Improve Error handling by adding more checks in the case of missing files or other errors
- Optimize data writing to reduce frequency of file openings and use more efficient data structures
