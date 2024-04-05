/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "data.h"
//~ #include "Data.h"
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <crypto_aead.h>
// #include <api.h>

#define ENCRYPT(a, b, c, d, e, f, g, h, i) crypto_aead_encrypt(a, b, c, d, e, f, g, h, i)
#define DECRYPT(a, b, c, d, e, f, g, h, i) crypto_aead_decrypt(a, b, c, d, e, f, g, h, i)

#define MSG_SIZE INPUT_SIZE*4

// #define POWER_CONS

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef hlpuart1;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_LPUART1_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* DWT (Data Watchpoint and Trace) registers, only exists on ARM Cortex with a DWT unit */
#define KIN1_DWT_CONTROL (*((volatile uint32_t *)0xE0001000))
/*!< DWT Control register */
#define KIN1_DWT_CYCCNTENA_BIT (1UL << 0)
/*!< CYCCNTENA bit in DWT_CONTROL register */
#define KIN1_DWT_CYCCNT (*((volatile uint32_t *)0xE0001004))
/*!< DWT Cycle Counter register */
#define KIN1_DEMCR (*((volatile uint32_t *)0xE000EDFC))
/*!< DEMCR: Debug Exception and Monitor Control Register */
#define KIN1_LAR (*((volatile uint32_t *)0xE0001FB0))
/*!< lock access register */
#define KIN1_TRCENA_BIT (1UL << 24)
/*!< Trace enable bit in DEMCR register */

#define KIN1_InitCycleCounter() \
  KIN1_DEMCR |= KIN1_TRCENA_BIT
/*!< TRCENA: Enable trace and debug block DEMCR (Debug Exception and Monitor Control Register */

#define KIN1_EnableLockAccess() \
  KIN1_LAR = 0xC5ACCE55;
/*!< lock access */

#define KIN1_ResetCycleCounter() \
  KIN1_DWT_CYCCNT = 0
/*!< Reset cycle counter */

#define KIN1_EnableCycleCounter() \
  KIN1_DWT_CONTROL |= KIN1_DWT_CYCCNTENA_BIT
/*!< Enable cycle counter */

#define KIN1_DisableCycleCounter() \
  KIN1_DWT_CONTROL &= ~KIN1_DWT_CYCCNTENA_BIT
/*!< Disable cycle counter */

#define KIN1_GetCycleCounter() \
  KIN1_DWT_CYCCNT
/*!< Read cycle counter register */

void send_serial(uint8_t *data, int size)
{

  HAL_UART_Transmit(&hlpuart1, data, size, HAL_MAX_DELAY);
}

void receive_serial(uint8_t *data, int size)
{

  HAL_UART_Receive(&hlpuart1, data, size, HAL_MAX_DELAY);
}

// Sync controller and wrapper
void sync()
{
  float zero = 0.0;
  float one = 1.0;

  // Sync
  while (1)
  {
    float rec_zero;
    receive_serial(&rec_zero, 4);

    if (!(rec_zero == (float)0))
    {
      send_serial(&one, 4);
      continue;
    }
    else
    {
      send_serial(&zero, 4);
      break;
    }
  }
}

uint32_t cycles_e, cycles_d;  /* number of cycles */
int freq;

void send_app_runtime(float c)
{
  float time, discard;

  // Sync with script
  send_serial(&time, 4);
  sync();
  receive_serial(&discard, 4);

  // Send app runtime (seconds)
  time = (float)c / freq; 
  send_serial(&time, 4);
}

void send_runtime(float c)
{
  float time, discard = 0;
  time = (float)c / freq; 

  // Sync with script
  sync();
  receive_serial(&discard, 4);
  send_serial(&time, 4);
}

void send_output(double output)
{
  float discard = 0;

  // Sync with script
  sync();
  receive_serial(&discard, 4);
  send_serial(&output, 8);
}

void send_checksum(uint32_t output)
{
  float discard = 0;

  // Sync with script
  sync();
  receive_serial(&discard, 4);
  send_serial(&output, 1);
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_LPUART1_UART_Init();
  /* USER CODE BEGIN 2 */
  KIN1_InitCycleCounter(); /* enable DWT hardware */
  KIN1_EnableLockAccess();
  freq = HAL_RCC_GetSysClockFreq();
  
  #if CRYPTO_KEYBYTES==16
    volatile unsigned char key[CRYPTO_KEYBYTES] = {0xDEADBEEF, 0x01234567, 0x89ABCDEF, 0xDEADBEEF};
#else 
    volatile unsigned char  key[CRYPTO_KEYBYTES] = {0xDEADBEEF, 0x01234567, 0x89ABCDEF, 0xDEADBEEF, 0xDEADBEEF, 0x01234567, 0x89ABCDEF, 0xDEADBEEF};
#endif
  volatile unsigned char nonce[CRYPTO_NPUBBYTES] = {0};
  // volatile unsigned char key[CRYPTO_KEYBYTES] = {0};
  volatile uint64_t msglen = MSG_SIZE;// sizeof(text) / sizeof(unsigned char);
  volatile unsigned long long ctlen = 0;
  volatile unsigned char ct[MSG_SIZE + CRYPTO_ABYTES] = {0};
  volatile unsigned long long adlen = 0;

  // decrypt check
  volatile unsigned char dt[MSG_SIZE] = {0};

  // Declare pointers
  volatile unsigned char *c;
  volatile unsigned long long *clen;
  volatile uint64_t *mlen;
  volatile unsigned char *k, *npub;
  volatile unsigned char *m;

  // Initialise pointers
  k = key;
  npub = nonce;
  clen = &ctlen;
  m = text;
  c = ct;
  mlen=&msglen;
	
  double output;
  uint8_t sum = 0;
  HAL_GPIO_TogglePin (LD2_GPIO_Port, LD2_Pin);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	#ifdef POWER_CONS
		
		for(int i=0;i<N_LOOP;i++)
			output = ENCRYPT(c, clen, m, msglen, NULL, adlen, NULL, npub, k);
      HAL_GPIO_TogglePin (LD2_GPIO_Port, LD2_Pin);
		HAL_Delay(1000);


	#else

		// Sync before app execution
		sync();

		KIN1_ResetCycleCounter();  /* reset cycle counter */
		KIN1_EnableCycleCounter(); /* start counting */

		// Start application
    // Encryption
		output = ENCRYPT(c, clen, m, msglen, NULL, adlen, NULL, npub, k);
		cycles_e = KIN1_GetCycleCounter(); /* get cycle counter */
    
    // Decryption
    KIN1_ResetCycleCounter();  /* reset cycle counter */
		KIN1_EnableCycleCounter(); /* start counting */
    // DECRYPT(dm, mlen, NULL, c, ctlen, NULL, adlen, npub, k);
    double decrypt = DECRYPT(dt, mlen, NULL, c, *clen, NULL, adlen, npub, k);

    cycles_d = KIN1_GetCycleCounter(); /* get cycle counter */

    // Checksum
    int check_ind[5] = {29, 774, 226, 973, 2079};
    for (int i=0;i<5;i++){
      sum += (dt[check_ind[i]*4] - text[check_ind[i]]);
    }

		send_app_runtime(cycles_e);
    send_runtime(cycles_d);
		// Send output
		send_output(decrypt);
    send_checksum(sum);
		//~ HAL_Delay(1000);
	
	#endif
  }
   KIN1_DisableCycleCounter();
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  if (HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_MSI;
  RCC_OscInitStruct.MSIState = RCC_MSI_ON;
  RCC_OscInitStruct.MSICalibrationValue = 0;
  RCC_OscInitStruct.MSIClockRange = RCC_MSIRANGE_11;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_MSI;
  RCC_OscInitStruct.PLL.PLLM = 3;
  RCC_OscInitStruct.PLL.PLLN = 20;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief LPUART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_LPUART1_UART_Init(void)
{

  /* USER CODE BEGIN LPUART1_Init 0 */

  /* USER CODE END LPUART1_Init 0 */

  /* USER CODE BEGIN LPUART1_Init 1 */

  /* USER CODE END LPUART1_Init 1 */
  hlpuart1.Instance = LPUART1;
  hlpuart1.Init.BaudRate = 115200;
  hlpuart1.Init.WordLength = UART_WORDLENGTH_8B;
  hlpuart1.Init.StopBits = UART_STOPBITS_1;
  hlpuart1.Init.Parity = UART_PARITY_NONE;
  hlpuart1.Init.Mode = UART_MODE_TX_RX;
  hlpuart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  hlpuart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  hlpuart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&hlpuart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN LPUART1_Init 2 */

  /* USER CODE END LPUART1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOG_CLK_ENABLE();
  HAL_PWREx_EnableVddIO2();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, LD3_Pin|LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOG, USB_PowerSwitchOn_Pin|SMPS_V1_Pin|SMPS_EN_Pin|SMPS_SW_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LD3_Pin LD2_Pin */
  GPIO_InitStruct.Pin = LD3_Pin|LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : USB_OverCurrent_Pin SMPS_PG_Pin */
  GPIO_InitStruct.Pin = USB_OverCurrent_Pin|SMPS_PG_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

  /*Configure GPIO pins : USB_PowerSwitchOn_Pin SMPS_V1_Pin SMPS_EN_Pin SMPS_SW_Pin */
  GPIO_InitStruct.Pin = USB_PowerSwitchOn_Pin|SMPS_V1_Pin|SMPS_EN_Pin|SMPS_SW_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);

  /*Configure GPIO pins : USB_SOF_Pin USB_ID_Pin USB_DM_Pin USB_DP_Pin */
  GPIO_InitStruct.Pin = USB_SOF_Pin|USB_ID_Pin|USB_DM_Pin|USB_DP_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF10_OTG_FS;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
