/*****************************************************/
/* Auther : Eman Mohamed                             */
/* Date   : 23 March 2021                            */
/* Version: V01                                      */
/*****************************************************/

#ifndef MOTOR_INTERFACE_H
#define MOTOR_INTERFACE_H



#define MOTOR1   1
#define MOTOR2	 2

void HMOTOR_voidInit(void);
void HMOTOR_voidTurnRight(void);
void HMOTOR_voidTurnLeft(void);
void HMOTOR_voidStop(void);
void HMOTOR_voidForward(void);
void HMOTOR_voidBackward(void);
void HMOTOR_voidMotorSpeed(u8 Copy_u8motor , u8 Copy_u8speed);

#endif 
