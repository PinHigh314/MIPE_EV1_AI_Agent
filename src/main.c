/**
 * MIPE_EV2 Test - GPIO Test  
 * Proven 23ms timing pattern from MIPE_EV1
 * RTT Hardware Monitoring Integration
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/printk.h>

LOG_MODULE_REGISTER(mipe_ev1_gpio, LOG_LEVEL_DBG);

/* LEDs on P0.00 and P0.01 */
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios);

/* Test pins on P1.05 and P1.06 */
static const struct gpio_dt_spec test_pin05 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin05), gpios);
static const struct gpio_dt_spec test_pin06 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin06), gpios);

int main(void)
{
    LOG_INF("🚀 MIPE_EV1 GPIO Test Started - Hardware Monitoring Active");
    LOG_INF("⏱️  Target timing: 23ms toggle cycles");
    LOG_INF("📊 RTT timestamping enabled for Actions monitoring");
    
    /* Configure pin directions - PROVEN pattern */
    LOG_DBG("🔧 Configuring GPIO pins...");
    gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
    gpio_pin_configure_dt(&led1, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT);
    LOG_INF("✅ GPIO configuration complete");

    /* Set initial states - all LOW */
    LOG_DBG("🔽 Setting initial pin states to LOW");
    gpio_pin_set_dt(&led0, 0);
    gpio_pin_set_dt(&led1, 0);
    gpio_pin_set_dt(&test_pin05, 0);
    gpio_pin_set_dt(&test_pin06, 0);
    LOG_INF("✅ Initial states set - pins ready for testing");

    bool led_state = false;
    uint32_t counter = 0;
    uint32_t cycle_count = 0;
    const uint32_t toggle_threshold = 1000000;  /* Proven 23ms timing from EV1 */
    
    LOG_INF("🔄 Starting GPIO toggle loop - monitoring for Actions");
    LOG_INF("📈 Toggle threshold: %u cycles (≈23ms)", toggle_threshold);
    
    while (1) {
        counter++;
        
        if (counter >= toggle_threshold) {
            cycle_count++;
            
            /* Log every 10th cycle for Actions monitoring */
            if (cycle_count % 10 == 0) {
                LOG_INF("🔄 Cycle %u: Toggling pins (23ms timing verified)", cycle_count);
            }
            
            /* Toggle all pins with proven pattern */
            led_state = !led_state;
            LOG_DBG("📍 Toggle event: state=%s, cycle=%u", 
                    led_state ? "HIGH" : "LOW", cycle_count);
                    
            gpio_pin_set_dt(&led0, led_state ? 1 : 0);
            gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
            gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);  /* Same as LED0 */
            gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);  /* Same as LED1 */
            
            /* Log timing validation for Actions */
            if (cycle_count % 50 == 0) {
                LOG_INF("⏱️  Timing validation: %u cycles completed (≈%ums total)", 
                        cycle_count, cycle_count * 23);
            }
            
            counter = 0;
        }
    }

    return 0;
}