/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 23 March 2021                            */
/* Version: V01                                      */
/*****************************************************/

#include "STD_TYPES.h"
#include "BIT_MATH.h"

#include "STK_interface.h"
#include "GPIO_interface.h"

#include "Motor_interface.h"
#include "Motor_config.h"

void HMOTOR_voidInit()
{
	MGPIO_voidInit(MOTOR1_PORT);
		MGPIO_voidInit(MOTOR2_PORT);
	
		MGPIO_voidSetPinDirection(MOTOR1_PORT,M1INA ,OUTPUT );
	  MGPIO_voidSetPinDirection(MOTOR1_PORT,M1INB ,OUTPUT );
  	MGPIO_voidSetPinDirection(MOTOR1_PORT,M1PWM ,OUTPUT );
	
		MGPIO_voidSetPinDirection(MOTOR2_PORT,M2INA ,OUTPUT );
		MGPIO_voidSetPinDirection(MOTOR2_PORT,M2INB ,OUTPUT );
		MGPIO_voidSetPinDirection(MOTOR2_PORT,M2PWM ,OUTPUT );
	
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INB,GPIO_HIGH);
	
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INB,GPIO_HIGH);
}
void HMOTOR_voidTurnRight()
{
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INA,GPIO_HIGH);
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INB,GPIO_LOW);
	
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INA,GPIO_HIGH);
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INB,GPIO_LOW);
}
void HMOTOR_voidTurnLeft()
{
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INA,GPIO_HIGH);
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INB,GPIO_LOW);
	
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INB,GPIO_HIGH);
}
void HMOTOR_voidStop()
{
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INB,GPIO_LOW);
	
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INB,GPIO_LOW);
}
void HMOTOR_voidForward()
{
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INA,GPIO_LOW);
		MGPIO_voidSetPinValue(MOTOR1_PORT,M1INB,GPIO_HIGH);
	
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INA,GPIO_HIGH);
		MGPIO_voidSetPinValue(MOTOR2_PORT,M2INB,GPIO_LOW);
}
void HMOTOR_voidMotorSpeed()
{
	
}
