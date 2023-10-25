#ifndef PINOUT_H
#define PINOUT_H

// I2C Pin Definitions
#define I2C_SCL             ((const uint) 1)
#define I2C_SDA             ((const uint) 0)

// SPI Pin Definitions
#define SPI_SCLK            ((const uint) 2)
#define SPI_MOSI            ((const uint) 3)
#define SPI_MISO            ((const uint) 4)
#define ADC_CS              ((const uint) 5)

// GPIO Pin Definitions/Functionality

#define MCU_LED             ((const uint) 6)

#define Z_MOTOR_EN          ((const uint) 29)
#define Z_MOTOR_M2          ((const uint) 28)
#define Z_MOTOR_M1          ((const uint) 27)
#define Z_MOTOR_M0          ((const uint) 26)
#define Z_MOTOR_DIR         ((const uint) 25)
#define Z_MOTOR_STEP        ((const uint) 24)

#define X_MOTOR_EN          ((const uint) 21)
#define X_MOTOR_M2          ((const uint) 20)
#define X_MOTOR_M1          ((const uint) 19)
#define X_MOTOR_M0          ((const uint) 18)
#define X_MOTOR_DIR         ((const uint) 17)
#define X_MOTOR_STEP        ((const uint) 16)

#define GPIO1               ((const uint) 8)
#define GPIO2               ((const uint) 9)
#define GPIO3               ((const uint) 10)
#define GPIO4               ((const uint) 11)
#define GPIO5               ((const uint) 12)
#define GPIO6               ((const uint) 13)
#define GPIO7               ((const uint) 14)
#define GPIO8               ((const uint) 15)
#define GPIO9               ((const uint) 22)
#define GPIO10              ((const uint) 23)

// IO Expander Pin Positions
#define PPUMP_1             ((const uint8_t) 7)
#define PPUMP_2             ((const uint8_t) 6)
#define PPUMP_3             ((const uint8_t) 5)
#define PPUMP_4             ((const uint8_t) 4)

#define GRW_LIGHT_1         ((const uint8_t) 3)
#define GRW_LIGHT_2         ((const uint8_t) 2)
#define GRW_LIGHT_3         ((const uint8_t) 1)
#define EXPANDER_LED        ((const uint8_t) 0)

#endif