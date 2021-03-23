/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 1 Jannuary 2021                          */
/* Version: V02                                     */
/*****************************************************/
#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "GPIO_interface.h"
#include "GPIO_private.h"


 

					
	
void MGPIO_voidInit(u8 copy_u8PORT)
{
	switch(copy_u8PORT)
	{
		case GPIOA :
					/*Enable clock on port A */
					SET_BIT(RCGCGPIO,GPIOA);
					while(GET_BIT(PRGPIO,GPIOA)== 0);
					/* Unlock */
					GPIOA_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOA_AHP_CR   =0xff;
		
					GPIOA_AHP_AFSEL = 0x00;       // input output 
					GPIOA_AHP_AMSEL = 0x00;          // Analoge
					break;
		case GPIOB :
					/*Enable clock on port */
					SET_BIT(RCGCGPIO,GPIOB);
					while(GET_BIT(PRGPIO,GPIOB)== 0);
					/* Unlock */
					GPIOB_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOB_AHP_CR   =0xff;
		
					GPIOB_AHP_AFSEL = 0x00;       // input output 
					GPIOB_AHP_AMSEL = 0x00;
					break;
		
		case GPIOC :
					/*Enable clock on port C*/
					SET_BIT(RCGCGPIO,GPIOC);
					while(GET_BIT(PRGPIO,GPIOC)== 0);
					/* Unlock */
					GPIOC_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOC_AHP_CR   =0xff;
		
					GPIOC_AHP_AFSEL = 0x00;       // input output 
					GPIOC_AHP_AMSEL = 0x00;
					break;
		case GPIOD :
					/*Enable clock on port D*/
					SET_BIT(RCGCGPIO,GPIOD);
					while(GET_BIT(PRGPIO,GPIOD)== 0);
	      	/* Unlock */
					GPIOD_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOD_AHP_CR   =0xff;
		
					GPIOD_AHP_AFSEL = 0x00;       // input output 
					GPIOD_AHP_AMSEL = 0x00;
					break;
		case GPIOE :
					/*Enable clock on port E*/
					SET_BIT(RCGCGPIO,GPIOE);
					while(GET_BIT(PRGPIO,GPIOE)== 0);
					/* Unlock */
					GPIOE_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOE_AHP_CR   =0xff;
		
					GPIOE_AHP_AFSEL = 0x00;       // input output 
					GPIOE_AHP_AMSEL = 0x00;
					break;
		
		case GPIOF :
					/*Enable clock on port F*/
					SET_BIT(RCGCGPIO,GPIOF);
					while(GET_BIT(PRGPIO,GPIOF)== 0);
					/* Unlock */
					GPIOF_AHP_LOCK = GPIO_LOCK_KEY;
					GPIOF_AHP_CR   =0xff;
		
					GPIOF_AHP_AFSEL = 0x00;       // input output 
					GPIOF_AHP_AMSEL = 0x00;
					GPIOF_AHP_PUR = 0x01;
					break;
		
					
		default : break;
	}
	
}

void MGPIO_voidSetPinDirection (u8 copy_u8PORT,u8 copy_u8PIN, u8 copy_u8Mode  ) // set pin input or output
{
	switch(copy_u8PORT)
	{
		case GPIOA :
						CLR_BIT(GPIOA_AHP_DIR,copy_u8PIN);				   				  // reset pin 
						GPIOA_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));    // write the mode value (input or output)
						SET_BIT(GPIOA_AHP_DEN,copy_u8PIN);										// Digital
						break;
	
		case GPIOB :
						CLR_BIT(GPIOB_AHP_DIR,copy_u8PIN);                   // reset pin 
						GPIOB_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));   // write the value
						SET_BIT(GPIOB_AHP_DEN,copy_u8PIN);
						break;
		
		case GPIOC :
						CLR_BIT(GPIOC_AHP_DIR,copy_u8PIN);             // reset pin 
						GPIOC_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));   // write the value
						SET_BIT(GPIOC_AHP_DEN,copy_u8PIN);
						break;
	
		case GPIOD :
						CLR_BIT(GPIOD_AHP_DIR,copy_u8PIN);            // reset pin 
						GPIOD_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));   // write the value
					  SET_BIT(GPIOD_AHP_DEN,copy_u8PIN);
						break;
		
		case GPIOE :
						CLR_BIT(GPIOE_AHP_DIR,copy_u8PIN);             // reset pin 
						GPIOE_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));   // write the value
					 	SET_BIT(GPIOE_AHP_DEN,copy_u8PIN);
						break;
		
		case GPIOF :
						CLR_BIT(GPIOF_AHP_DIR,copy_u8PIN);           // reset pin 
						GPIOF_AHP_DIR |=   ((copy_u8Mode)<< (copy_u8PIN));   // write the value
						SET_BIT(GPIOF_AHP_DEN,copy_u8PIN);
						break;
	
						
		
		default : break;
		
	}
}


void MGPIO_voidSetPinValue (u8 copy_u8PORT,u8 copy_u8PIN, u8 copy_u8Value)
{
	switch(copy_u8PORT)
	{
		case GPIOA :
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOA_AHP_DATA,copy_u8PIN);
						
					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOA_AHP_DATA,copy_u8PIN);
						
					}
					break;
		case GPIOB :
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOB_AHP_DATA,copy_u8PIN);

					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOB_AHP_DATA,copy_u8PIN);

					}
					break;
		
		case GPIOC :
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOC_AHP_DATA,copy_u8PIN);
						
					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOC_AHP_DATA,copy_u8PIN);
						
					}
					break;
					
		case GPIOD :
			
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOD_AHP_DATA,copy_u8PIN);
						
					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOD_AHP_DATA,copy_u8PIN);
						
					}
					break;
		case GPIOE :
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOE_AHP_DATA,copy_u8PIN);
						
					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOE_AHP_DATA,copy_u8PIN);
						
					}
					break;
		case GPIOF :
					if (copy_u8Value == GPIO_HIGH) 
					{
						SET_BIT(GPIOF_AHP_DATA,copy_u8PIN);
						
					}
					else if (copy_u8Value == GPIO_LOW) 
					{
						CLR_BIT(GPIOF_AHP_DATA,copy_u8PIN);
						
					}
					break;
					
		default : break;
	}
}

u8 MGPIO_voidGETPinValue (u8 copy_u8PORT,u8 copy_u8PIN)
{
	u8 LOC_u8Result =0;
	switch(copy_u8PORT)
	{
		case GPIOA :
					LOC_u8Result = GET_BIT(GPIOA_AHP_DATA , copy_u8PIN);
					break;
		case GPIOB :
					LOC_u8Result = GET_BIT(GPIOB_AHP_DATA , copy_u8PIN);
					break;
		
		case GPIOC :
					LOC_u8Result = GET_BIT(GPIOC_AHP_DATA , copy_u8PIN);
					break;
		case GPIOD :
					LOC_u8Result = GET_BIT(GPIOD_AHP_DATA , copy_u8PIN);
					break;
		case GPIOE :
					LOC_u8Result = GET_BIT(GPIOE_AHP_DATA , copy_u8PIN);
					break;
		case GPIOF :
					LOC_u8Result = GET_BIT(GPIOF_AHP_DATA , copy_u8PIN);
					break;
		
					
		default : break;
	}
	return LOC_u8Result;
}


