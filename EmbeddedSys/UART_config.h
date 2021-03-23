/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 5 OCT 2020                              */
/* Version: V01                                      */
/*****************************************************/
# ifndef 	UART_CONFIG_H
#define     UART_CONFIG_H
/* options :
			SYSTEM_CLOCK
			PIOSC
			*/
#define UART_CLOCK  SYSTEM_CLOCK
/* options :
			UART_9600
			UART_115200 */
#define BUAD_RATE  UART_9600

/* options :
			BASE_ADDRESS_UART0
            BASE_ADDRESS_UART1
            BASE_ADDRESS_UART2
            BASE_ADDRESS_UART3
            BASE_ADDRESS_UART4
            BASE_ADDRESS_UART5
            BASE_ADDRESS_UART6
            BASE_ADDRESS_UART7
*/
#define MUART BASE_ADDRESS_UART0

/* options :
			UART0
            UART1
            UART2
            UART3
            UART4
            UART5
            UART6
            UART7
*/
#define UART_NUMBER UART0



#endif