
#include <stdint.h>
#include "../inc/tm4c123gh6pm.h"
#include "STD_TYPES.h"
#include "BIT_MATH.h"

//#include "GPIO_private.h"
#include "STK_interface.h"
#include "GPIO_interface.h"

#define GPIO_LOCK_KEY           0x4C4F434B  // Unlocks the GPIO_CR register
#define PF0       (*((volatile uint32_t *)0x40025004))
#define PF4       (*((volatile uint32_t *)0x40025040))
#define SWITCHES  (*((volatile uint32_t *)0x40025044))
#define SW1       0x10                      // on the left side of the Launchpad board
#define SW2       0x01                      // on the right side of the Launchpad board
#define SYSCTL_RCGC2_GPIOF      0x00000020  // port F Clock Gating Control
#define RED       0x02
#define BLUE      0x04
#define GREEN     0x08
void PortF_Init(void){ volatile uint32_t delay;
  SYSCTL_RCGCGPIO_R |= 0x00000020;  // 1) activate clock for Port F
  delay = SYSCTL_RCGCGPIO_R;        // allow time for clock to start
  GPIO_PORTF_LOCK_R = 0x4C4F434B;   // 2) unlock GPIO Port F
  GPIO_PORTF_CR_R = 0x1F;           // allow changes to PF4-0
  // only PF0 needs to be unlocked, other bits can't be locked
  GPIO_PORTF_AMSEL_R = 0x00;        // 3) disable analog on PF
  GPIO_PORTF_PCTL_R = 0x00000000;   // 4) PCTL GPIO on PF4-0
  GPIO_PORTF_DIR_R = 0x0E;          // 5) PF4,PF0 in, PF3-1 out
  GPIO_PORTF_AFSEL_R = 0x00;        // 6) disable alt funct on PF7-0
  GPIO_PORTF_PUR_R = 0x11;          // enable pull-up on PF0 and PF4
  GPIO_PORTF_DEN_R = 0x1F;          // 7) enable digital I/O on PF4-0
}
uint32_t PortF_Input(void){
  return (GPIO_PORTF_DATA_R&0x11);  // read PF4,PF0 inputs
}

void PortF_Output(uint32_t data){ // write PF3-PF1 outputs
  GPIO_PORTF_DATA_R = data;
}





#define M1INA  GPIOD,PIN0
#define M1INB  GPIOD,PIN1

#define M1PWM  GPIOD,PIN2
#define M2INA  GPIOB,PIN0
#define M2INB  GPIOB,PIN1
#define M2PWM  GPIOB,PIN2

int main (void)
{
	/*initialize SYSTICK*/
	MSTK_voidInit();
 // PortF_Init();
  MGPIO_voidInit(GPIOD);
	MGPIO_voidInit(GPIOB);

	
	MGPIO_voidSetPinDirection(M1INA ,OUTPUT );
	MGPIO_voidSetPinDirection(M1INB ,OUTPUT );
	MGPIO_voidSetPinDirection(M2INA ,OUTPUT );
	MGPIO_voidSetPinDirection(M2INB ,OUTPUT );
	MGPIO_voidSetPinDirection(M1PWM ,OUTPUT );
	MGPIO_voidSetPinDirection(M2PWM ,OUTPUT );
	
	MGPIO_voidSetPinValue(M1INA,GPIO_LOW);
	
	MGPIO_voidSetPinValue(M1INB,GPIO_HIGH);
	
	MGPIO_voidSetPinValue(M2INA,GPIO_LOW);
	
	MGPIO_voidSetPinValue(M2INB,GPIO_HIGH);
	
		MGPIO_voidSetPinValue(M2INA,GPIO_HIGH);
	
	
	

	//MGPIO_voidSetPinDirection(GPIOF , PIN0 ,INPUT );
	//portD();





	while (1)
	{/*
			MGPIO_voidSetPinValue(M2INA,GPIO_LOW);
			MSTK_voidDelay_ms(1);
			MGPIO_voidSetPinValue(M2INB,GPIO_HIGH);
			MSTK_voidDelay_ms(1);*/
	}



}

/*
		if (MGPIO_voidGETPinValue(GPIOF , PIN0) == 0)
		{
			MGPIO_voidSetPinValue(GPIOD , PIN0,GPIO_HIGH);
			MGPIO_voidSetPinValue(GPIOD , PIN1,GPIO_LOW);
		}
		else
		{
				MGPIO_voidSetPinValue(GPIOD , PIN0,GPIO_LOW);
				MGPIO_voidSetPinValue(GPIOD , PIN1,GPIO_HIGH);
		}
		PortF_Output(RED);
		MSTK_voidDelay_ms(1000);
		PortF_Output(0x00) ;
	  MSTK_voidDelay_ms(1000);
		MSTK_voidDelay_ms(1000);
	
		MSTK_voidDelay_ms(1000);
		*/
