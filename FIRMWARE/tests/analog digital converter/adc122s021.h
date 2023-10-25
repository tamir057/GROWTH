#ifndef ADC122S021_H
#define ADC122S021_H

#include "pico/stdlib.h"
#include "hardware/spi.h"

#define ADC_INPUT1      (0x00)
#define ADC_INPUT2      (0x01 << 3)

uint16_t ADC122021_ReadADC(spi_inst_t* spi, const uint cs, bool channel);

#endif