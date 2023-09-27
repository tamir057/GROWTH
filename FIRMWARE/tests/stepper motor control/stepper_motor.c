#include "stepper_motor.h"

void init_motor(stepper_config* cfg, uint8_t en, uint8_t ustep) {

    const uint* pin_ptr = &(cfg->step_pin);
    for (int i=0; i<6; i++) {

        gpio_init(*pin_ptr);
        gpio_set_dir(*pin_ptr, GPIO_OUT);
        pin_ptr++;
        
    }

    gpio_put(cfg->en_pin, (en>0)?(true):(false));
    gpio_put(cfg->step_pin, false);
    gpio_put(cfg->dir_pin, false);

    ustep &= (0x07);    // bit mask XXXXXbbb -> three LSB
    gpio_put(cfg->M0_pin, (ustep>>0 & 0x01)?(true):(false));
    gpio_put(cfg->M1_pin, (ustep>>1 & 0x01)?(true):(false));
    gpio_put(cfg->M2_pin, (ustep>>2 & 0x01)?(true):(false));

}

void execute_steps(uint32_t steps, uint8_t dir, stepper_config* cfg) {

    double delay_mag = (cfg->Delay_max - cfg->Delay_min) / 2.0;
    double delay_offset = (cfg->Delay_max + cfg->Delay_min) / 2.0;
    uint32_t delay;

    if (dir > 0) {
        gpio_put(cfg->dir_pin, true);
    } else {
        gpio_put(cfg->dir_pin, false);
    }

    if (steps <= (cfg->S_accel + cfg->S_decel)) {

        double correction_factor = 0.3;
        double new_ampl_min = (1-correction_factor) * (delay_mag * cos(M_PI * (double) (steps) / (2 * (double) cfg->S_accel)) + delay_offset) + correction_factor;
        double new_mag = (cfg->Delay_max - new_ampl_min) / 2.0;
        double new_offset = (cfg->Delay_max + new_ampl_min) / 2.0;

        for (uint32_t S=0; S<steps; S++) {
            delay = (uint32_t) (new_mag * cos(2 * M_PI * (double) S / (double) steps) + new_offset) / 2;

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

    } else {

        // acceleration stage
        for (uint32_t A=0; A<cfg->S_accel; A++) {
            delay = (uint32_t) ((delay_mag * cos(M_PI * ((double) A) / ((double) cfg->S_accel)) + delay_offset) / 2);

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

        // constant velo. stage
        delay = cfg->Delay_min / 2;
        for (uint32_t K=0; K<(steps - (cfg->S_accel + cfg->S_decel)); K++) {
            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

        // deceleration stage
        for (uint32_t D=0; D<cfg->S_decel; D++) {
            delay = (uint32_t) ((delay_mag * cos(M_PI * ((double) (D + cfg->S_decel)) / ((double) cfg->S_decel)) + delay_offset) / 2);

            gpio_put(cfg->step_pin, true);
            sleep_us(delay);
            gpio_put(cfg->step_pin, false);
            sleep_us(delay);
        }

    }

}

void disable_motor(stepper_config* cfg) {
    gpio_put(cfg->en_pin, true);
}

void enable_motor(stepper_config* cfg) {
    gpio_put(cfg->en_pin, false);
}