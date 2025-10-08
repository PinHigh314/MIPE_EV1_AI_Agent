/**
 * MIPE_EV1 - SPI LSM6DSO32 Test + GPIO
 * Real hardware test with logic analyzer capture
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(mipe_ev1, LOG_LEVEL_INF);

/* LEDs on P0.00 and P0.01 */
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios);

/* Test pins on P1.05 and P1.06 */
static const struct gpio_dt_spec test_pin05 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin05), gpios);
static const struct gpio_dt_spec test_pin06 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin06), gpios);

/* LSM6DSO32 SPI Configuration */
#define LSM6DSO32_WHO_AM_I_REG 0x0F
#define LSM6DSO32_WHO_AM_I_VAL 0x6C

/* SPI Configuration for LSM6DSO32 */
static struct spi_config lsm6dso32_spi_cfg = {
	.frequency = 1000000,  /* 1MHz - Conservative start */
	.operation = SPI_WORD_SET(8) | SPI_TRANSFER_MSB | SPI_OP_MODE_MASTER,
	.slave = 0,
	.cs = {
		.gpio = {
			.port = DEVICE_DT_GET(DT_NODELABEL(gpio0)),
			.pin = 16,  /* P2.05 = pin 16 */
			.dt_flags = GPIO_ACTIVE_LOW
		},
		.delay = 1  /* CS setup time */
	}
};

static const struct device *spi_dev;

int lsm6dso32_read_reg(uint8_t reg, uint8_t *data)
{
	uint8_t tx_buffer[2] = {reg | 0x80, 0x00}; /* Read bit set */
	uint8_t rx_buffer[2] = {0};
	
	struct spi_buf tx_buf = {.buf = tx_buffer, .len = 2};
	struct spi_buf_set tx_bufs = {.buffers = &tx_buf, .count = 1};
	
	struct spi_buf rx_buf = {.buf = rx_buffer, .len = 2};
	struct spi_buf_set rx_bufs = {.buffers = &rx_buf, .count = 1};
	
	int ret = spi_transceive(spi_dev, &lsm6dso32_spi_cfg, &tx_bufs, &rx_bufs);
	if (ret == 0) {
		*data = rx_buffer[1];
		LOG_INF("SPI Read: reg=0x%02X, data=0x%02X", reg, *data);
	} else {
		LOG_ERR("SPI Read failed: %d", ret);
	}
	return ret;
}

int init_lsm6dso32(void)
{
	/* Get SPI device - using SPI00 which is enabled in device tree */
	spi_dev = DEVICE_DT_GET(DT_NODELABEL(spi00));
	if (!device_is_ready(spi_dev)) {
		LOG_ERR("SPI device not ready");
		return -1;
	}
	
	LOG_INF("SPI device ready, testing LSM6DSO32...");
	
	/* Test WHO_AM_I register */
	uint8_t who_am_i;
	int ret = lsm6dso32_read_reg(LSM6DSO32_WHO_AM_I_REG, &who_am_i);
	if (ret == 0) {
		LOG_INF("LSM6DSO32 WHO_AM_I: 0x%02X (expected 0x%02X)", 
		        who_am_i, LSM6DSO32_WHO_AM_I_VAL);
		if (who_am_i == LSM6DSO32_WHO_AM_I_VAL) {
			LOG_INF("🎉 LSM6DSO32 sensor detected successfully!");
			return 0;
		} else {
			LOG_WRN("Unexpected WHO_AM_I value");
		}
	}
	
	LOG_ERR("LSM6DSO32 communication failed");
	return -1;
}

int main(void)
{
	LOG_INF("🚀 MIPE_EV1 Real Hardware SPI Test Starting!");
	
	/* Configure all pins as outputs, start LOW */
	gpio_pin_configure_dt(&led0, GPIO_OUTPUT_LOW);         /* P0.00 LED - Start OFF */
	gpio_pin_configure_dt(&led1, GPIO_OUTPUT_LOW);         /* P0.01 LED - Start OFF */
	gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT_LOW);   /* P1.05 - Start LOW */
	gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT_LOW);   /* P1.06 - Start LOW */

	/* Initialize LSM6DSO32 sensor */
	LOG_INF("📊 Initializing LSM6DSO32 sensor via SPI...");
	int spi_result = init_lsm6dso32();
	
	bool led_state = false;
	int test_count = 0;

	/* Main loop - LED flashing + periodic SPI tests */
	while (1) {
		/* Toggle LEDs every 200ms */
		led_state = !led_state;
		gpio_pin_set_dt(&led0, led_state ? 1 : 0);
		gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
		
		/* Copy LED0 behavior to P1.05 for scope measurement */
		gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);  /* Same as LED0 */
		
		/* P1.06 gets opposite pattern for comparison */
		gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);  /* Same as LED1 */
		
		/* Every 10 cycles (2 seconds), test SPI communication */
		if (++test_count >= 10) {
			test_count = 0;
			LOG_INF("🧪 Testing SPI communication (cycle %d)...", test_count);
			
			uint8_t who_am_i;
			int ret = lsm6dso32_read_reg(LSM6DSO32_WHO_AM_I_REG, &who_am_i);
			if (ret == 0 && who_am_i == LSM6DSO32_WHO_AM_I_VAL) {
				LOG_INF("✅ SPI communication working! WHO_AM_I=0x%02X", who_am_i);
				/* Flash LED0 rapidly 3 times to indicate success */
				for (int i = 0; i < 6; i++) {
					gpio_pin_toggle_dt(&led0);
					k_msleep(50);
				}
			} else {
				LOG_ERR("❌ SPI communication failed, WHO_AM_I=0x%02X", who_am_i);
			}
		}
		
		/* Sleep for stable timing */
		k_msleep(200);
	}

	return 0;
}
