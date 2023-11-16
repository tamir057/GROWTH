#include "pico/stdlib.h"
#include "stdio.h"
#include "tusb.h"
#include "pico/multicore.h"
#include "string.h"

#include "pinout.h"
#include "adc122s021.h"
#include "serial_commands.h"
#include "stepper_motor.h"
#include "tca9534.h"
#include "ds18b20.h"

// defines
#define SPI_BIT_RATE 1000000    // SPI clock speed
#define I2C_BIT_RATE 100000     // I2C clock speed

// global variables
i2c_inst_t* i2c_port = i2c0;
spi_inst_t* spi_port = spi0;

uint8_t usb_rx_buf[256];
uint8_t usb_tx_buf[256];

// list of all supported serial commands (including number of arguments and priority level)
command_attributes valid_commands[] = {{MOVE_MOTOR_CMD, 3, false},
                                       {STOP_MOTOR_CMD, 1, true},
                                       {MOVE_CONT_CMD, 2, false},
                                       {READ_SENSOR_CMD, 1, false},
                                       {PUMP_ON_CMD, 1, false},
                                       {PUMP_OFF_CMD, 1, false},
                                       {LIGHT_ON_CMD, 1, false},
                                       {LIGHT_OFF_CMD, 1, false},
                                       {LED_ON_CMD, 0, false},
                                       {LED_OFF_CMD, 0, false},
                                       {RETURN_CURRENT_POS_CMD, 1, false},
                                       {ZERO_POS_CMD, 1, false}};
#define NUM_COMMANDS (sizeof(valid_commands) / sizeof(valid_commands[0])) // number of commands in valid_commands

command_queue_entry normal_priority_cmd[1];     // buffer stores one command that executes when the current has finished
command_queue_entry immediate_priority_cmd[1];  // buffer stores one command that executes immediately

stepper_config x_axis_motor = {X_MOTOR_STEP, X_MOTOR_DIR, X_MOTOR_M0, 
                                   X_MOTOR_M1, X_MOTOR_M2, X_MOTOR_EN,
                                   6400, 6400, 200, 150};

stepper_config z_axis_motor = {Z_MOTOR_STEP, Z_MOTOR_DIR, Z_MOTOR_M0, 
                                   Z_MOTOR_M1, Z_MOTOR_M2, Z_MOTOR_EN,
                                   3200, 3200, 100, 75};

// global flag variables
struct flag_register {
    bool read_command;  // trigger to read a new command in the main loop
    bool kill_x_motor;  // immediately kill motor and indicate that calibration is needed
    bool kill_z_motor;
    bool stop_x_motor;  // immediately stop motor (no calibration needed)
    bool stop_z_motor;
    bool command_running;
} flags = {false, false, false, false, false, false};

// error handler function
void error_handler(uint32_t error_code) {

    while(1) {
        gpio_put(MCU_LED, true);
        sleep_ms(100);
        gpio_put(MCU_LED, false);
        sleep_ms(100);
        gpio_put(MCU_LED, true);
        sleep_ms(100);
        gpio_put(MCU_LED, false);
        sleep_ms(700);
    }
}

// interrupt handler for limit switches
void limit_switch_triggered(uint gpio, uint32_t events) {

    if (gpio == GPIO1) {
        disable_motor(&x_axis_motor);
        flags.kill_x_motor = true;
        printf("ACK:LIMIT_SWITCH_TRIGGERED:LEFT\n");

    } else if (gpio == GPIO2) {
        disable_motor(&x_axis_motor);
        flags.kill_x_motor = true;
        printf("ACK:LIMIT_SWITCH_TRIGGERED:RIGHT\n");

    } else if (gpio == GPIO3) {
        disable_motor(&z_axis_motor);
        flags.kill_z_motor = true;
        printf("ACK:LIMIT_SWITCH_TRIGGERED:UP\n");

    } else if (gpio == GPIO4) {
        disable_motor(&z_axis_motor);
        flags.kill_z_motor = true;
        printf("ACK:LIMIT_SWITCH_TRIGGERED:DOWN\n");
    }

    return;
}

// command handler
void command_handler(command_queue_entry* cmd) {

    uint8_t return_val[100] = ""; // string to store return values

    flags.command_running = true; // parse_command() will not read low priority commands while this is set

    if (strcmp(cmd->command, LED_ON_CMD) == 0) {;
        uint8_t reg_val = TCA9534_ReadReg(i2c_port, TCA9534_OUTPUT_REG);
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, SET_BIT(EXPANDER_LED, reg_val));

    } else if (strcmp(cmd->command, LED_OFF_CMD) == 0) {
        uint8_t reg_val = TCA9534_ReadReg(i2c_port, TCA9534_OUTPUT_REG);
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, CLR_BIT(EXPANDER_LED, reg_val));

    } else if (strcmp(cmd->command, PUMP_ON_CMD) == 0) {
        uint8_t reg_val = TCA9534_ReadReg(i2c_port, TCA9534_OUTPUT_REG);
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, SET_BIT((uint8_t) (7 - cmd->args[0]), reg_val));

    } else if (strcmp(cmd->command, PUMP_OFF_CMD) == 0) {
        uint8_t reg_val = TCA9534_ReadReg(i2c_port, TCA9534_OUTPUT_REG);
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, CLR_BIT((uint8_t) (7 - cmd->args[0]), reg_val));

    } else if (strcmp(cmd->command, MOVE_MOTOR_CMD) == 0 || strcmp(cmd->command, MOVE_CONT_CMD) == 0) {

        if (strcmp(cmd->command, MOVE_CONT_CMD) == 0) {
            cmd->args[2] = 1000000;
        }

        stepper_config* mtr;
        bool* kill_motor;
        bool* stop_motor;

        bool against_switch = false;

        switch(cmd->args[0]) {
        case 0:
            mtr = &x_axis_motor;
            kill_motor = &flags.kill_x_motor;
            stop_motor = &flags.stop_x_motor;

            if (gpio_get(GPIO1) == 1 && cmd->args[1] == 0) {
                //printf("X axis against left limit switch. Not moving\n"); // TODO: reformat
                against_switch = true;
            } else if (gpio_get(GPIO2) == 1 && cmd->args[1] == 1) {
                //printf("X axis against right limit switch. Not moving\n"); // TODO: reformat
                against_switch = true;
            }
            
            break;

        case 1:
            mtr = &z_axis_motor;
            kill_motor = &flags.kill_z_motor;
            stop_motor = &flags.stop_z_motor;

            if (gpio_get(GPIO3) == 1 && cmd->args[1] == 0) {
                //printf("Z axis against top limit switch. Not moving\n"); // TODO: reformat
                against_switch = true;
            } else if (gpio_get(GPIO4) == 1 && cmd->args[1] == 1) {
                //printf("Z axis against bottom limit switch. Not moving\n"); // TODO: reformat
                against_switch = true;
            }

            break;

        default:
            error_handler(0);
        }

        uint8_t dir = cmd->args[1];
        if (dir != 0 && dir != 1) {
            error_handler(0);
        }

        uint32_t steps = cmd->args[2];

        //printf("Args: %lu\n", steps);


        if (!against_switch) {
            execute_steps(steps, dir, mtr, kill_motor, stop_motor);
        }

    } else if (strcmp(cmd->command, RETURN_CURRENT_POS_CMD) == 0){
        // code for returning current position
        stepper_config* mtr;
        switch(cmd->args[0]){
        case 0:
            mtr = &x_axis_motor;
            break;
        case 1:
            mtr = &z_axis_motor;
            break;
        default:
            error_handler(0);
        }

        sprintf(return_val, "%ld", mtr->current_pos);
        // printf("CURRENT_POSITION:%ld\n", mtr->current_pos);

    } else if (strcmp(cmd->command, READ_SENSOR_CMD) == 0) {

        //double sensor_value;
        double temp;
        double pH_voltage;
        double pH_value;
        double offset = 0.0;
        double conductivity_voltage;
        double conductivity_value;

        switch(cmd->args[0]) {
        case 0:
            // read from temp sensor
            temp = DS18B20_getTemperature(DS18B20_PIN);
            if (temp > -1000)
            {
                // if no error, take the value
                break;
            }
            else{
                // if there was an error, try again
                temp = DS18B20_getTemperature(DS18B20_PIN);
                // determine what to do if there is still an error
            }

            // print out the temperature value
            // printf("TEMP:%f\n", temp);
            sprintf(return_val, "%f", temp);
            break;

        case 1:
            // read from pH sensor
            pH_voltage = ADC122S021_GetVoltage(spi_port, ADC_CS, 0); // channel 0 is pH sensor
            pH_value = pH_reading(pH_voltage, offset);

            // print out the pH value
            // printf("PH:%f\n", pH_value);
            sprintf(return_val, "%f", pH_value);
            break;

        case 2:
            // read from conductivity sensor
            temp = DS18B20_getTemperature(DS18B20_PIN);
            conductivity_voltage = ADC122S021_GetVoltage(spi_port, ADC_CS, 1); // channel 1 is conductivity sensor
            conductivity_value = conductivity_reading(conductivity_voltage, temp);
            // maybe need to handle errors here a little bit
            
            // print out the conductivity value
            // printf("CONDUCTIVITY:%f\n", conductivity_value);
            sprintf(return_val, "%f", conductivity_value);
            break;

        default:
            error_handler(0);
        }

    } else if (strcmp(cmd->command, ZERO_POS_CMD) == 0){
        stepper_config* mtr;
        switch(cmd->args[0]){
        case 0:
            mtr = &x_axis_motor;
            break;
        case 1:
            mtr = &z_axis_motor;
            break;
        default:
            error_handler(0);
        }
        mtr->current_pos = 0;
        // printf("CURRENT_POS_ZEROED:\n");
    }

    if (strcmp(cmd->command, MOVE_CONT_CMD) != 0){
        printf("ACK:%s:%s\n", cmd->command, return_val);
    }
    flags.command_running = false;

}

// multi-core interrupt handlers
// void core0_interrupt_handler() {

//     // handle all immediate priority instructions

// }

// void core1_interrupt_handler() {

// }

// core1 main code
void core1_entry() {

    uint8_t byte;
    uint8_t counter = 0;
    while(1) {

        while(tud_cdc_available()) {

            byte = getchar_timeout_us(1);

            if (byte == '\n') {

                usb_rx_buf[counter] = '\0';

                //printf("MESSAGE_OF_SIZE_(%i)_BYTES_RECEIVED:\n", counter);
                //printf("MESSAGE:%s\n\n", usb_rx_buf);

                command_queue_entry tmp;
                int8_t rtn = parse_command(usb_rx_buf, valid_commands, NUM_COMMANDS, &tmp); // if adding new command, remember to change the len arg here
                if (!flags.command_running && rtn == 0) {

                    memcpy(normal_priority_cmd, &tmp, sizeof(command_queue_entry));
                    flags.read_command = true;

                } else if (rtn == 1) {

                    memcpy(immediate_priority_cmd, &tmp, sizeof(command_queue_entry));

                    if (strcmp(immediate_priority_cmd->command, STOP_MOTOR_CMD) == 0) {

                        if (immediate_priority_cmd->args[0] == 0) {
                            flags.stop_x_motor = true;
                        } else if (immediate_priority_cmd->args[0] == 1) {
                            flags.stop_z_motor = true;
                        }
                    }
                }

                counter = 0;

            } else {

                usb_rx_buf[counter] = byte;
                counter++;
            }    
        }

    }

    return;
}

// core0 main code
int main() {

    // configure USB serial communication;
    stdio_init_all();

    // configure SPI port
    spi_init(spi_port, SPI_BIT_RATE);
    spi_set_format(spi_port, 8, 1, 1, SPI_MSB_FIRST);

    gpio_set_function(SPI_SCLK, GPIO_FUNC_SPI);
    gpio_set_function(SPI_MOSI, GPIO_FUNC_SPI);
    gpio_set_function(SPI_MISO, GPIO_FUNC_SPI);

    gpio_init(ADC_CS);
    gpio_set_dir(ADC_CS, GPIO_OUT);
    gpio_put(ADC_CS, true);

    // configure I2C port
    i2c_init(i2c_port, I2C_BIT_RATE);

    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);

    // configure GPIO pin
    gpio_init(DS18B20_PIN);

    gpio_init(MCU_LED);
    gpio_set_dir(MCU_LED, GPIO_OUT);

    gpio_init(GPIO1);
    gpio_set_dir(GPIO1, GPIO_IN);
    gpio_set_pulls(GPIO1, false, false);

    gpio_init(GPIO2);
    gpio_set_dir(GPIO2, GPIO_IN);
    gpio_set_pulls(GPIO2, false, false);

    gpio_init(GPIO3);
    gpio_set_dir(GPIO3, GPIO_IN);
    gpio_set_pulls(GPIO3, false, false);

    gpio_init(GPIO4);
    gpio_set_dir(GPIO4, GPIO_IN);
    gpio_set_pulls(GPIO4, false, false);

    // initialize peripheral devices (if necessary)
    TCA9534_WriteReg(i2c_port, TCA9534_CONFIG_REG, 0x00); // configure pins as outputs

    init_motor(&x_axis_motor, 1, USTEP_1_32);
    init_motor(&z_axis_motor, 1, USTEP_1_8);

    TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, 0x00);

    // enable interrupts
    gpio_set_irq_enabled_with_callback(GPIO1, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);
    gpio_set_irq_enabled_with_callback(GPIO2, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);
    gpio_set_irq_enabled_with_callback(GPIO3, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);
    gpio_set_irq_enabled_with_callback(GPIO4, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);

    // blink MCU LED to indicate that MCU is starting up
    for (int i=0; i<10; i++) {
        gpio_put(MCU_LED, true);
        sleep_ms(10);
        gpio_put(MCU_LED, false);
        sleep_ms(90);
    }

    for (int i=0; i<10; i++) {
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, 0x01);
        sleep_ms(10);
        TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, 0x00);
        sleep_ms(90);
    }

    // launch core1 code execution
    multicore_launch_core1(core1_entry);

    // main core0 loop
    while(1) {

        // execute a command (when permitted to)
        if (flags.read_command) {
            command_handler(normal_priority_cmd);
            flags.read_command = false;
        }

    }

    return 0;
}