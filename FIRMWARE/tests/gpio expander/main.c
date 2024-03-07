#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include "tca9534.h"

int main() {

    // INITIALIZATION CODE
    
    const uint i2c0_sda_pin = 0;
    const uint i2c0_scl_pin = 1;

    i2c_inst_t* i2c0_port = i2c0;

    stdio_init_all();

    i2c_init(i2c0_port, 100*1000);

    gpio_set_function(i2c0_sda_pin, GPIO_FUNC_I2C);
    gpio_set_function(i2c0_scl_pin, GPIO_FUNC_I2C);

    TCA9534_WriteReg(i2c0_port, TCA9534_ADDR, TCA9534_CONFIG_REG, 0x00);

    while(true) {

        TCA9534_WriteReg(i2c0_port, TCA9534_ADDR, TCA9534_OUTPUT_REG, 0xFF);
        sleep_ms(500);
        TCA9534_WriteReg(i2c0_port, TCA9534_ADDR, TCA9534_OUTPUT_REG, 0x00);
        sleep_ms(500);

    }

    return 0;
}