#ifndef TCA9534_H
#define TCA9534_H

#include "pico/stdlib.h"
#include "hardware/i2c.h"

#define SET_BIT(pos, reg) (reg |= (1 << pos))
#define CLR_BIT(pos, reg) (reg &= ~(1 << pos))

// DEFINES

// device I2C parameters
#define TCA9534_ADDR			(0x20)	    // need to left shift - bit 0 is for R/W
#define TCA9534_TMOUT			(250)       // milliseconds
#define TCA9534_GOOD			(1)

// IO states
#define LOW						(0x00)
#define HIGH					(0x01)

// port definitions
#define TCA9534_INPUT_REG		(0x00) // reads the current states of the IO pins (works in both in/out modes)
#define TCA9534_OUTPUT_REG		(0x01) // stores desired states of IO pins (only drives IO state in output mode)
#define TCA9534_POL_INV_REG		(0x02) // invert polarity of pins defined as inputs in config register (1-> inv, 0-> no-inv)
#define TCA9534_CONFIG_REG		(0x03) // sets the direction of the IO pins (1-> input, 0-> output)

// TYPEDEFS
typedef struct {

	uint8_t output_config;			// sets initial state of outputs
	uint8_t polarity_config;		// sets input polarity inversion (only applies to inputs)
	uint8_t io_config;				// sets direction of IO pins

	// I2C_HandleTypeDef* hi2c;		// I2C port

} TCA9534_ConfigTypeDef;

// FUNCTION PROTOTYPES
uint8_t TCA9534_ReadReg(i2c_inst_t* i2c, const uint addr, uint8_t reg, uint8_t len);
void TCA9534_WriteReg(i2c_inst_t* i2c, const uint addr, uint8_t reg, uint8_t val);

// uint8_t TCA9534_Init(TCA9534_ConfigTypeDef* setup); // configures the IO expander with desired properties
// void TCA9534_Write_All_Outputs(I2C_HandleTypeDef* hi2c, uint8_t outputs); // sets the states of all outputs simultaneously
// void TCA9534_Write_Output(I2C_HandleTypeDef* hi2c, uint8_t idx, uint8_t state); // sets the state of an individual output
// uint8_t TCA9534_Read_All_Inputs(I2C_HandleTypeDef* hi2c); // reads the current state of all GPIO pins
// uint8_t TCA9534_Read_Input(I2C_HandleTypeDef* hi2c, uint8_t idx); // reads the current state of desired IO pin

#endif