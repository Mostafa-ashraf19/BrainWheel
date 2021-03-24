/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 5 OCT 2020                              */
/* Version: V01                                      */
/*****************************************************/
#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "UART_interface.h"
#include "UART_privat.h"
#include "UART_config.h"

void MUART_voidInit(void)
{
    /*
	Disable UART
	*/
	CLR_BIT( MUART -> UARTCTL , 0);
	
		
		
	/*
	buad rate = 115200--> BRR = 0x
	*/
	#if BUAD_RATE == UART_115200
	/* 
	integer portion of the buad rate using this equation 20,000,000 / (16 * 115,200) = 10.8507 assuming clock is 20 MHZ 
	*/
		MUART -> UARTIBRD = 0xA ;
		MUART -> UARTFBRD = 54;
	/*
		Data length of 8 bits
		One stop bit
		No parity
		FIFOs disabled
		No interrupts
	*/
		MUART -> UARTLCRH = 0x00000060 ;
	
	/*
		Enable Rx
		Enable TX
	*/
    SET_BIT(MUART -> UARTCTL , 8 );
	SET_BIT(MUART -> UARTCTL , 9 );	
	/*
		Enable UART
	*/
	SET_BIT( MUART -> UARTCTL ,0 );
	
	/* 
		Clear Flag and status Register 
	*/
	MUART -> UARTRSR = 0 ;
    MUART -> UARTFR  = 0 ;

	#endif 
}
void MUART_voidTransmit(u8 Data[])
{
	u8 i = 0 ; 
	while (Data[i] != '\0')
	{
		MUART -> UARTDR = Data[i] ;
		/*
			Wait till transmission complete 
		*/
		while (GET_BIT(MUART -> UARTFR , 7) == 0 ); 
		i++; 
	}
}
u8 MUART_u8Receive(void)
{
	/* 
		Wait till Receive complete 
	*/
	while (GET_BIT(MUART -> UARTFR , 6) == 0 );
	/*
		And with 0xFF to make sure that the returned data is u8
	*/
    return (0xFF & (MUART -> UARTDR) ) ;
}
