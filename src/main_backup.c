/**
 * MIPE_EV1 - Timer Test
 * 200ms LED flashing + GPIO control
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
	/* Configure all pins as outputs using correct pattern */
	gpio_pin_configure_dt(&led0, GPIO_OUTPUT);         /* P0.00 LED */
	gpio_pin_configure_dt(&led1, GPIO_OUTPUT);         /* P0.01 LED */
	gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);   /* P1.05 */
	gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT);   /* P1.06 */
	
	/* Set initial states - all LOW */
	gpio_pin_set_dt(&led0, 0);         /* Start OFF */
	gpio_pin_set_dt(&led1, 0);         /* Start OFF */
	gpio_pin_set_dt(&test_pin05, 0);   /* Start LOW */
	gpio_pin_set_dt(&test_pin06, 0);   /* Start LOW */

	bool led_state = false;

	/* Busy-wait control loop - NO k_msleep for accurate timing */
	uint32_t counter = 0;
	const uint32_t toggle_threshold = 1000000;  /* Adjust for desired timing */
	
	while (1) {
		/* Increment counter for timing */
		counter++;
		
		/* Toggle every threshold cycles */
		if (counter >= toggle_threshold) {
			led_state = !led_state;
			gpio_pin_set_dt(&led0, led_state ? 1 : 0);
			gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
			
			/* Copy LED0 behavior to P1.05 for scope measurement */
			gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);  /* Same as LED0 */
			
			/* P1.06 gets opposite pattern for comparison */
			gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);  /* Same as LED1 */
			
			counter = 0;  /* Reset counter */
		}
	}

	return 0;
}
