/**
 * MIPE_EV2 Test - GPIO Test  
 * Proven 23ms timing pattern from MIPE_EV1
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

/* LEDs on P0.00 and P0.01 */
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios);

/* Test pins on P1.05 and P1.06 */
static const struct gpio_dt_spec test_pin05 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin05), gpios);
static const struct gpio_dt_spec test_pin06 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin06), gpios);

int main(void)
{
    /* Configure pin directions - PROVEN pattern */
    gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
    gpio_pin_configure_dt(&led1, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT);

    /* Set initial states - all LOW */
    gpio_pin_set_dt(&led0, 0);
    gpio_pin_set_dt(&led1, 0);
    gpio_pin_set_dt(&test_pin05, 0);
    gpio_pin_set_dt(&test_pin06, 0);

    bool led_state = false;
    uint32_t counter = 0;
    const uint32_t toggle_threshold = 1000000;  /* Proven 23ms timing from EV1 */
    
    while (1) {
        counter++;
        
        if (counter >= toggle_threshold) {
            led_state = !led_state;
            gpio_pin_set_dt(&led0, led_state ? 1 : 0);
            gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
            gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);  /* Same as LED0 */
            gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);  /* Same as LED1 */
            counter = 0;
        }
    }

    return 0;
}