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
	/* Configure all pins as outputs, start LOW */
	gpio_pin_configure_dt(&led0, GPIO_OUTPUT_LOW);         /* P0.00 LED - Start OFF */
	gpio_pin_configure_dt(&led1, GPIO_OUTPUT_LOW);         /* P0.01 LED - Start OFF */
	gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT_LOW);   /* P1.05 - Start LOW */
	gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT_LOW);   /* P1.06 - Start LOW */

	bool led_state = false;

	/* Timer-based control loop - BACK TO SLEEP MODE FOR POWER STABILITY */
	while (1) {
		/* Toggle LEDs every 200ms */
		led_state = !led_state;
		gpio_pin_set_dt(&led0, led_state ? 1 : 0);
		gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
		
		/* Copy LED0 behavior to P1.05 for scope measurement */
		gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);  /* Same as LED0 */
		
		/* P1.06 gets opposite pattern for comparison */
		gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);  /* Same as LED1 */
		
		/* Back to k_msleep for power stability - CPU sleeps, VDD stable */
		k_msleep(200);  /* ~6 seconds actual, but stable VDD */
	}

	return 0;
}
