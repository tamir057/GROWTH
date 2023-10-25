#include "tca9534.h"

uint8_t TCA9534_ReadReg(i2c_inst_t* i2c, const uint addr, uint8_t reg, uint8_t len) {

    uint8_t reg_val;

    i2c_write_blocking(i2c, addr, &reg, 1, true);       // address is always 1 byte long
    i2c_read_blocking(i2c, addr, &reg_val, 1, false);   // registers are all 1 byte long

    return reg_val;
}

void TCA9534_WriteReg(i2c_inst_t* i2c, const uint addr, uint8_t reg, uint8_t val) {

    uint8_t data[2] = {reg, val};
    i2c_write_blocking(i2c, addr, &data, 2, false);

}