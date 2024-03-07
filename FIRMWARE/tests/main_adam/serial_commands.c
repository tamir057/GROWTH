#include "serial_commands.h"

uint8_t parse_commands(uint8_t* buf, command_attributes* command_list, uint8_t len) {

    uint8_t command[32] = "";
    uint8_t arguments[64] = "";

    uint8_t* token = strtok(buf, ":");
    uint8_t ctr = 0;
    while (token != NULL) {

        ctr++;

        switch(ctr) {
        case 1:
            strcpy(command, token);
            break;
        case 2:
            strcpy(arguments, token);
            break;
        default:
            break;
        }

        token = strtok(NULL, ":");
    }

    if (ctr != 1 && ctr != 2) {
        printf("%u parameters found, only 1 or 2 allowed\n\n", ctr);
        return 1;
    }

    for (uint8_t cmd=0; cmd<len; cmd++) {

        if (strcmp(command, command_list[cmd].command) == 0) {

            if (command_list[cmd].n_args == 0) {
                break;
            }

            uint8_t* arg_token = strtok(arguments, ",");

            uint8_t arg_ctr = 0;
            while (arg_token != NULL) {
                arg_ctr++;
                printf("Argument found -> %s\n", arg_token);
                arg_token = strtok(NULL, ",");
            }
            printf("\n");

            if (arg_ctr != command_list[cmd].n_args) {
                printf("Argument count does not match expected value\n\n");
                return 2;
            }

            break;

        } else if (cmd == len-1) {

            printf("Specified command not found in internal library\n\n");
            return 3;
        }
    }

    return 0;
}