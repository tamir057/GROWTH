#include "tca9534.h"

// read specified register in the TCA9534 IO expander
uint8_t TCA9534_ReadReg(i2c_inst_t* i2c, uint8_t reg) {

    uint8_t reg_val;

    i2c_write_blocking(i2c, TCA9534_ADDR, &reg, 1, true);       // address is always 1 byte long
    i2c_read_blocking(i2c, TCA9534_ADDR, &reg_val, 1, false);   // registers are all 1 byte long

    return reg_val;
}

// write byte to the specified register of the TCA9534 IO expander
void TCA9534_WriteReg(i2c_inst_t* i2c, uint8_t reg, uint8_t val) {

    uint8_t data[2] = {reg, val};
    i2c_write_blocking(i2c, TCA9534_ADDR, (uint8_t*) &data, 2, false);

}