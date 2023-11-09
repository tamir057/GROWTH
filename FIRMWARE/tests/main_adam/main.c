#include "pico/stdlib.h"
#include "stdio.h"
// #include "pico/multicore.h"
// #include "hardware/irq.h"
// #include "pico/stdio_usb.h"
// #include "tusb.h"

#include "pinout.h"
// #include "adc122s021.h"
// #include "serial_commands.h"
// #include "stepper_motor.h"
// #include "tca9534.h"

// defines
// #define SPI_BIT_RATE 1000000

// global variables
// uint8_t usb_rx_buf[256];
// uint8_t usb_tx_buf[256];

// command_attributes valid_commands[] = {{MOVE_MOTOR_CMD, 3},
//                                        {STOP_MOTOR_CMD, 1},
//                                        {MOVE_CONT_CMD, 2},
//                                        {READ_SENSOR_CMD, 1},
//                                        {PUMP_ON_CMD, 1},
//                                        {PUMP_OFF_CMD, 1},
//                                        {LIGHT_ON_CMD, 1},
//                                        {LIGHT_OFF_CMD, 1},
//                                        {LED_ON_CMD, 0},
//                                        {LED_OFF_CMD, 0}};

// global flag variables
// bool kill_x_motor_flag = false;
// bool kill_y_motor_flag = false;

// interrupt handler for limit switches
// void limit_switch_triggered(uint gpio, uint32_t events) {

//     return;
// }

// core1 main code
// void core1_entry() {

//     uint8_t byte;
//     uint8_t counter = 0;
//     while(1) {

//         while(tud_cdc_available()) {

//             byte = getchar_timeout_us(1);

//             if (byte == '\n') {

//                 usb_rx_buf[counter] = '\0';

//                 printf("MESSAGE OF SIZE (%i) BYTES RECEIVED\n", counter);
//                 printf("MESSAGE: %s\n\n", usb_rx_buf);

//                 // uint8_t rtn = parse_commands(usb_rx_buf, valid_commands, 10);

//                 counter = 0;

//             } else {

//                 usb_rx_buf[counter] = byte;
//                 counter++;
//             }    
//         }

//     }

//     return;
// }

// core0 main code
int main() {

    // configure USB serial communication
    stdio_init_all();

    // configure SPI port
    // spi_inst_t* spi_port = spi0;

    // spi_init(spi_port, SPI_BIT_RATE);
    // spi_set_format(spi_port, 8, 1, 1, SPI_MSB_FIRST);

    // gpio_set_function(SPI_SCLK, GPIO_FUNC_SPI);
    // gpio_set_function(SPI_MOSI, GPIO_FUNC_SPI);
    // gpio_set_function(SPI_MISO, GPIO_FUNC_SPI);

    // gpio_init(ADC_CS);
    // gpio_set_dir(ADC_CS, GPIO_OUT);
    // gpio_put(ADC_CS, true);

    // configure I2C port
    // i2c_inst_t* i2c_port = i2c0;

    // i2c_init(i2c_port, 100*1000);

    // gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    // gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);

    // configure GPIO pins
    gpio_init(MCU_LED);
    gpio_set_function(MCU_LED, GPIO_OUT);

    // gpio_init(GPIO1);
    // gpio_set_dir(GPIO1, GPIO_IN);
    // gpio_set_pulls(GPIO1, false, false);

    // gpio_init(GPIO2);
    // gpio_set_dir(GPIO2, GPIO_IN);
    // gpio_set_pulls(GPIO2, false, false);

    // gpio_init(GPIO3);
    // gpio_set_dir(GPIO3, GPIO_IN);
    // gpio_set_pulls(GPIO3, false, false);

    // gpio_init(GPIO4);
    // gpio_set_dir(GPIO4, GPIO_IN);
    // gpio_set_pulls(GPIO4, false, false);

    // initialize peripheral devices (if necessary)
    // TCA9534_WriteReg(i2c_port, TCA9534_CONFIG_REG, 0x00); // configure pins as outputs

    // stepper_config x_axis_motor = {X_MOTOR_STEP, X_MOTOR_DIR, X_MOTOR_M0,
    //                                X_MOTOR_M1, X_MOTOR_M2, X_MOTOR_EN,
    //                                6400, 6400, 200, 150};
    // init_motor(&x_axis_motor, 1, USTEP_1_32);

    // stepper_config z_axis_motor = {Z_MOTOR_STEP, Z_MOTOR_DIR, Z_MOTOR_M1,
    //                                Z_MOTOR_M1, Z_MOTOR_M2, Z_MOTOR_EN,
    //                                1000, 1000, 400, 300};
    // init_motor(&z_axis_motor, 1, USTEP_1_32);

    // TCA9534_WriteReg(i2c_port, TCA9534_OUTPUT_REG, 0x00);

    // enable interrupts
    // gpio_set_irq_enabled_with_callback(GPIO1, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);
    // gpio_set_irq_enabled_with_callback(GPIO2, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);    
    // gpio_set_irq_enabled_with_callback(GPIO3, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);
    // gpio_set_irq_enabled_with_callback(GPIO4, GPIO_IRQ_EDGE_RISE, true, &limit_switch_triggered);

    // blink MCU LED to indicate that MCU is starting up
    for (int i=0; i<10; i++) {
        gpio_put(MCU_LED, true);
        sleep_ms(10);
        gpio_put(MCU_LED, false);
        sleep_ms(90);
    }

    // launch core1 code execution
    // multicore_launch_core1(core1_entry);

    // main loop
    while(1) {
        sleep_ms(1000);
    }

    return 0;
}