/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 5 OCT 2020                              */
/* Version: V01                                      */
/*****************************************************/
# ifndef 	UART_INTERFACE_H
#define     UART_INTERFACE_H

void MUART_voidInit(void);
void MUART_voidTransmit(u8 Data[]);
u8 MUART_u8Receive(void);


#endif