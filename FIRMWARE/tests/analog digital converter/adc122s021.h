#ifndef ADC122S021_H
#define ADC122S021_H

#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "stdio.h"

uint16_t ADC122S021_ReadADC(spi_inst_t* spi, const uint cs, bool channel);
double ADC122S021_GetVoltage(spi_inst_t* spi, const uint cs, bool channel);

#endif