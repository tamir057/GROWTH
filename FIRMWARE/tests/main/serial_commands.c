#include "serial_commands.h"

// reads a string and determines whether a valid command is contained within the string
// if a valid command is contained, arguments are extracted and stored
/*
ARGS
    buf          -> string to be parsed
    command_list -> list of valid commands
    len          -> length of command_list
    queue        -> destination of command and arguments (if found)

RETURN
    -4  -> specified command not in list of valid options
    -3  -> incorrect number of arguments passed
    -2  -> at least one argument was of an invalid type (i.e not a 32-bit integer)
    -1  -> the input string contained more than 1 ":" separator (hence invalid)
    0   -> command successfully parsed, low priority command
    1   -> command successfully parsed, high priority command
*/

int8_t parse_command(uint8_t* buf, command_attributes* command_list, uint8_t len, command_queue_entry* queue) {

    uint8_t command[32] = "";
    uint8_t arguments[64] = "";
    bool priority = false;


    // split the input string (buf) into separate strings using ":" delimiter

    uint8_t* token = strtok(buf, ":");
    uint8_t ctr = 0;
    while (token != NULL) {

        ctr++;

        switch(ctr) {
        case 1:
            strcpy(command, token);     // command string will be first matched token
            break;
        case 2:
            strcpy(arguments, token);   // arguments are contained within the second matched string
            break;
        default:
            break;
        }

        token = strtok(NULL, ":");
    }

    // if the input string was separated into more than 2 segments, error occurred

    if (ctr > 2) {
        //printf("%u parameters found, only 1 or 2 allowed\n\n", ctr);
        return -1;
    }

    // search through all valid commands to attempt to find match

    for (uint8_t cmd=0; cmd<len; cmd++) {

        // if the command matches in the list
        if (strcmp(command, command_list[cmd].command) == 0) {

            // copy command string and priority into the queue entry
            priority = command_list[cmd].priority;
            strcpy((char*) queue->command, (char*) command);

            // no need to search for arguments if command requires none
            if (command_list[cmd].n_args == 0) {
                break;
            }

            // parse arguments, separated by comma
            uint8_t* arg_token = strtok(arguments, ",");
            uint8_t arg_ctr = 0;
            while (arg_token != NULL) {

                arg_ctr++;
                
                // arguments must be uint32_t
                if (sscanf(arg_token, "%lu", &(queue->args[arg_ctr-1])) != 1) {
                    //printf("Argument not a valid 32-bit unsigned integer\n\n");
                    return -2;
                };

                arg_token = strtok(NULL, ",");
            }

            //printf("\n");

            if (arg_ctr != command_list[cmd].n_args) {
                //printf("Argument count does not match expected value\n\n");
                return -3;
            }

            break;

        } else if (cmd == len-1) {

            //printf("Specified command not found in internal library\n\n");
            return -4;
        }
    }

    // if reached here, command parse success -> return priority level

    int8_t rtn = (int8_t) priority;
    return rtn;
}