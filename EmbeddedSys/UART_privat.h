/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 5 OCT 2020                              */
/* Version: V01                                      */
/*****************************************************/
# ifndef 	UART_PRIVATE_H
#define     UART_PRIVATE_H

typedef struct
{
	volatile u32 UARTDR;         // UART Data
	volatile u32 UARTRSR; 		 // UART Receive Status/Error Clear
	volatile u32 UARTFR ;        // UART Flag
	volatile u32 UARTILPR;       // not used
	volatile u32 UARTIBRD;
	volatile u32 UARTFBRD;
	volatile u32 UARTLCRH;
	volatile u32 UARTCTL;        // Control register Enable and disable uart
	volatile u32 UARTIFLS;		 // not used
	volatile u32 UARTIM;		 // not used
	volatile u32 UARTRIS;		 // read only not used
	volatile u32 UARTMIS;        // read only not used
	volatile u32 UARTICR;        // interrupt clear write 1 to clear
	volatile u32 UARTDMACTL;     // not used
	volatile u32 UART9BITADDR;   // not used
	volatile u32 UART9BITAMASK;  // not used
	volatile u32 UARTPP;         // not used 
	volatile u32 UARTCC;         // For clock choice
}MUART_Type;


/*UART BASE Address */
#define  BASE_ADDRESS_UART0 	  ((volatile MUART_Type *) 0x4000C000)	
#define  BASE_ADDRESS_UART1 	  ((volatile MUART_Type *) 0x4000D000)
#define  BASE_ADDRESS_UART2 	  ((volatile MUART_Type *) 0x4000E000)
#define  BASE_ADDRESS_UART3 	  ((volatile MUART_Type *) 0x4000F000)
#define  BASE_ADDRESS_UART4 	  ((volatile MUART_Type *) 0x40010000)
#define  BASE_ADDRESS_UART5 	  ((volatile MUART_Type *) 0x40011000)
#define  BASE_ADDRESS_UART6 	  ((volatile MUART_Type *) 0x40012000)
#define  BASE_ADDRESS_UART7 	  ((volatile MUART_Type *) 0x40013000)
/*Buad Rate */
#define  UART_9600		    0
#define  UART_115200		1

/* UART clock */
#define  SYSTEM_CLOCK       0
#define  PIOSC	        	1
/*UART Number */
#define  UART0				0
#define  UART1				1
#define  UART2				2
#define  UART3 				3
#define  UART4 				4
#define  UART5 				5
#define  UART6				6
#define  UART7				7

#define RCGCUART  *((u32*)0x400FE618)
#define RCGCGPIO  *((u32*)0x400FE608)

 

#endif
